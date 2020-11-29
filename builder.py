import glob
import os

import numpy as np
import struct
import imageio
import zlib


class SensorMaker:

    def __init__(self, number):
        self.versoin = 4
        self.sensor_name = 'StructureSensor'
        self.strlen = len(self.sensor_name)

        self.intrinsic_color = np.loadtxt("C:\\scanData\\result\\data\\intrinsic\\intrinsic_color.txt")
        self.extrinsic_color = np.loadtxt("C:\\scanData\\result\\data\\intrinsic\\extrinsic_color.txt")
        self.intrinsic_depth = np.loadtxt("C:\\scanData\\result\\data\\intrinsic\\intrinsic_depth.txt")
        self.extrinsic_depth = np.loadtxt("C:\\scanData\\result\\data\\intrinsic\\extrinsic_depth.txt")

        self.color_compression_type = 2
        self.depth_compression_type = 1

        self.color_width = 640
        self.color_height = 480
        self.depth_width = 640
        self.depth_height = 480
        self.depth_shift = 900.0

        self.num_frames = number

        # for image_lead
        self.pose_f = np.identity(4).astype("float32")
        self.pose_data = 0
        self.color_data = 0
        self.color_len = 0
        self.color_ts = struct.pack('Q', 0)
        self.depth_f = 0
        self.depth_data = 0
        self.depth_len = 0
        self.depth_ts = struct.pack('Q', 0)

        # for bytes list
        self.bytes = list()
        self.bytes.append(self.pose_data)
        self.bytes.append(self.color_ts)
        self.bytes.append(self.depth_ts)
        self.bytes.append(self.color_len)
        self.bytes.append(self.depth_len)
        self.bytes.append(self.color_data)
        self.bytes.append(self.depth_data)

        self.make()

    def image_load(self, c, d):
        bytes = []
        color_data = open(c, 'rb').read()
        depth_f = imageio.imread(d)

        depth_data = zlib.compress(depth_f)  # data compress

        pose_data = struct.pack('f' * 16, self.pose_f[0][0], self.pose_f[0][1], self.pose_f[0][2],
                                     self.pose_f[0][3], self.pose_f[1][0], self.pose_f[1][1], self.pose_f[1][2],
                                     self.pose_f[1][3], self.pose_f[2][0], self.pose_f[2][1], self.pose_f[2][2],
                                     self.pose_f[2][3], self.pose_f[3][0], self.pose_f[3][1], self.pose_f[3][2],
                                     self.pose_f[3][3])
        color_len = struct.pack('Q', len(color_data))
        depth_len = struct.pack('Q', len(depth_data))
        bytes.append(pose_data)
        bytes.append(self.color_ts)
        bytes.append(self.depth_ts)
        bytes.append(color_len)
        bytes.append(depth_len)
        bytes.append(color_data)
        bytes.append(depth_data)

        return bytes

    def make(self):
        with open('.\\apt0.sens', 'wb') as f:
            f.write(struct.pack('I', self.versoin))
            f.write(struct.pack('Q', self.strlen))
            f.write(struct.pack('c' * self.strlen, 'S', 't', 'r', 'u', 'c', 't', 'u', 'r', 'e', 'S', 'e', 'n', 's', 'o',
                                'r'))
            f.write(struct.pack('f' * 16, self.intrinsic_color[0][0], self.intrinsic_color[0][1],
                                self.intrinsic_color[0][2], self.intrinsic_color[0][3], self.intrinsic_color[1][0],
                                self.intrinsic_color[1][1], self.intrinsic_color[1][2], self.intrinsic_color[1][3],
                                self.intrinsic_color[2][0], self.intrinsic_color[2][1], self.intrinsic_color[2][2],
                                self.intrinsic_color[2][3], self.intrinsic_color[3][0], self.intrinsic_color[3][1],
                                self.intrinsic_color[3][2], self.intrinsic_color[3][3]))
            f.write(struct.pack('f' * 16, self.extrinsic_color[0][0], self.extrinsic_color[0][1],
                                self.extrinsic_color[0][2], self.extrinsic_color[0][3], self.extrinsic_color[1][0],
                                self.extrinsic_color[1][1], self.extrinsic_color[1][2], self.extrinsic_color[1][3],
                                self.extrinsic_color[2][0], self.extrinsic_color[2][1], self.extrinsic_color[2][2],
                                self.extrinsic_color[2][3], self.extrinsic_color[3][0], self.extrinsic_color[3][1],
                                self.extrinsic_color[3][2], self.extrinsic_color[3][3]))
            f.write(struct.pack('f' * 16, self.intrinsic_depth[0][0], self.intrinsic_depth[0][1],
                                self.intrinsic_depth[0][2], self.intrinsic_depth[0][3], self.intrinsic_depth[1][0],
                                self.intrinsic_depth[1][1], self.intrinsic_depth[1][2], self.intrinsic_depth[1][3],
                                self.intrinsic_depth[2][0], self.intrinsic_depth[2][1], self.intrinsic_depth[2][2],
                                self.intrinsic_depth[2][3], self.intrinsic_depth[3][0], self.intrinsic_depth[3][1],
                                self.intrinsic_depth[3][2], self.intrinsic_depth[3][3]))
            f.write(struct.pack('f' * 16, self.extrinsic_depth[0][0], self.extrinsic_depth[0][1],
                                self.extrinsic_depth[0][2], self.extrinsic_depth[0][3], self.extrinsic_depth[1][0],
                                self.extrinsic_depth[1][1], self.extrinsic_depth[1][2], self.extrinsic_depth[1][3],
                                self.extrinsic_depth[2][0], self.extrinsic_depth[2][1], self.extrinsic_depth[2][2],
                                self.extrinsic_depth[2][3], self.extrinsic_depth[3][0], self.extrinsic_depth[3][1],
                                self.extrinsic_depth[3][2], self.extrinsic_depth[3][3]))
            f.write(struct.pack('i', self.color_compression_type))
            f.write(struct.pack('i', self.depth_compression_type))
            f.write(struct.pack('I', self.color_width))
            f.write(struct.pack('I', self.color_height))
            f.write(struct.pack('I', self.depth_width))
            f.write(struct.pack('I', self.depth_height))
            f.write(struct.pack('f', self.depth_shift))
            f.write(struct.pack('Q', self.num_frames))
            # for i in range(self.num_frames):
            dlist = sorted(glob.glob('C:\\scanData\\result\\data\\depth\\*'))
            clist = sorted(glob.glob('C:\\scanData\\result\\data\\color\\*'))
            for d, c in zip(dlist, clist):
                items = self.image_load(c, d)
                for item in items:
                    f.write(item)


SensorMaker(1338)

