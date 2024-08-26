import aiohttp
from config import *



async def txt2img(prompt, ratio=SD_RATIO, steps=SD_STEPS, cfg_scale=SD_CFG_SCALE, batch_count=SD_BATCH_COUNT):
    payload = {
        "prompt": prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "batch_count": batch_count,
        "width": ratio[0],
        "height": ratio[1]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{SD_URL}/sdapi/v1/txt2img', json=payload) as resp:
            data = await resp.json()
            return data['images']
