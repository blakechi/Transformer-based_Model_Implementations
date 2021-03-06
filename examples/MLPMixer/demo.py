import os
import sys
sys.path.insert(0, os.getcwd())

import torch

from comvex.mlpmixer import MLPMixerConfig, MLPMixerWithLinearClassifier


if __name__ == "__main__":
    
    mlp_mixer_config = MLPMixerConfig.MLPMixer_B_16(1000)

    mlp_mixer = MLPMixerWithLinearClassifier(mlp_mixer_config)
    print(mlp_mixer)

    x = torch.randn(1, 3, 224, 224)

    print("Input Shape:\n", x.shape)
    print("Output Shape:\n", mlp_mixer(x).shape)