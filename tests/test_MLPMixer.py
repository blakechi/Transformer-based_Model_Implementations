import gc
import torch
from .utils import *

# === Import model-related objects ===
from comvex.mlpmixer import MLPMixerConfig, MLPMixerWithLinearClassifier

# === Instantiate your Model ===
# - For specializations
specializations = [attr for attr in dir(MLPMixerConfig) if attr.startswith("MLPMixer")]

# === Settings ===
# - Required:
input_shape = (1, 3, 224, 224)
expected_shape = (1, 10)
# - Optional:
kwargs = {}
kwargs['num_classes'] = 10

# === Test Cases ===
# Default test for specializations
def test_forward():
    for spec in specializations:
        print(spec)
        config = getattr(MLPMixerConfig, spec)(**kwargs)
        model = MLPMixerWithLinearClassifier(config)
        model.eval()

        x = torch.randn(input_shape)
        out = model(x)

        assert_output_shape_wrong(out, expected_shape)
        assert_output_has_nan(out)
    
        del model
        gc.collect()