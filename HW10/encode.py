import argparse
import os
import math
import numpy as np
from scipy import fftpack
from PIL import Image
from matplotlib import pyplot as plt
from skimage import img_as_ubyte
import cv2
from utility import *
from huffmantree import HuffmanTree
import imageio


if __name__ == "__main__":
    img = imageio.imread('source.png')
    # 块大小
    B = 8
    # 图片的大小，保证图片大小可以被8整除
    height, width = (np.array(img.shape[:2]) / B * B).astype(np.int32)
    img = img[:height, :width]
    # 把RGB转换成YCbCr颜色模型
    ycbcr = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
    # 显示YCbCr图片
    # plt.imshow(ycbcr)
    # plt.show()
    # 每两个像素垂直采样一次
    vertical_subsample = 2
    # 每两个像素水平采样一次
    horizontal_subsample = 2

    # 2*2平滑滤波（取区域内的平均值）
    crf = cv2.boxFilter(ycbcr[:, :, 1], ddepth=-1, ksize=(2, 2))
    cbf = cv2.boxFilter(ycbcr[:, :, 2], ddepth=-1, ksize=(2, 2))

    # 每隔一行和一列采样，即2*2区域内采样一次
    crsub = crf[::vertical_subsample, ::horizontal_subsample]
    cbsub = cbf[::vertical_subsample, ::horizontal_subsample]

    # 将三个通道下采样后的像素值存入列表
    sub_img = [ycbcr[:, :, 0], crsub, cbsub]
    # 输出大小检验
    print(ycbcr[:,:,0].size)
    print(crsub.size)
    print(cbsub.size)

    # 亮度和色度量化表
    QY = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                   [12, 12, 14, 19, 26, 48, 60, 55],
                   [14, 13, 16, 24, 40, 57, 69, 56],
                   [14, 17, 22, 29, 51, 87, 80, 62],
                   [18, 22, 37, 56, 68, 109, 103, 77],
                   [24, 35, 55, 64, 81, 104, 113, 92],
                   [49, 64, 78, 87, 103, 121, 120, 101],
                   [72, 92, 95, 98, 112, 100, 103, 99]])

    QC = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                   [18, 21, 26, 66, 99, 99, 99, 99],
                   [24, 26, 56, 99, 99, 99, 99, 99],
                   [47, 66, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99]])
    # 所有dct变换后的块
    dct_blocks = []
    # 所有量化后的块
    quan_blocks = []
    # YCrCb颜色通道
    ch = ['Y', 'Cr', 'Cb']
    # 量化表
    Q = [QY, QC, QC]
    # 所有z扫描后的向量
    Zs = []
    # 遍历每个颜色通道
    for index, channel in enumerate(sub_img):
        # 行数
        rows = channel.shape[0]
        # 列数
        cols = channel.shape[1]
        print(rows)
        print(cols)
        # dct变换后的块
        dct_block = np.zeros((rows, cols), np.int32)
        # 量化后的块
        quan_block = np.zeros((rows, cols), np.int32)
        # 块的行数
        block_rows = int(rows / B)
        # 块的列数
        block_cols = int(cols / B)

        # z扫描后的向量
        z = []

        block = np.zeros((rows, cols), np.float32)
        block[:rows, :cols] = channel
        # 整齐化，减128使Y分量（DC）成为均值为0。
        block = block - 128
        # 处理每个块
        for row in range(block_rows):
            for col in range(block_cols):
                # 当前块
                currentblock = fftpack.dct(
                    fftpack.dct(block[row * B:(row + 1) * B, col * B:(col + 1) * B].T, norm='ortho').T,
                    norm='ortho').round().astype(np.int32)
                # 存储二维dct变换后的块
                dct_block[row * B:(row + 1) * B, col * B:(col + 1) * B] = currentblock
                # 存储量化后的块
                quan_block[row * B:(row + 1) * B, col * B:(col + 1) * B] = np.round(currentblock / Q[index])
                # z扫描
                z.append(block_to_zigzag(quan_block[row * B:(row + 1) * B, col * B:(col + 1) * B]))

        dct_blocks.append(dct_block)
        quan_blocks.append(quan_block)
        Zs.append(z)

    dcs = dcpm(Zs)
    dcs_values = dc(Zs)
    acs_symbol1 = rlc(Zs)
    acs = ac(Zs)
    acs_bin = rlc_values(Zs)
    # print(len(dcs1[0]))
    H_DC_Y = HuffmanTree(dcs[0])
    H_DC_C = HuffmanTree(dcs[1] + dcs[2])
    H_AC_Y = HuffmanTree(flatten(acs_symbol1[0]))
    H_AC_C = HuffmanTree(flatten(acs_symbol1[1]) + flatten(acs_symbol1[2]))

    tables = {'dc_y': H_DC_Y.value_to_bitstring_table(),
              'ac_y': H_AC_Y.value_to_bitstring_table(),
              'dc_c': H_DC_C.value_to_bitstring_table(),
              'ac_c': H_AC_C.value_to_bitstring_table()}

    count = write_to_file('encode.b', dcs, dcs_values, acs_symbol1, acs_bin, tables)
    print("图片写入位数：\n", count)
