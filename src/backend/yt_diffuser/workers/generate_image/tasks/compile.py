"""
モデルをコンパイルするタスク
"""
import torch
from diffusers import StableDiffusionXLPipeline

def compile_current_model (
        pipe:StableDiffusionXLPipeline,
    ) -> None:
    """
    現在のモデルをコンパイルする
    """

    torch._inductor.config.conv_1x1_as_mm = True
    torch._inductor.config.coordinate_descent_tuning = True
    torch._inductor.config.epilogue_fusion = False
    torch._inductor.config.coordinate_descent_check_all_directions = True
    #torch._inductor.config.force_fuse_int_mm_with_mul = True
    #torch._inductor.config.use_mixed_mm = True

    pipe.unet.to(memory_format=torch.channels_last)
    pipe.vae.to(memory_format=torch.channels_last)

    pipe.unet = torch.compile(pipe.unet, mode="max-autotune", fullgraph=True)
    # VAEのコンパイルはPyTorch2.2以降っぽい？ stableビルドだとエラーになる。
    #pipe.vae.decode = torch.compile(pipe.vae.decode, mode="max-autotune", fullgraph=True)
