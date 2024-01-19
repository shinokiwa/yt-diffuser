from typing import Union, Dict
from os import PathLike
import json

from PIL import Image
from PIL.PngImagePlugin import PngInfo

def save_image(image:Image, filepath:Union[str, bytes, PathLike], model_name, seed, data:Dict):
    metadata = PngInfo()
    metadata.add_text('Title', 'AI generated image')
    metadata.add_text('Description', data.get('prompt', ''))
    metadata.add_text('Software', 'YuTori Diffuser')
    metadata.add_text('Source', model_name)
    comment = {
        "uc": data.get('negative_prompt', ''),
        "seed": seed,
    }
    if 'steps' in data:
        comment['steps'] = data.get('steps')

    if 'sampler' in data:
        comment['sampler'] = data.get('scheduler')

    if 'strength' in data:
        comment['strength'] = data.get('strength')

    if 'guidance_scale' in data:
        comment['scale'] = data.get('guidance_scale')

    metadata.add_text('Comment', json.dumps(comment))
    image.save(filepath, pnginfo=metadata)