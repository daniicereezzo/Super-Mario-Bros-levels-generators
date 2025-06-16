import os
import sys

def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
        print(f"Directory '{dir_name}' created successfully.")
    except FileExistsError:
        print(f"WARNING: Directory '{dir_name}' already exists.")
    except PermissionError:
        print(f"ERROR: Permission denied: Unable to create '{dir_name}'.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)