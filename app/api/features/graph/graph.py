from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv, find_dotenv

from app.api.features.crew import EmailGeneratorCrew
from app.api.schemas.schema import EmailBodySchema, FinalEmailSchema, GraphState, PersonalizedEmailSchema, SuggestionsSchema

load_dotenv(find_dotenv())

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def generate_email_body(state):
    json_parser = JsonOutputParser(pydantic_object=EmailBodySchema)
    messages = [
        SystemMessage(content="You are an assistant that generates professional email responses based on the content of the original email and the provided context."),
        HumanMessage(content=f"""Please generate an email response based on the following original email and context:

    Original Email Context:
    {state['message_context']}

    Subject:
    {state['subject']}

    Ensure your response addresses the key points of the original email and follows the format and requirements specified in {json_parser.get_format_instructions()}.""")
    ]
    result = llm.invoke(messages)
    parsed_result = json_parser.parse(result.content)
    print(f"STEP 1 - GENERATE EMAIL RESPONSE BODY: {parsed_result}")
    return {"email_body": parsed_result}

def personalize_email(state):
    json_parser = JsonOutputParser(pydantic_object=PersonalizedEmailSchema)
    messages = [
        SystemMessage(content="You are an assistant that personalizes content based on the email's body."),
        HumanMessage(content=f"""Please personalize the following email's body:

    Email Response Body:
    {state['email_body']}

    Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.""")
    ]
    result = llm.invoke(messages)
    parsed_result = json_parser.parse(result.content)
    print(f"STEP 2 - PERSONALIZE EMAIL RESPONSE: {parsed_result}")
    return {"personalized_email": parsed_result}

def suggest_improvements(state):
    json_parser = JsonOutputParser(pydantic_object=SuggestionsSchema)
    messages = [
        SystemMessage(content="You are an assistant that suggests improvements to email response content."),
        HumanMessage(content=f"""Please provide suggestions to improve the following email response:

    Email Response Content:
    {state['personalized_email']}

    Ensure your suggestions focus on enhancing clarity, tone, and overall effectiveness. Follow the format and requirements specified in {json_parser.get_format_instructions()}.""")
    ]
    result = llm.invoke(messages)
    parsed_result = json_parser.parse(result.content)
    print(f"STEP 3 - SUGGEST IMPROVEMENTS TO EMAIL RESPONSE: {parsed_result}")
    return {"suggestions": parsed_result}

def finalize_email(state):
    json_parser = JsonOutputParser(pydantic_object=FinalEmailSchema)
    messages = [
        SystemMessage(content="You are an assistant that finalizes email responses by applying suggestions for improvement."),
        HumanMessage(content=f"""Please apply the following suggestions to improve the email response content:

    Email Response Content:
    {state['personalized_email']}

    Suggestions:
    {state['suggestions']}

    Ensure your response follows the format and requirements specified in {json_parser.get_format_instructions()}.""")
    ]
    result = llm.invoke(messages)
    parsed_result = json_parser.parse(result.content)
    print(f"STEP 4 - FINALIZE EMAIL RESPONSE: {parsed_result}")
    return {"final_email": parsed_result}

workflow = StateGraph(GraphState)

workflow.add_node("generate_email_body", generate_email_body)
workflow.add_node("personalize_email", personalize_email)
workflow.add_node("suggest_improvements", suggest_improvements)
workflow.add_node("finalize_email", finalize_email)
workflow.add_node("generate_improved_email", EmailGeneratorCrew().kickoff)

workflow.set_entry_point("generate_email_body")
workflow.add_edge("generate_email_body", "personalize_email")
workflow.add_edge("personalize_email", "suggest_improvements")
workflow.add_edge("suggest_improvements", "finalize_email")
workflow.add_edge("finalize_email", "generate_improved_email")
workflow.add_edge("generate_improved_email", END)

def return_graph():
    app = workflow.compile()
    return app