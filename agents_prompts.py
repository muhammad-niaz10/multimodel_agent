from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from tools import search_results, get_webpage_content
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

api = os.getenv("MISTRAL_API_KEY")

llm = init_chat_model("mistral-small-latest", model_provider="mistralai", api_key=api, temperature=0.7)

def search_agent():
    return create_agent(
        model=llm,tools=[search_results])

def scrape_agent():
    return create_agent(
        model=llm,tools=[get_webpage_content])


writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured, and insightful reports."),
    ("human", """Write a detailed research report on the topic below using the gathered research.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual, and professional.""")
])



critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...""")
])


writer_chain = writer_prompt | llm | StrOutputParser()
critic_chain = critic_prompt | llm | StrOutputParser()