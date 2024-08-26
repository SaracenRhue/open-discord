import aiohttp
from config import *



async def txt2img(prompt):
    payload = {
        "prompt": prompt,
        "steps": SD_STEPS,
        "cfg_scale": SD_CFG_SCALE,
        "batch_count": SD_BATCH_COUNT,
        "batch_size": SD_BATCH_SIZE,
        "width": SD_RATIO[0],
        "height": SD_RATIO[1]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{SD_URL}/sdapi/v1/txt2img', json=payload) as resp:
            data = await resp.json()
            return data['images']

async def set_steps(steps: int):
    global SD_STEPS
    SD_STEPS = steps
    return f'Steps set to {SD_STEPS}'

async def set_cfg_scale(cfg_scale: float):
    global SD_CFG_SCALE
    SD_CFG_SCALE = cfg_scale
    return f'CFG Scale set to {SD_CFG_SCALE}'

async def set_batch_count(batch_count: int):
    global SD_BATCH_COUNT
    SD_BATCH_COUNT = batch_count
    return f'Batch Count set to {SD_BATCH_COUNT}'

async def set_batch_size(batch_size: int):
    global SD_BATCH_SIZE
    SD_BATCH_SIZE = batch_size
    return f'Batch Size set to {SD_BATCH_SIZE}'

async def set_width(width: int):
    global SD_RATIO
    SD_RATIO[0] = width
    return f'Width set to {SD_RATIO[0]}. Ratio set to {SD_RATIO[0]}:{SD_RATIO[1]}'

async def set_height(height: int):
    global SD_RATIO
    SD_RATIO[1] = height
    return f'Height set to {SD_RATIO[1]}. Ratio set to {SD_RATIO[0]}:{SD_RATIO[1]}'