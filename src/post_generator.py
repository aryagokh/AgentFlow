from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, StreamingResponse, FileResponse, JSONResponse
from components.post_creator import create_post
from components.summary_generator import summary_generator
from components.seo_optimizer import seo_optimizer
from components.image_generator import generate_image_with_gemini
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI()

@app.post('/generate_post/')
async def generate_post(topic:str, platform:str, creativity_temperature:float = 0.7, image_gen_bool:bool = False):
    try:
        raw_post = create_post(topic, platform, creativity_temperature)
        print('Finished Generating Post')
        post_summary = summary_generator(role=f'{platform} post summary writer', content=raw_post)
        print('Finished Generating Summary')
        seo_optimized_post = seo_optimizer(platform, raw_post)
        print('Finished SEO Optimization')
        if image_gen_bool is False:
            return seo_optimized_post
        else:
            img_details = generate_image_with_gemini(content=post_summary)
            img_path = img_details['img_path']

            # image_stream = BytesIO(img_details["img_bytes"])
            # return StreamingResponse(image_stream, media_type="image/png")
            
            return {
            "post": seo_optimized_post,
            "image": FileResponse(img_path, media_type="image/png")
            }
    except Exception as e:
        print(e)
        return -1

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)