from config import get_secret
import google.genai as genai
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()

def make_img_describer_prompt(additional_info=None):
    prompt = f'''
    Descibe what is in this image.
    If there is text any text in image, only return that text.

    If there is no text, return what does the image describe.
    Avoid startings. Just start with the direct details.
    '''
    if additional_info is not None:
        prompt = prompt + "\n" + f'''Also consider this : {additional_info}'''
    
    return prompt


def scrape_image(image_path, additional_info=None):
    try:
        prompt = make_img_describer_prompt(additional_info)
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[Image.open(image_path), prompt]
        )

        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return -1


if __name__ == '__main__':
    print(
        scrape_image('data/raw/images/image_with_text.png')
    )