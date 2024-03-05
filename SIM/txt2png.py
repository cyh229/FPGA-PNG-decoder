"""
python txt2png.py <txt_input_folder> <origin_img_folder> <output_folder>

将 txt 转为 png，并且将原始的 png 复制过来对比
"""


import sys
import os
from PIL import Image
import numpy as np
import shutil

def process_txt_file(txt_path, origin_img_folder, output_folder):
    # 读取.txt文件中的像素数据
    with open(txt_path, "rt") as txt:
        height, width = 0, 0
        for line in txt.readlines():
            if height>0 and width>0:
                arr = np.zeros([height*width,4], dtype=np.uint8)
                for idx, value in enumerate(line.split()):
                    rgba = [int(value[0:2],16), int(value[2:4],16), int(value[4:6],16), int(value[6:8],16)]
                    arr[idx] = rgba
                # return height, width, arr
            if line.startswith("decode result"):
                height, width = 0, 0
                for item in line.split():
                    pair = item.split(':')
                    try:
                        name, value = pair[0].strip(), int(pair[1].strip())
                        if name == "height":
                            height = value
                        elif name == "width":
                            width = value
                    except:
                        pass

    # 创建一个RGBA模式的图像
    img = Image.fromarray(arr.reshape(height, width, 4), 'RGBA')
    
    # 生成输出 PNG 图片的路径
    basename = os.path.splitext(os.path.basename(txt_path))[0]
    output_filename = basename + "_new.png"
    output_path = os.path.join(output_folder, output_filename)

    # 将图像保存为 PNG 文件，支持透明通道
    img.save(output_path, format='PNG')

    print("PNG 图片已创建:", output_path)

    # 复制原始图片
    origin_img_name = basename + ".png"
    shutil.copyfile(os.path.join(origin_img_folder, origin_img_name), os.path.join(output_folder, origin_img_name))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python txt2png.py <txt_input_folder> <origin_img_folder> <output_folder>")
        sys.exit(1)

    # 设置输入 .txt 文件所在的文件夹
    input_folder = sys.argv[1]
    # 设置原始图片所在的文件夹
    origin_img_folder = sys.argv[2]
    # 设置输出 .png 文件所在的文件夹
    output_folder = sys.argv[3]

    # 确保输出文件夹存在，如果不存在则创建
    os.makedirs(output_folder, exist_ok=True)

    # 处理所有.txt文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            txt_path = os.path.join(input_folder, filename)
            process_txt_file(txt_path, origin_img_folder, output_folder)