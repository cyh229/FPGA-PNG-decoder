/*
cpp opencv 检验解码结果，思路是比较 opencv 读取的 png 各像素 RGBA 4通道的值，和 output.txt 读入的数据进行对比，对于 output.txt
第一行，形如 "decode result:  colortype:0  width:32  height:32"，后续则是形如 "000000ff 010101ff 020202ff 030303ff " 每个像素(从左到右，从上到下)的 RGBA值
*/
#include <opencv2/opencv.hpp>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char* argv[]) {
    // 检查命令行参数数量
    if (argc != 3) {
        cout << "Usage: " << argv[0] << " <path_to_png> <path_to_txt>" << endl;
        return -1;
    }

    // 读取PNG文件
    Mat image;
    try {
        image = imread(argv[1], IMREAD_UNCHANGED); // 保证 A 顺利读取
        if (image.empty()) {
            throw cv::Exception(1, "Error: Unable to read " + string(argv[1]), "main", "ReadImage", 1);
        }
    }
    catch (cv::Exception& e) {
        const char* err_msg = e.what();
        cout << "Exception caught: " << err_msg; // << endl;
        return -1;
    }


    // 确保图像为四通道（RGBA）
    if (image.channels() != 4) {
        cvtColor(image, image, COLOR_BGR2BGRA);
    }

    // 读取output.txt文件
    ifstream infile(argv[2]);
    if (!infile.is_open()) {
        cout << "Error: Unable to open " << argv[2] << "." << endl;
        return -1;
    }

    // cout << "Files opened successfully." << endl;

    // 读取第一行，获取colortype、width、height
    string line;
    getline(infile, line);

    // 从第一行提取colortype、width、height信息
    int colortype, width, height;
    if (sscanf(line.c_str(), "decode result: colortype:%d width:%d height:%d", &colortype, &width, &height) != 3) {
        cout << "Error: Unable to extract colortype, width, and height from the first line." << endl;
        return -1;
    }

    // cout << "Colortype: " << colortype << ", width: " << width << ", height: " << height << "." << endl;

    // 检验图像属性
    if (image.cols != width || image.rows != height || image.channels() != 4) {
        cout << "Error: Image dimensions or channels do not match." << "png: " << image.cols << "x" << image.rows << "x" << image.channels() << "  txt: " << width << "x" << height << "x4" << "." << endl;
        return -1;
    }

    // cout << "Image dimensions and channels match the expected values." << endl;

    // 检验colortype（如果需要）
    // ...

    // 逐像素比较
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            Vec4b pixel = image.at<Vec4b>(y, x);

            // 读取output.txt中的RGBA值
            string rgba_str;
            infile >> rgba_str;

            // 转换为Vec4b格式
            Vec4b expected_pixel;
            sscanf(rgba_str.c_str(), "%02hhx%02hhx%02hhx%02hhx", &expected_pixel[2], &expected_pixel[1], &expected_pixel[0], &expected_pixel[3]); // opencv BGRA <- txt RGBA

            // 检验每个通道的值
            for (int i = 0; i < 4; ++i) {
                if (pixel[i] != expected_pixel[i]) {
                    cout << "Error: Pixel mismatch at position (" << x << ". " << y << ") " << "png: [" << (int)pixel[0] << " " << (int)pixel[1] << ". " << (int)pixel[2] << ". " << (int)pixel[3] << "]  txt: [" << (int)expected_pixel[0] << ". " << (int)expected_pixel[1] << ". " << (int)expected_pixel[2] << ". " << (int)expected_pixel[3] << "]." << endl;
                    return -1;
                }
            }
        }
    }

    cout << "Decoding results match the expected values." << endl;

    return 0;
}
