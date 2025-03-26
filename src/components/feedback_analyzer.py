import pandas as pd
import google.genai as genai
from dotenv import load_dotenv
import os
from config import get_secret
load_dotenv()

client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))

def file_to_text(file_path, review_column_name='reviews'):
    if str(file_path).endswith('csv'):
        data = pd.read_csv(file_path)
    elif str(file_path).endswith('xlsx'):
        data = pd.read_excel(file_path)
    elif str(file_path).endswith('json'):
        data = pd.read_json(file_path)
    else:
        print('Invalid file type. Please upload csv, excel or json files!!!')
        return -1
    collective_response = ''
    for i in range(len(data)):
        collective_response = collective_response + '\n' + data[review_column_name][i]
    return collective_response

def create_analysing_prompt(data, additional_info=None):
    prompt = f'''
    You are an expert in analyzing the reviews.
    Given any set of reviews, you analyze them perfectly.
    You list the issues listed inside the reviews in the form of bullet points.
    If no issue is present, just tell 'No issues'
    Do not add filler text. Just output the bullet points if issue is present.
    And strictly do not add **headers like this**.

    This is the data on which you have to perform analyzing process:
    {data}
    '''
    if additional_info is not None:
        prompt = prompt + '\n' + f'Here is some additional information about the same : {additional_info}'

    return prompt

def analyze_feedback(file_path, review_column_name='reviews', additional_info=None):
    try:
        collective_response = file_to_text(file_path)
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=create_analysing_prompt(collective_response)
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return -1


# if __name__ == '__main__':
#     print(analyze_feedback(
#         file_path='data/raw/documents/Issues_DS.xlsx'
#     ))