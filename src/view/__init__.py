import os
import sys

# Get the parent directory path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Insert the parent directory into the system path
sys.path.insert(0, parent_dir)
