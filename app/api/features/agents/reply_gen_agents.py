from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import SerpAPIWrapper
from crewai.tools import tool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@tool
def wikipedia_search(query: str) -> str:
    """Search for information on Wikipedia."""
    api_wrapper = WikipediaAPIWrapper()
    return WikipediaQueryRun(api_wrapper=api_wrapper).run(query)

@tool
def serp_api_search(query: str) -> str:
    """Look up information using SerpAPI."""
    serp_api = SerpAPIWrapper()
    return serp_api.run(query)

@tool
def tavily_search(query: str) -> str:
    """Perform a search with Tavily, including answers and raw content."""
    tavily = TavilySearchResults(
        max_results=5,
        include_answer=True,
        include_raw_content=True
    )
    return tavily.run(query)

class CustomAgents:
    def __init__(self):
        self.OpenAIGPT4Mini = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4o", temperature=0)
        self.tools = [wikipedia_search,
                    serp_api_search,
                    tavily_search
        ]

    def content_agent(self):
        # Agent 1: Email Content Generator
        return Agent(
            role="Email Content Generator",
            backstory=dedent("""
                You are an expert at crafting engaging and appropriate email content based on provided context.
            """),
            goal=dedent("""
                Generate a draft email based on the given message context, ensuring the content aligns with the intended purpose.
            """),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4Mini,
        )

    def review_agent(self):
        # Agent 2: Email Reviewer
        return Agent(
            role="Email Reviewer",
            backstory=dedent("""
                You specialize in reviewing email content for tone, grammar, and clarity.
            """),
            goal=dedent("""
                Review the draft email, make improvements to grammar and tone, and ensure clarity.
            """),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def personalization_agent(self):
        # Agent 3: Personalization Specialist
        return Agent(
            role="Personalization Specialist",
            backstory=dedent("""
                You excel at adding personalized touches to emails based on recipient information.
            """),
            goal=dedent("""
                Personalize the email by adding relevant details about the recipient to make the message more engaging.
            """),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4Mini,
        )

    def output_agent(self):
        # Agent 4: Output Compiler
        return Agent(
            role="Output Compiler",
            backstory=dedent("""
                You are responsible for compiling the final email output, ensuring all elements are cohesive.
            """),
            goal=dedent("""
                Compile the final version of the email, incorporating all revisions and personalizations.
            """),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )