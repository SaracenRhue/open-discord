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
