import google.genai as genai 
from google.genai.types import Tool, GoogleSearch, GenerateContentConfig
from dotenv import load_dotenv
import os
import json
from config import get_secret
load_dotenv()

def create_price_generation_prompt(item, additional_info=None, website=None):
    prompt = f'''
    You are an expert in scraping the internet and providing **real time retail prices**.
    Everytime you get request for any item's price, you use google search tool provided and return the price of the item.

    Please don't use any filler words. Also, no **highlighted headings and texts**.
    Return strictly only
    ```json
    {{
    food_item_1 : price,
    ...
    }}```

    Here is the item:
    {item}
    '''
    if website is not None:
        prompt = prompt + f'''
        Try to search the required rel time information here:
        {website}    
        '''
    if additional_info is not None:
        prompt = prompt + f'''
        Here is some additional things to consider:
        {additional_info}
        '''

    return prompt


def generate_price(item, addtional_info=None, website=None):
    try:
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
        google_search_tool = Tool(
            google_search=GoogleSearch()
        )
        response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=create_price_generation_prompt(item, 
                                                additional_info=addtional_info,
                                                website=website),
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=['TEXT']
        )
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return -1

def parse_price_output(price_pseudo_json):
    try:
        parsed_json = json.loads(price_pseudo_json.strip("```json"))
        parsed_response = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        parsed_list_response = json.loads(parsed_response)
        return parsed_list_response
    except Exception as e:
        print(e)
        return -1
    

def generate_realtime_parsed_price(item, additional_info=None, website=None):
    retries, max_retries = 0, 5
    if retries < max_retries:
        try:
           pseudo_json = generate_price(item, additional_info, website)
           parsed_prices = parse_price_output(pseudo_json)
           return parsed_prices
        except Exception as e:
            retries = retries + 1
            print(f"Exception occurred : {e}. Retrying...")
    else:
        print(f"Max retries exceeded. Please try after sometime...")


# if __name__ == '__main__':
#     response = generate_realtime_parsed_price(
#         item=['Society Tea (100g)', 'Cow Milk (1/2 litre)', 'Sugar (100g)', 'Ginger(100g)'],
#         additional_info='The information should be based on Mumbai.',
#         website=['zepto.com', 'blinkit.com']
#     )
#     print("Response : ", response)