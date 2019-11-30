import os
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch import nn

from _utils_torch import show_torch, show_batch_torch

from model import SinGAN


class Paint2Image(SinGAN):
    def __init__(self, naive_img, input, config, device):
        super().__init__(input, config, device)

        if np.max(naive_img) < 10:
            naive_img = naive_img * 255
        self.naive_img = naive_img / 127.5 - 1

        self.naive_pyramid = []
        for i in range(self.config['num_scale']):
            height_scaled = self.height_pyramid[i]
            width_scaled = self.width_pyramid[i]

            processed = cv2.resize(self.naive_img, (height_scaled, width_scaled))
            processed = torch.tensor(np.transpose(processed, [2, 0, 1])[np.newaxis])
            self.naive_pyramid.append(processed.to(self.device, torch.float))

    def generate_paint2image(self, init_scale):
        if init_scale == -1:
            init_scale = self.config['num_scale'] - 1
            
        self.paint2image_pyramid = []  # just for enjoy
        for scale in range(init_scale, self.config['num_scale']):
            generator = self.generator_pyramid[scale]
            noise_optimal = self.noise_optimal_pyramid[scale]
            sigma = self.sigma_pyramid[scale]

            if scale == init_scale:
                naive = self.naive_pyramid[init_scale]
                paint2image = generator(naive, noise_optimal * sigma)

            else:
                paint2image = nn.Upsample((self.width_pyramid[scale], self.height_pyramid[scale]))(paint2image)
                paint2image = generator(paint2image, noise_optimal * sigma)

            self.paint2image_pyramid.append(paint2image)
        return paint2image

    def sample_scales(self, save):
        os.makedirs(self.path_sample, exist_ok=True)

        self.eval_mode_all()
        with torch.no_grad():
            if not self.config['num_scale'] % 2:
                n_rows = 2
                n_cols = self.config['num_scale'] // 2
            else:
                n_rows, n_cols = None, None
                
            save_image = show_batch_torch(
                torch.cat([self.generate_paint2image(scale).clamp(-1, 1) for scale in range(self.config['num_scale'])]),
                padding=2, n_rows=n_rows, n_cols=n_cols, return_img=True
            )
            if save:
                save_name = os.path.join(self.path_sample, "sample_scales")
                plt.imsave(save_name, save_image)
        return save_image