"""
python txt_map.py <map_filepath> <input_txt_folder> <output_txt_folder>

从 map_filename.csv 读出 (Original Name, New Name)，建立 New Name 到 Original Name 的映射，
然后从 txt_folder 下找到，和  New Name 相同 basename 的 txt 文件，以 Original Name 作为 basename 复制到 output_folder 下
"""
import sys
import os
import csv
import shutil

def read_csv_mapping(csv_filename):
    mapping = {}
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            original_name, new_name = row
            # 去除 .png 后缀
            original_name = original_name.split(".")[0].strip()
            new_name = new_name.split(".")[0].strip()
            mapping[new_name] = original_name
    return mapping

def copy_files_based_on_mapping(txt_folder, output_folder, mapping):
    for txt_filename in os.listdir(txt_folder):
        if txt_filename.endswith(".txt"):
            # Get the basename without extension
            base_name, _ = os.path.splitext(txt_filename)

            # Check if the basename is in the mapping
            if base_name in mapping:
                original_name = mapping[base_name]
                output_filename = os.path.join(output_folder, f"{original_name}.txt")

                # Copy the file to the output folder
                shutil.copy2(os.path.join(txt_folder, txt_filename), output_filename)
                print(f"File '{txt_filename}' copied to '{output_filename}'.")
            else:
                print(f"File '{txt_filename}' not found in the mapping.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python txt_map.py <map_filepath> <input_txt_folder> <output_txt_folder>")
        sys.exit(1)
    map_filepath = sys.argv[1]
    input_txt_folder = sys.argv[2]
    output_txt_folder = sys.argv[3]

    # 确保输出文件夹存在，如果不存在则创建
    os.makedirs(output_txt_folder, exist_ok=True)

    # 读取映射
    mapping = read_csv_mapping(map_filepath)

    # 复制文件
    copy_files_based_on_mapping(input_txt_folder, output_txt_folder, mapping)