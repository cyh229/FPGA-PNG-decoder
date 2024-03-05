"""
20240229:

因为 Verilog 比较低级，不能像其他高级语言一样遍历文件夹，依次将文件输入，所以只能先按着原先的仿真文件类似的方式，按照图片序号解码图片。

然后，使用 python 改名，并将映射关系记录在 csv 文件中

map_filename.csv : 保存原始文件名和新文件名的映射关系
map_filepath.csv : 保存原始文件路径和新文件路径的映射关系

"""

import os
from shutil import copyfile
import csv
import sys


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python rename.py <original_folder> <target_folder> <csv_folder>")
        sys.exit(1)

    # 指定原始文件夹和目标文件夹
    original_folder = sys.argv[1]
    target_folder =   sys.argv[2]
    csv_folder =      sys.argv[3]    
    
    # # PngSuite
    # original_folder = '/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/PngSuite-2017jul19/origin'
    # target_folder =   '/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/PngSuite-2017jul19/renamed'
    # csv_folder =      '/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/PngSuite-2017jul19/'

    # # CityScapes sample suite
    # original_folder = '/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/CityScapes/sample_suite'
    # target_folder =   '/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/CityScapes/sample_renamed'
    # csv_folder =      '/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/CityScapes/'

    os.makedirs(target_folder, exist_ok=True)

    # 遍历原始文件夹中的文件
    file_list = os.listdir(original_folder)
    # 保证为 png 文件
    file_list = [filename for filename in file_list if filename.endswith('.png')]
    file_list.sort()

    # 保存文件名映射关系到 map.csv
    with open(csv_folder + "map_filename.csv", 'w', newline='') as csv_filename:
        with open(csv_folder + "map_filepath.csv", 'w', newline='') as csv_filepath:
            csv_filename_writer = csv.writer(csv_filename)
            csv_filename_writer.writerow(['Original Name', 'New Name'])
            csv_filepath_writer = csv.writer(csv_filepath)
            csv_filepath_writer.writerow(['Original Path', 'New Path'])

            # 遍历文件列表并重命名文件
            for index, filename in enumerate(file_list):
                original_path = os.path.join(original_folder, filename)
                new_filename = f"{index+1:03d}.png"
                new_path = os.path.join(target_folder, new_filename)

                # 复制文件
                copyfile(original_path, new_path)

                # 写入映射关系到 CSV 文件
                csv_filename_writer.writerow([filename, new_filename])
                csv_filepath_writer.writerow([original_path, new_path])

    # print("重命名完成，并且映射关系已保存到 map.csv 文件中。")
