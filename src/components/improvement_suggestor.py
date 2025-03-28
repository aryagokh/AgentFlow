import os
from openai import OpenAI
from dotenv import load_dotenv
from config import get_secret
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=get_secret('OPENROUTER_API_KEY')
)


def create_improvement_suggestion_prompt(background, issues, additional_info=None, whom=None):
    system_prompt = f'''
    You are an expert in improvement suggestions of all the content.
    You can use your available knowledge or search on internet, you decide.
    Respond with strictly only resolvements of the issues.
    No filler words and headers.
    Format for all issues and resolution should be:
    * Issue:
    * Resolution:
    '''
    user_prompt = f'''
    This is some background for your prerequisite knowledge:
    {background}

    These are the issues which are the input:
    {issues}
    '''
    if additional_info is not None:
        if whom=='system':
            system_prompt = system_prompt + '\n' + f'''{additional_info}'''
        elif whom=='user':
            user_prompt = user_prompt + '\n' + f'''Also, consider this additional information \n{additional_info} '''
        else:
            print('No additional info given to anyone. Stop if you believe its a mistake!!')
    return system_prompt, user_prompt


def suggest_improvements(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model='deepseek/deepseek-r1-zero:free',
            messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return -1
    
def improvement_suggestions(background, issues, additional_info=None, whom=None):
    system_prompt, user_prompt = create_improvement_suggestion_prompt(background, issues, additional_info, whom)
    improvements_needed = suggest_improvements(system_prompt, user_prompt)
    return improvements_needed


if __name__ == '__main__':
    issues = f'''
    *   Deployment process took longer than expected.
    *   Documentation provided for integration was incomplete.
    *   Pricing was on the higher side.
    *   Some model predictions were difficult to interpret.
    '''

    background = 'AI ML Big Data Company'
    system_prompt, user_prompt = create_improvement_suggestion_prompt(background, issues)
    print(suggest_improvements(system_prompt, user_prompt))

