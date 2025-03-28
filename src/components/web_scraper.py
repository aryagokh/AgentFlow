from tavily import TavilyClient
import os
import google.genai as genai
from dotenv import load_dotenv
from config import get_secret
load_dotenv()


def create_stuctured_tavily_job_prompt(content):
    client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
    prompt = f'''
    You are an expert prompt engineer.
    You create structured prompt based on the content provided.
    This time, you have to extract keywords and location if present that will be passed to tavily search for real time serping.

    Extract keywords and location for the job/internship from the following content:
    {content}.

    You should return prompt in the following structure:
    You are an expert web scraper.
    You should search for jobs related to [keywords that you extract goes here...].
    Roles should be striclty based in [location that you extract goes here...].
    You should only provide real time information.
    '''
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt
    )
    return response.candidates[0].content.parts[0].text

def scrape_web(keywords):
    try:
        prompt = create_stuctured_tavily_job_prompt(keywords)
        tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
        response = tavily_client.search(prompt)
        return response
    except Exception as e:
        print(e)
        return -1


def tavily_search(content):
    try:
        tavily_prompt = create_stuctured_tavily_job_prompt(content)
        scrape_results = scrape_web(tavily_prompt)
        a = ''
        for result in scrape_results['results']:
            role = result.get('title', 'N/A')
            url = result.get('url', '#')
            description = result.get('content', 'No description available.')
            a = a + f"Title found : {role}\n"
            a = a + f"Website : {url}\n"
            a = a + f"Content Description : {description}\n"
            a = a + "\n\n"

        return a
    except Exception as e:
        print(e)
        return -1
    

# if __name__ == '__main__':
#     results = tavily_search(
#         content='''
# Arya GokhaleMumbai, Maharashtra, India
# 8999407351 #arya.gokhale1@gmail.com ïArya Gokhale §aryagokh aryagokh-portfolio
# Education
# Dwarkadas J. Sanghavi College of Engineering 2022 – 2026
# B.Tech in Mechanical Engineering (Honours in Robotics) 9.07 CGPA
# M.G.M. Junior College of Science 2021 – 2022
# HSC in Science with IT (4th Rank, MHTCET - 96.01 percentile) 88.00%
# Relevant Certifications and Coursework
# •Data Science and Machine Learning
# •Kaggle Certifications
# •Deep Learning and NLP
# •Data Analytics
# Projects
# Chat with PDFs |Python, Langchain, GROQ API, FAISS |Github
# •Developed an AI-powered chatbot enabling users to interact with PDFs using natural language queries.
# •Implemented efficient document retrieval and response generation for seamless user experience.
# •Deployed on Streamlit, enabling an interactive and user-friendly interface for querying PDFs.
# Product Feature Extraction |Pix2Struct, Python, PyTorch |Github
# •Implemented a script to efficiently automate the download of images, streamlining the dataset creation process.
# •Fine-tuned the pix2struct model for domain-specific measurement extraction, optimizing GPU memory usage throughout
# training.
# •Achieved a notable rank of 292 out of 70,000 participants (Amazon ML Challenge 2024).
# Image Captcha Detection |TROCR, PyTorch, Pandas |Github
# •Fine-tuned a model to solve Image Captcha Detection, leveraging advanced OCR techniques to interpret distorted and
# noisy captchas.
# •Achieved 1st place in the DataBlitz - Opencode’24 competition organized by GeekHaven, IIIT Allahabad.
# •Applied cutting-edge machine learning practices such as learning rate experimenting, showcasing creativity in model
# optimization and successfully adhering to strict no-API competition rules.
# Financial Sentiment Analysis |BERT, PyTorch, Streamlit |Github
# •Fine-tuned BERT for sentiment analysis in the financial domain, focusing on extracting insights from financial news,
# reports, and stock market data.
# •Achieved 80percent accuracy on the test set, demonstrating strong performance in classifying sentiments as positive, negative,
# or neutral.
# •Deployed the model on Huggingface Spaces, creating an interactive web interface for real-time sentiment analysis on
# financial texts.
# Fundamentals |Tensorflow, PyTorch, TorchVision, Scikit-Learn, Seaborn, Matplotlib, NumPy, Pandas, AutoML
# •Kaggle Playgrounds (Traditional ML) |Github
# •PyTorch and Computer Vision Fundamentals |Github
# •NLP Fundamentals and Transformers |Github
# Technical Skills
# Languages : Python, C/C++, SQL, HTML, CSS, Javascript
# Tools : VS Code, Google Colab, Kaggle, Jupyter
# Technologies/Frameworks : Streamlit, Tensorflow, Keras, PyTorch, Huggingface Transformers, Langchain
# Achievements
# •1st place in DataBlitz - Opencode’24 (GeekHaven - IIIT Allahabad)
# •Ranked 292nd out of 70,000+ participants in the Amazon ML Challenge 2024.
# •Secured 6th place in the DJS NSDC Machine Learning Competition (99.42percent F1 Score).
# •Achieved Kaggle Expert status.
#         '''
#     )
#     print(results)