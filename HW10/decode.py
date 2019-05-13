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

class JPEGFileReader:
    TABLE_SIZE_BITS = 16
    BLOCKS_COUNT_BITS = 32

    DC_CODE_LENGTH_BITS = 4
    CATEGORY_BITS = 4

    AC_CODE_LENGTH_BITS = 8
    RUN_LENGTH_BITS = 4
    SIZE_BITS = 4

    def __init__(self, filepath):
        self.__file = open(filepath, 'r')

    def read_int(self, size):
        if size == 0:
            return 0

        # the most significant bit indicates the sign of the number
        bin_num = self.__read_str(size)
        if bin_num[0] == '1':
            return self.__int2(bin_num)
        else:
            return self.__int2(binstr_flip(bin_num)) * -1

    def read_dc_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            category = self.__read_uint(self.CATEGORY_BITS)
            code_length = self.__read_uint(self.DC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = category
        return table

    def read_ac_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            run_length = self.__read_uint(self.RUN_LENGTH_BITS)
            size = self.__read_uint(self.SIZE_BITS)
            code_length = self.__read_uint(self.AC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = (run_length, size)
        return table

    def read_blocks_count(self):
        return self.__read_uint(self.BLOCKS_COUNT_BITS)

    def read_huffman_code(self, table):
        prefix = ''
        # TODO: break the loop if __read_char is not returing new char
        while prefix not in table:
            prefix += self.__read_char()
        return table[prefix]

    def __read_uint(self, size):
        if size <= 0:
            raise ValueError("size of unsigned int should be greater than 0")
        return self.__int2(self.__read_str(size))

    def __read_str(self, length):
        return self.__file.read(length)

    def __read_char(self):
        return self.__read_str(1)

    def __int2(self, bin_num):
        return int(bin_num, 2)


def read_image_file(filepath):
    reader = JPEGFileReader(filepath)

    tables = dict()
    for table_name in ['dc_y', 'ac_y', 'dc_c', 'ac_c']:
        if 'dc' in table_name:
            tables[table_name] = reader.read_dc_table()
        else:
            tables[table_name] = reader.read_ac_table()

    Y_blocks_count = reader.read_blocks_count()
    
    # print(Y_blocks_count)
    # print(tables['ac_y'])

    dcs = []
    acss = []
    dc = []
    acs = []
    for i in range(Y_blocks_count):
        dc_table = tables['dc_y'] 
        ac_table = tables['ac_y']

        category = reader.read_huffman_code(dc_table)
        # dcs[0][i] = reader.read_int(category)
        dc.append(reader.read_int(category))

        cells_count = 0
        ac = []

        # TODO: try to make reading AC coefficients better
        while cells_count < 63:
            run_length, size = reader.read_huffman_code(ac_table)

            if (run_length, size) == (0, 0):
                while cells_count < 63:
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                    cells_count += 1
            else:
                for j in range(run_length):
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                    cells_count += 1
                if size == 0:
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                else:
                    value = reader.read_int(size)
                    # ac[block_index, cells_count, component] = value
                    # acs[0][i][cells_count] = value
                    ac.append(value)
                cells_count += 1
        acs.append(ac)
    dcs.append(dc)
    acss.append(acs)

    print(dcs[0][0])
    print(acss[0][0])
    
    C_blocks_count = reader.read_blocks_count()

    dc = []
    acs = []
    for i in range(C_blocks_count):
        dc_table = tables['dc_c'] 
        ac_table = tables['ac_c']

        category = reader.read_huffman_code(dc_table)
        # dcs[0][i] = reader.read_int(category)
        dc.append(reader.read_int(category))

        cells_count = 0
        ac = []

        # TODO: try to make reading AC coefficients better
        while cells_count < 63:
            run_length, size = reader.read_huffman_code(ac_table)

            if (run_length, size) == (0, 0):
                while cells_count < 63:
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                    cells_count += 1
            else:
                for j in range(run_length):
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                    cells_count += 1
                if size == 0:
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                else:
                    value = reader.read_int(size)
                    # ac[block_index, cells_count, component] = value
                    # acs[0][i][cells_count] = value
                    ac.append(value)
                cells_count += 1
        acs.append(ac)
    dcs.append(dc)
    acss.append(acs)

    dc = []
    acs = []
    for i in range(C_blocks_count):
        dc_table = tables['dc_c'] 
        ac_table = tables['ac_c']

        category = reader.read_huffman_code(dc_table)
        # dcs[0][i] = reader.read_int(category)
        dc.append(reader.read_int(category))

        cells_count = 0
        ac = []

        # TODO: try to make reading AC coefficients better
        while cells_count < 63:
            run_length, size = reader.read_huffman_code(ac_table)

            if (run_length, size) == (0, 0):
                while cells_count < 63:
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                    cells_count += 1
            else:
                for j in range(run_length):
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                    cells_count += 1
                if size == 0:
                    # ac[block_index, cells_count, component] = 0
                    # acs[0][i][cells_count] = 0
                    ac.append(0)
                else:
                    value = reader.read_int(size)
                    # ac[block_index, cells_count, component] = value
                    # acs[0][i][cells_count] = value
                    ac.append(value)
                cells_count += 1
        acs.append(ac)
    dcs.append(dc)
    acss.append(acs)

    print(len(dcs))
    print(len(dcs[0]))
    print(len(dcs[1]))
    print(len(dcs[2]))
    print(len(acs))
    print(len(acss[0]))
    print(len(acss[1]))
    print(len(acss[2]))

    return dcs,acss,Y_blocks_count,C_blocks_count,tables


QY=np.array([[16,11,10,16,24,40,51,61],
             [12,12,14,19,26,48,60,55],
             [14,13,16,24,40,57,69,56],
             [14,17,22,29,51,87,80,62],
             [18,22,37,56,68,109,103,77],
             [24,35,55,64,81,104,113,92],
             [49,64,78,87,103,121,120,101],
             [72,92,95,98,112,100,103,99]])

QC=np.array([[17,18,24,47,99,99,99,99],
             [18,21,26,66,99,99,99,99],
             [24,26,56,99,99,99,99,99],
             [47,66,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99]])

# 要求：1. 查阅资料，了解JPEG图片压缩流程，依照encode.py实现的压缩代码，编写相应的decode代码。
#      2. 调整量化表，观察不同量化表压缩后的解压图像差异，至少做4组，图像要有差异，outimg是当前量化表压缩后解压得到的图片
#      3. 实验报告记录解压后的图、压缩率和重构误差图像
#      4. 实验报告和代码打包提交到ftp，截至时间是5/13

if __name__ == "__main__":
    # step 1
    # 读取二进制文件并进行hafuman解码，还原成Z型数组
    # des是直流系数，acs是交流系数，Y_blocks_count是Y的块数，C_blocks_count是Cr和Cb的块数，tables可以不适用

    dcs, acs, Y_blocks_count, C_blocks_count, tables = read_image_file('encode.b')
    # step 2
    # 将Z型数组还原成 8 X 8 的块
    # 注意：dc系数解码后仍然是dcpm，需要转换成原有形式

    # step 3
    # 对每一块都进行逆量化和逆DCT变换

    # step 4
    # 计算重构误差




