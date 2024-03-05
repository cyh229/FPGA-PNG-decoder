import struct
import sys
import os

def parse_png_ihdr(file_path):
    with open(file_path, 'rb') as file:
        # PNG文件的头部是8个字节的固定签名
        signature = file.read(8)
        if signature[:8] != b'\x89PNG\r\n\x1a\n':
            print("不是有效的PNG文件")
            return

        # 逐块读取文件，直到找到IHDR块
        while True:
            length_data = file.read(4)
            length = struct.unpack('!I', length_data)[0]
            chunk_type = file.read(4)

            if chunk_type == b'IHDR':
                # 读取IHDR块的数据
                width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack('!IIBBBBB', file.read(13))

                # 输出IHDR块的内容
                # print("宽度:", width)
                # print("高度:", height)
                # print("位深度:", bit_depth)
                # print("颜色类型:", color_type)
                # print("压缩方法:", compression)
                # print("滤波方法:", filter_method)
                # print("隔行扫描:", interlace)
                # print("width, height, bit_depth, color_type, compression, filter_method, interlace")
                print("{},{},{},{},{},{},{}".format(width, height, bit_depth, color_type, compression, filter_method, interlace))
                break
            else:
                # 跳过当前块的数据
                file.seek(length + 4, 1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python IHDR.py <PNG file>")
        sys.exit(1)
    png_file_path = sys.argv[1]

    # 如果是 png 文件，调用 parse_png_ihdr 函数；如果是目录，则遍历目录下的所有 png 文件
    if png_file_path.endswith('.png'):
        print("width,height,bit_depth,color_type,compression,filter_method,interlace")
        parse_png_ihdr(png_file_path)
    elif os.path.isdir(png_file_path):
        print("filepath,width,height,bit_depth,color_type,compression,filter_method,interlace")
        for root, dirs, files in os.walk(png_file_path):
            files.sort()
            for file in files:
                if file.endswith('.png'):
                    file_path = os.path.join(root, file)
                    print("{},".format(file_path), end="")
                    parse_png_ihdr(file_path)
