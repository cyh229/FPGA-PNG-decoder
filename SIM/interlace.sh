# 对指定目录下所有 png 执行 
# identify -verbose <png_path> | grep interlace_method

#!/bin/bash

# 指定目录路径
directory_path="/mnt/nvme0/OpenDataLab___CityScapes/sample/image"

# 遍历目录下的所有 PNG 文件
for png_file in "$directory_path"/*.png; do
    if [ -f "$png_file" ]; then
        # 执行 identify -verbose 命令，并筛选包含 "interlace_method" 的行
        interlace_method=$(identify -verbose "$png_file" | grep "interlace_method" | awk '{print $2}')

        # 输出文件名和对应的 interlace_method 行
        echo "$png_file : $interlace_method"
    fi
done
