import os

def init_fifos(filenames):
    # Create fifos for communication
    for f in filenames:
        if os.path.exists(f):
            os.remove(f)
        os.mkfifo(f)