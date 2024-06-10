import torch
from diffusers import DiffusionPipeline

from yt_diffuser.types.path import AppPath

class StableDiffusionXLEntity:
    """
    StableDiffusionXLPipeline を制御するエンティティ
    """

    def __init__(self, pipeline:DiffusionPipeline = None):
        """
        コンストラクタ

        Args:
            pipeline (DiffusionPipeline): パイプライン
        """
        self.pipeline = pipeline
    
    def load(self, model_name:str, revision:str, compile:bool) -> None:
        """
        モデルを読み込む
        """
        self.pipeline = DiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path=model_name,
            revision=revision,
            cache_dir=self.path.STORE_HF_MODEL_DIR,
            torch_dtype=torch.bfloat16,
            use_safetensors=True,
            local_files_only=True,
            variant="fp16",
        )

        #self.pipeline = YTStableFissuionXLPipeline(**pipeline.components)

        if torch.cuda.is_available():
            self.pipeline = self.pipeline.to("cuda")

        if compile:
            #compile_current_model(pipe)
            pass
    
    def seed_generator(self, input_seed:int = None) -> torch.Generator:
        """
        シードジェネレータを取得する

        Args:
            input_seed (str): シード
        """
        type = "cpu"
        if torch.cuda.is_available():
            type = "cuda"

        initial_seed = torch.Generator(type=type)

        if input_seed is None:
            seed = initial_seed.seed()
        else:
            seed = input_seed

        initial_seed.manual_seed(seed)