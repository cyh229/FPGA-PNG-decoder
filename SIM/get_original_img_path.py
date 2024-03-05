"""
usage: python get_original_img_path.py <filepath> <map_filepath>

获取原始图片路径，根据 map_filepath.csv 读出 (Original Path, New Path)，建立 New Path 到 Original Path 的映射，
"""

import sys
import csv

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python get_original_img_path.py <filepath> <map_filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    map_filepath = sys.argv[2]
    mapping = {}
    with open(map_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            original_name, new_name = row
            mapping[new_name] = original_name

    if filepath in mapping:
        print(mapping[filepath])
    else:
        print(f"File '{filepath}' not found in the mapping.")