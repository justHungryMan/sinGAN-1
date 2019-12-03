import os
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch import nn

from chanye._utils_torch import reshape_batch_torch
from chanye._visualizer import preprocess
from utils import normalize_image
from sinGAN import SinGAN


class Editing(SinGAN):
    def __init__(self, config, dataset_path):
        super().__init__(config, dataset_path)

        naive_img = plt.imread(os.path.join(dataset_path, config['path_naive_data']))
        self.naive_img = normalize_image(naive_img)

        self.naive_pyramid = []
        for i in range(self.num_scale):
            height_scaled = self.height_pyramid[i]
            width_scaled = self.width_pyramid[i]

            processed = cv2.resize(self.naive_img, (height_scaled, width_scaled))
            processed = torch.tensor(np.transpose(processed, [2, 0, 1])[np.newaxis])
            self.naive_pyramid.append(processed.to(self.device, torch.float))

    def generate_editing(self, init_scale):
        if init_scale == -1:
            init_scale = self.num_scale - 1

        self.editing_pyramid = []  # just for enjoy
        for scale in range(init_scale, self.num_scale):
            generator = self.generator_pyramid[scale]
            noise_optimal = self.noise_optimal_pyramid[scale]
            sigma = self.sigma_pyramid[scale]

            if scale == init_scale:
                naive = self.naive_pyramid[init_scale]
                editing = generator(naive, noise_optimal * sigma)

            else:
                editing = nn.Upsample((self.width_pyramid[scale], self.height_pyramid[scale]))(editing)
                editing = generator(editing, noise_optimal * sigma)

            self.editing_pyramid.append(editing)
        return editing

    def test_samples(self, save):
        os.makedirs(self.path_sample, exist_ok=True)

        self.eval_mode_all()
        with torch.no_grad():
            if not self.num_scale % 2:
                n_rows = 2
                n_cols = self.num_scale // 2

                save_image, _, _ = reshape_batch_torch(
                    torch.cat(
                        [self.generate_editing(scale).clamp(-1, 1) for scale in range(self.num_scale)]),
                    padding=2, n_rows=n_rows, n_cols=n_cols
                )
            else:
                editings = [self.generate_editing(scale).clamp(-1, 1) for scale in range(self.num_scale)]
                editings += [torch.zeros_like(editings[0])]
                save_image, _, _ = reshape_batch_torch(
                    torch.cat(editings), n_rows=2, n_cols=-1
                )

            save_image = preprocess(save_image)  # preprocess image
            if save:
                save_name = os.path.join(self.path_sample, "editing")
                plt.imsave(save_name, save_image)
                print("Editing samples Saved:" + save_name)
        return save_image
