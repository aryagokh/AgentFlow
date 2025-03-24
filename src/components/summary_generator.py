import google.genai as genai
import os
import time
from dotenv import load_dotenv
load_dotenv()

def construct_summary_prompt(role, content, additional_details=None):
    prompt = f'''
    You are an expert in summarizing the texts.

    Your role here is {role}.
    The task is to generate a summary based on the content.
    The content is as follows:
    {content}

    Please do not add any filler words and strictly **no headings**.
    Just relevant content.
    '''
    if additional_details is not None:
        prompt = prompt + '\n' + f'''Also, some additional details are as follows '\n' {additional_details}.'''

    return prompt


def summary_generator(role, content, additional_details=None):
    try:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        prompt = construct_summary_prompt(role, content, additional_details=None)
        retries, max_retries, base_wait = 0, 5, 5
        while retries < max_retries:
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash-lite', contents=prompt
                )
                return response.candidates[0].content.parts[0].text

            except genai.errors.ClientError as e:
                if "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = base_wait * (2 ** retries)
                    print(f"Quota exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
    except Exception as e:
        print(e)
        return -1
    
# if __name__ == '__main__':
#     sample_text = f'''
#     Two Minute Short Speech on APJ Abdul Kalam In English
#     Today, I am here to deliver a speech on Dr APJ Abdul Kalam. APJ Abdul Kalam was born to Jainulabdeen and Ashiamma on October 15, 1931. His father was a boat owner and his mother was a homemaker. His family's economic situation was not strong, so at an early age, he began helping his family financially.


#     He graduated in 1955 from the Madras Institute of Technology and graduated from St. Joseph's College, Tiruchirappalli, in Aerospace Engineering. He joined the Defense Research and Development Organization's (DRDO) Aeronautical Development Base as a Chief Scientist after his graduation. He won credit as Project Director-General for making India's first indigenous satellite (SLV III) rocket. It was his ultimate support that brought nuclear power to India. In July 1992, he was appointed Scientific Advisor to the Indian Ministry of Defence. As a national counsellor, he played a significant role in the world-famous nuclear tests at Pokhran II. In 1981, he was awarded the Padma Bhushan Award, in 1909 the Padma Vibhushan, and in 1997 the highest civilian award of India' Bharat Ratna 'for modernizing the defence technology of India and his outstanding contribution.


#     From July 25, 2002 - July 25, 2007, he served as President of India, becoming famous among Indians and receiving a lot of attention from Indian youth. He became popular as the People's President. Kalam worked as a professor, chancellor, and assistant at many institutions after leaving office. He experienced serious cardiac arrest on the evening of July 27, 2015, and fell unconscious and died 2 hours later.


#     In 1999, Kalam published his autobiography and a book called The Wings of Fire. He has written many other books that are useful to the people of every generation.


#     Long APJ Abdul Kalam Speech In English For Students
#     Greeting everyone. Today, I am here to deliver a speech on APJ Abdul Kalam. Dr APJ Abdul Kalam’s full name was Avul Pakir Zainuldeben Abdul Kalam, very few people know him by his full name as he was mostly addressed as ‘Missile Man of India’ and ‘People’s President’. He was born into a very poor family in Rameswaram on October 15, 1931. 

    

#     Since childhood, he enjoyed flying, and was equally curious to know how birds fly in the air? He was very intelligent and enjoyed reading, but his family did not have sufficient income for his school fees, so to support his education, he would wake up early in the morning and ride a bicycle 3 kilometres from home to collect newspapers and sell them.


#     He was admitted to St. Joseph's College, Tiruchirapalli, and later he went on to complete a degree in physics in 1954 and then studied at the Madras Institute of Technology and graduated in aeronautical engineering in 1955. Since his childhood, Dr Abdul Alam wanted to be a pilot but couldn’t make his dream come true. He learned from his mistakes and accomplished numerous achievements in his life. After completing his degree, Abdul Kalam entered the Defense Department of India. He has been one of the key figures in building the nuclear capabilities of India.

    

#     APJ Abdul Kalam was appointed to the Indian Ministry of Defense as a Technical Advisor in 1992, after which he served with DRDO and ISRO, the country's largest organization. Considered a national hero for successful nuclear tests in 1998, a second successful nuclear test was conducted in Pokhran the same year under his supervision, after which India was included in the list of nuclear-powered nations. Abdul Kalam has been active in all space programs and development programs in India as a scientist. For developing India's Agni missile, Kalam was called 'Missile Man.'Abdul Kalam made a special technological and scientific contribution, for which, along with Bharat Ratna, India's highest honour, he was awarded the Padma Bhushan, Padam Vibhushan, etc. He was also awarded an honorary doctorate by more than 30 universities in the world for the same. 

    

#     In 2002, he was elected President of India and was the country's first scientist and non-political president. He visited many countries during his tenure as President and led India's youth through his lectures and encouraged them to move forward.  ‘My vision for India’ was a Famous Speech of APJ Abdul Kalam delivered at IIT Hyderabad in 2011, and is to this day my favourite speech. His far-reaching thinking gave India's growth a fresh path and became the youth's inspiration. Dr Abdul Kalam died on July 27, 2015, from an apparent cardiac arrest while delivering a lecture at IIM Shillong at the age of 83. He spent his entire life in service and inspiration for the nation and the youth, and his death is also while addressing the youth. His death is a never-ending loss to the country.
#     '''
    
#     print(summary_generator('school student - summary generator', sample_text, additional_details=None))