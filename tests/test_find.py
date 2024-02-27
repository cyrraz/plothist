import os

def find_files_by_name(root_dir, filename):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == filename:
                print(os.path.join(root, file))

def test_find():
    root_dir = "/"  # Example root directory (change as needed)
    filename = "fontlist-v330.json"
    find_files_by_name(root_dir, filename)
    assert False