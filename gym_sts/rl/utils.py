import typing as tp

from gymnasium import spaces


def assert_contains(space: spaces.Space, element: tp.Any):
    """Use with post-mortem debugging to see where in the space the error is."""
    if isinstance(space, spaces.Dict):
        assert isinstance(element, tp.Mapping)

        for key, subspace in space.items():
            assert_contains(subspace, element[key])
    assert space.contains(element)
