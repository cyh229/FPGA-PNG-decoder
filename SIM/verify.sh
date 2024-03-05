#!/bin/bash

###############################################
# test_image

# 指定目录
output_directory="/home/oem/cyh/png/FPGA-PNG-decoder/SIM/output/PngSuite-2017jul19/txt"
input_directory="/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/PngSuite-2017jul19/renamed"
map_csv_path="/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/PngSuite-2017jul19/map_filepath.csv"

# 检查 CSV 文件是否存在
CSV_path="/home/oem/cyh/png/FPGA-PNG-decoder/SIM/output/PngSuite-2017jul19/valid.csv"
if [ -e "$CSV_path" ]; then
    # 如果文件存在，则删除它
    rm "$CSV_path"
fi
echo "img,txt,img_original,idx,basename,test_feature,parameter,interlaced,color-type,bit-depth,PIL_mode,color_type(identify),valid_PIL,valid_opencv" > "$CSV_path"

# 遍历指定目录下的所有txt文件
for img_filepath in $input_directory/*.png; do # 验证能够解码的结果的正确性
    # 获取文件名（去除路径和后缀）
    filename=$(basename -- "$img_filepath") # e.g. 001.png
    filename_no_ext="${filename%.png}" # e.g. 001

    # 拼接得到 txt 文件路径
    txt_filepath="${output_directory}/${filename_no_ext}.txt"

    echo -n "${img_filepath},${txt_filepath}," >> "$CSV_path" # img,txt,

    # 获取原始图片路径
    img_original_filepath=$(python get_original_img_path.py "$img_filepath" "$map_csv_path")
    echo -n "$img_original_filepath,$filename_no_ext," >> "$CSV_path" # img_original,idx,

    # basename
    img_original_basename=$(basename -- "$img_original_filepath") # e.g. tbyn3p08.png
    echo -n "$img_original_basename," >> "$CSV_path" # basename,

    # basename breakdown
    basename_no_ext="${img_original_basename%.png}" # e.g. tbyn3p08
    # test_feature,parameter,interlaced,color-type,bit-depth
    test_feature="${basename_no_ext:0:1}" # e.g. t
    parameter="${basename_no_ext:1:2}" # e.g. by
    interlaced="${basename_no_ext:3:1}" # e.g. n
    color_type="${basename_no_ext:4:2}" # e.g. 3p
    bit_depth="${basename_no_ext:6:2}" # e.g. 08
    echo -n "$test_feature,$parameter,$interlaced,$color_type,$bit_depth," >> "$CSV_path" # test_feature,parameter,interlaced,color-type,bit-depth,

    PIL_mode=$(python png_mode.py "$img_filepath" 0) # 不获取详细信息
    echo -n "$PIL_mode," >> "$CSV_path" # PIL_mode,

    # 运行 identify 得到的 color_type
    color_type=$(identify -verbose $img_filepath | grep "png:IHDR.color_type:" | awk '{print $3}' | tr -d '()')
    echo -n "$color_type," >> "$CSV_path" # color_type(identify),

    # 如果 txt 文件存在，验证解码结果
    if [ -e "$txt_filepath" ]; then
        # 执行 python validation.py
        # PIL 报错处理
        valid_PIL=$(python validation.py "$img_filepath" "$txt_filepath")
        echo -n "$valid_PIL," >> "$CSV_path" # valid_PIL,

        # opencv 报错处理
        ./validation "$img_filepath" "$txt_filepath" >> "$CSV_path"
    else
        echo "" >> "$CSV_path" # '\n'
    fi

done

###############################################
# test_image

# # 指定目录
# output_directory="/home/oem/cyh/png/FPGA-PNG-decoder/SIM/output/test_image/txt"
# input_directory="/home/oem/cyh/png/FPGA-PNG-decoder/SIM/data/test_image"

# # 遍历指定目录下的所有txt文件
# for filepath in $output_directory/*.txt; do # 验证能够解码的结果的正确性
#     # 获取文件名（去除路径和后缀）
#     filename=$(basename -- "$filepath")
#     filename_no_ext="${filename%.txt}"

#     # 将 "out" 替换为 "img" 得到新的文件名
#     img_filename="${filename_no_ext/out/img}"

#     # 拼接新的文件路径
#     img_filepath="${input_directory}/${img_filename}.png"

#     # 执行 python validation.py
#     python validation.py "$img_filepath" "$filepath"
#     echo "validate" "$img_filepath" "$filepath"

# done
