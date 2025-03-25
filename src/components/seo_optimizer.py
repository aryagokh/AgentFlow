from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentExecutor, AgentType
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
load_dotenv()

tavily_search = TavilySearchResults(max_results=5)
tools = [
    Tool(name="TavilySearch", func=tavily_search.run, description="SEO Optimizer")
]

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    max_retries=3,
    api_key=os.getenv('GEMINI_API_KEY')
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  
    verbose=True,
    # agent_kwargs={"prompt": create_tavily_agent_prompt(raw_content)},
    handle_parsing_errors=True
)

def seo_optimizer(platform, post):

    seo_prompt = f'''
    Use Tavily to search for the best SEO optimization techniques specific to [domain]. Analyze the top strategies, keyword usage, and content patterns from the search results. Based on these insights, identify key SEO elements (keywords, structure, engagement tactics) that improve {platform} visibility.

    Now, take my previous {platform} post:
    {post}

    Rewrite and transform it into an SEO-optimized {platform} post by applying the learned strategies. Ensure it remains engaging, professional, and aligned with {platform}'s algorithm best practices.

    Finally, only return the post and not any extra words.
    '''

    refined_response = agent.run(seo_prompt)
    return refined_response

if __name__ == '__main__':
    dummy_post = f'''
    **AI & ML: Level Up Your Mechanical Engineering Career! 🚀**
    Hey #MechanicalEngineers! 👋 Ready to future-proof your skills?

    AI and Machine Learning aren't just buzzwords anymore; they're revolutionizing manufacturing, design, and maintenance. Think:

    *   **Predictive Maintenance:** Imagine algorithms that foresee equipment failures *before* they happen, saving time and $$$ 💰.
    *   **Generative Design:** AI creating optimal designs we haven't even thought of yet – lighter, stronger, better! 🤯
    *   **Automated Quality Control:** Catching defects with superhuman accuracy, ensuring top-notch products. ✅

    **Why should YOU care?**

    Knowing AI/ML will make you a *highly* sought-after engineer. It's about:

    *   **Boosting Efficiency:** Streamlining processes, reducing waste. ♻️
    *   **Driving Innovation:** Creating cutting-edge solutions. ✨
    *   **Increasing Earning Potential:** Skills that are in demand pay BIG. 🤑

    **Get started now:**

    *   Explore online courses on platforms like Coursera or Udacity.
    *   Start small – look for AI/ML applications within your current projects.
    *   Join online communities and connect with experts!

    #AIinManufacturing #MachineLearning #MechanicalEngineering #FutureofWork #EngineeringJobs #TechSkills #Innovation #CareerDevelopment
    '''
    optimized_post = seo_optimizer('LinkedIn', dummy_post)
    print(optimized_post)