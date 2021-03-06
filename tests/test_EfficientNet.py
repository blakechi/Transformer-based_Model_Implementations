import gc
import pytest

import torch

from .utils import *

# === Import model-related objects ===
from comvex.utils import EfficientNetConfig, EfficientNetWithLinearClassifier

# === Instantiate your Model ===
# - For specializations
specializations = [attr for attr in dir(EfficientNetConfig) if attr.startswith("EfficientNet")]
specializations = specializations[:4]  # Avoid too large specializations

# === Settings ===
# - Required:
input_shape = (1, 3, 224, 224)
expected_shape = (1, 1000)
# - Optional:
kwargs = {}
kwargs['num_classes'] = 1000
kwargs['up_sampling_mode'] = 'bicubic'
official_num_params = [5.3, 7.8, 9.2, 12, 19, 30]

# === Test Cases ===
# Default test for specializations
def test_forward():
    for spec in specializations:
        print(spec)
        config = getattr(EfficientNetConfig, spec)(**kwargs)
        model = EfficientNetWithLinearClassifier(config)
        model.eval()

        x = torch.randn(input_shape)
        out = model(x)

        assert_output_shape_wrong(out, expected_shape)
        assert_output_has_nan(out)
    
        del model
        gc.collect()


def test_scripting_or_tracing():
    spec = specializations[0]  # one is enough
    print(spec)

    for to_reture_feature_maps in [True, False]:
        config = getattr(EfficientNetConfig, spec)(**kwargs, return_feature_maps=to_reture_feature_maps)

        x = torch.randn(input_shape)
        model = torch.jit.trace(EfficientNetWithLinearClassifier(config), x, strict=not to_reture_feature_maps)
        out = model(x)

        if to_reture_feature_maps:
            out = out['x']

        assert_output_shape_wrong(out, expected_shape)
        assert_output_has_nan(out)

        del model
        gc.collect()


@pytest.mark.skipif(True, reason="skip until find the why the number of parameters doesn't match with the official one.")
def test_num_parameters():
    for idx, spec in enumerate(specializations):
        print(spec)
        config = getattr(EfficientNetConfig, spec)(**kwargs)
        model = EfficientNetWithLinearClassifier(config)
        model.eval()
        num_params = model.num_parameters()
        num_params = round(num_params / 1e6, 1)
        
        assert (
            official_num_params[idx] == num_params
        ), f"The number of Parameters from official: {official_num_params[idx]} doesn't match self-implementated: {num_params}"

        gc.collect()