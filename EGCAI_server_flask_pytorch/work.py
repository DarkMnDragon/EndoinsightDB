"""
Created on 16/Jul/2023

@author: Liaorl
"""

import os
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from nn.networks import *
from nn.utils import *
import torch
from torchvision import transforms
from PIL import Image

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = 'cpu'

# 假设 device 是您想要使用的设备（CPU 或 GPU）
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 初始化一个新的 ResnetGenerator 实例
model = ResnetGenerator(input_nc=3, output_nc=3, ngf=64, n_blocks=4, img_size=256, light=False).to(device)

# 从 params.pt 文件中加载整个状态字典
params = torch.load('./nn/params.pt', map_location=device)

# 使用 genA2B 部分来初始化新的 ResnetGenerator 实例
if 'genA2B' in params:
    model.load_state_dict(params['genA2B'])
else:
    raise KeyError("'genA2B' not found in the loaded parameters.")

# 创建一个只包含 genA2B 部分的新字典
params_genA2B_only = {'genA2B': model.state_dict()}

# 保存这个新字典为一个新的 .pt 文件
torch.save(params_genA2B_only, 'genA2B_only.pt')
