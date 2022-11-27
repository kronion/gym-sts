import numpy as np
import pickle

from absl import app
from absl import flags

from gym import spaces
import torch
import torch.nn as nn
import tree

from gym_sts.envs import base

DATA = flags.DEFINE_string(
  'data', 'data/states.pkl', 'path to data')

LR = flags.DEFINE_float('lr', 1e-3, 'learning rate')

def one_hot(x, n):
  return nn.functional.one_hot(x.to(torch.int64), n).to(torch.float32)

def space_as_nest(space: spaces.Space):
  if isinstance(space, spaces.Dict):
    return {k: space_as_nest(v) for k, v in space.items()}
  if isinstance(space, spaces.Tuple):
    return tuple(map(space_as_nest, space))
  return space

def encode(space, x):
  if isinstance(space, spaces.Discrete):
    return one_hot(x, space.n)
  if isinstance(space, spaces.MultiBinary):
    return x.to(torch.float32)
  if isinstance(space, spaces.MultiDiscrete):
    one_hots = []
    for n, y in zip(space.nvec, torch.unbind(x, -1)):
      one_hots.append(one_hot(y, n))
    return torch.cat(one_hots, dim=-1)
  if isinstance(space, (spaces.Dict, spaces.Tuple)):
    encodings = tree.map_structure(encode, space_as_nest(space), x, check_types=False)
    return torch.cat(tree.flatten(encodings), dim=-1)
  raise NotImplementedError(type(space))

def space_size(space) -> int:
  if isinstance(space, spaces.Discrete):
    return space.n
  if isinstance(space, spaces.MultiBinary):
    assert isinstance(space.n, int)
    return space.n
  if isinstance(space, spaces.MultiDiscrete):
    return space.nvec.sum()
  if isinstance(space, spaces.Dict):
    space = space_as_nest(space)
    return sum(map(space_size, tree.flatten(space)))
  raise NotImplementedError(type(space))

ce_loss = nn.CrossEntropyLoss(reduction='none')

def to_tensor(x: np.ndarray):
  if x.dtype == np.uint16:
    x = x.astype(np.int16)
  return torch.from_numpy(x)

def struct_loss(space, x, y):
  if isinstance(space, spaces.Discrete):
    return ce_loss(x, y.to(torch.int64))

  if isinstance(space, spaces.MultiBinary):
    loss = nn.BCEWithLogitsLoss(reduction='none')(x, y.to(torch.float32))
    return torch.sum(loss, dim=-1)

  if isinstance(space, spaces.MultiDiscrete):
    assert y.shape[-1] == len(space.nvec)
    losses = []
    logits = torch.split(x, tuple(space.nvec), dim=-1)
    for x_, y_ in zip(logits, torch.unbind(y, -1)):
      losses.append(ce_loss(x_, y_.to(torch.int64)))
    loss = torch.stack(losses, dim=-1)
    return torch.sum(loss, dim=-1)

  if isinstance(space, (spaces.Dict, spaces.Tuple)):
    space = space_as_nest(space)
    flat_spaces = tree.flatten(space)
    space_sizes = tuple(map(space_size, flat_spaces))
    assert sum(space_sizes) == x.shape[-1]
    xs = torch.split(x, space_sizes, dim=-1)
    xs_tree = tree.unflatten_as(y, xs)
    return tree.map_structure(struct_loss, space, xs_tree, y, check_types=False)

  raise NotImplementedError(type(space))

def make_auto_encoder(input_size: int, depth: int, width: int):
  layers = [
      nn.Linear(input_size, width),
      nn.LeakyReLU(),
  ]

  for _ in range(depth):
    layers.extend([
        nn.Linear(width, width),
        nn.LeakyReLU(),
    ])
  layers.append(nn.Linear(width, input_size))
  return nn.Sequential(*layers)

def main(_):
  with open(DATA.value, "rb") as f:
    column_major = pickle.load(f)

  total_size = len(tree.flatten(column_major)[0])
  train_size = round(total_size * 0.8)
  print('total states:', total_size)

  train_set = tree.map_structure(lambda x: x[:train_size], column_major)
  valid_set = tree.map_structure(lambda x: x[train_size:], column_major)

  train_tensor = tree.map_structure(to_tensor, train_set)
  valid_tensor = tree.map_structure(to_tensor, valid_set)

  input_size = space_size(base.OBSERVATION_SPACE)
  print('input_size', input_size)

  obs_space = space_as_nest(base.OBSERVATION_SPACE)
  flat_spaces = tree.flatten(obs_space)
  print('num components:', len(flat_spaces))

  # prepare data
  flat_train_data = tree.flatten(train_tensor)
  train_dataset = torch.utils.data.TensorDataset(*flat_train_data)
  data_loader = torch.utils.data.DataLoader(train_dataset, batch_size=100, shuffle=True, drop_last=True)
  assert len(data_loader)
  print('num batches', len(data_loader))

  input_dim = space_size(base.OBSERVATION_SPACE)
  auto_encoder = make_auto_encoder(input_dim, depth=1, width=128)

  optimizer = torch.optim.Adam(auto_encoder.parameters(), lr=LR.value)
  scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.2, patience=5, min_lr=5e-7)

  training_losses = []
  val_losses = []

  def get_loss(batch):
    batch = tree.unflatten_as(obs_space, batch)
    # x = list(map(encode, flat_spaces, batch))
    x = encode(base.OBSERVATION_SPACE, batch)
    x = auto_encoder.forward(x)
    losses = struct_loss(base.OBSERVATION_SPACE, x, batch)
    losses = tree.flatten(losses)
    losses = torch.stack(losses, 1)
    losses = torch.sum(losses, 1)
    return torch.mean(losses, 0)

  def train():
      total_batches = len(data_loader)
      for batch_num, batch in enumerate(data_loader):
          # loss = LOSS_FN(batch, auto_encoder.forward(batch))
          loss = get_loss(batch)
          loss.backward()
          print(f"Batch: {batch_num+1}/{total_batches} loss: {loss.double()}", end="\n")
          training_losses.append(float(loss))
          optimizer.step()
      val_loss = get_loss(tree.flatten(valid_tensor))
      print(f"\nValidation loss: {val_loss}")
      val_losses.append(float(val_loss))
      scheduler.step(val_loss)

  for epoch in range(10):
      print(f"Epoch {epoch}")
      train()

if __name__ == '__main__':
  app.run(main)
