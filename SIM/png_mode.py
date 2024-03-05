"""
Usage: python png_mode.py <PNG_FILE> verbose

检查 png mode

verbose: 0 不打印图片信息，1 打印图片信息

"""
import sys
import numpy as np
from PIL import Image

def print_img_info(img):
        print(img)

        # 按照像素行打印
        for i in range(img.size[1]):
            for j in range(img.size[0]):
                print(img.getpixel((j, i)), end=" ")
            print()
        
        # # 获取图像的像素数据
        # pixels = list(img.getdata())
        # # 打印所有像素
        # for pixel in pixels:
        #     print(pixel)

        # 打印前 10 个像素
        # pixels = np.array(img)
        # print(pixels[0][:10])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png_mode.py <PNG_FILE> verbose")
        sys.exit(1)
    PNG_FILE = sys.argv[1]
    verbose = int(sys.argv[2])

    try:
        img = Image.open(PNG_FILE)
    except Exception as e:
        print(f"Error reading PNG file: {e}")
        sys.exit(1)  # 1 表示异常退出
    print(img.mode)
    if verbose > 0:
        print("################## original image ###################")
        print_img_info(img)

        # 转为 RGBA
        print("################## image convert RGBA ###################")
        img = img.convert("RGBA")
        print_img_info(img)
