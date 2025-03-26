import os
import google.genai as genai
from google.genai import types
from io import BytesIO
import base64
from gradio_client import Client
from dotenv import load_dotenv
from PIL import Image
import matplotlib.pyplot as plt
import random
from config import get_secret
load_dotenv()

def construct_image_gen_prompt(content, additional_info=None):
    client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
    gemini_prompt = f'''
    You are an expert prompt engineer who generates prompt based on the content and scenario.
    The following is the content based on which you have to make an optimized prompt which will be passed to an image generation model:
    {content}

    Keep these things in mind while generating the prompt:
    1. Be specific, even if it takes time.
    2. Be to the point.
    3. Only generate prompt. No filler text or boiler starting text from your side. Just pure prompt.
    4. No highlighted headers or messages.
    '''
    if additional_info is not None:
        gemini_prompt = gemini_prompt + '\n' + f'''Also consider this additional information : {additional_info}'''\
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=gemini_prompt
        )
        # print(response)
        # print(response.candidates[0].content.parts[0].text)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return -1


def generate_image_with_diffusionAI(content, additional_info=None):
    try:
        prompt = construct_image_gen_prompt(content, additional_info)
        # print(prompt)
        
        client = Client("stabilityai/stable-diffusion")
        result = client.predict(
                prompt=prompt,
                negative='No/minimal text should be present in the image.',
                scale=9,
                api_name="/infer"
        )
        return result
    except Exception as e:
        print(e)
        return -1
    
    
def generate_image_with_gemini(content, additional_info=None):
    try:
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))

        contents = (construct_image_gen_prompt(content, additional_info))
        # print("CONTENT", contents)

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=contents,
            config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
            )
        )
        # print("RESPONSE", response)
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))

                img_bytes_io = BytesIO()
                image.save(img_bytes_io, format="PNG")
                img_bytes = img_bytes_io.getvalue()

                img_save_path = f'gemini-native-image-{random.random()}.png'
                image.save(img_save_path)
                image.show()
                return {"img_path": img_save_path,
                        "img_bytes":img_bytes}
    except Exception as e:
        print(e)
        return -1
    

# if __name__ == '__main__':
#     generate_image_with_gemini(
#         content="Eiffel tower next to Taj Mahal and there's Christ the Redeemer in the middle.",
#         additional_info='The sun is setting.'
#     )



