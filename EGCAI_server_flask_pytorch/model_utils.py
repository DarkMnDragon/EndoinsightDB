"""
Created on 5/Dec/2023

@author: Liaorl
"""

import torch
from torchvision import transforms
from PIL import Image
from nn.networks import ResnetGenerator
import os

class ImagePredictor:
    def __init__(self, model_path, device='cpu'):
        self.model = self.load_model(model_path, device)
        self.transform = self.get_transform()
        self.device = device

    @staticmethod
    def load_model(path_to_model, device):
        model = ResnetGenerator(input_nc=3, output_nc=3, ngf=64, n_blocks=4, img_size=256, light=True).to(device)
        params = torch.load(path_to_model, map_location=device)
        model.load_state_dict(params['genA2B'])
        model.eval()
        return model

    @staticmethod
    def get_transform():
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
        ])

    def preprocess(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0)
        return image.to(self.device)

    def postprocess(self, tensor):
        tensor = tensor.detach().cpu().squeeze(0)
        tensor = 0.5 * (tensor + 1.0)
        tensor = tensor.clamp(0.0, 1.0)
        return tensor.permute(1, 2, 0).numpy()

    def predict(self, image_path):
        image = self.preprocess(image_path)
        with torch.no_grad():
            output = self.model(image)
            output = output[0]
        return self.postprocess(output)
