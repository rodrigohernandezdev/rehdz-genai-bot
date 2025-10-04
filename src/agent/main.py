import html
import re

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.tools.actual_date import date_tools
from src.agent.tools.themoviedb import themoviedb_tools
from src.agent.tools.weatherapi import weather_tools
from src.config import GEMINI_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=GEMINI_KEY,
    temperature=0.5
)

tools = themoviedb_tools + date_tools + weather_tools

system_instructions = """You are a helpful and friendly virtual assistant called Bot Assistant. Your purpose is to help users with:

**Your main capabilities:**
- Current weather information and forecasts
- Current date and time
- Movie search and film genres
- General conversation and assistance

**Important instructions:**
1. Always respond in Spanish in a clear, friendly, and natural way
2. Use the available tools when the user requests specific information
3. Maintain the context of previous conversations
4. If the user tells you their name or other personal information, remember it
5. Use a conversational and approachable tone
6. Format your responses clearly (use lists, separators when appropriate)
7. If you're not sure about something, honestly admit it
8. Be concise but complete in your responses
9. Format the output to look good in messaging (avoid problematic special characters)

Remember: You are a helpful assistant that can both chat casually and provide specific information using your tools."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_instructions),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
    max_execution_time=30,
    return_intermediate_steps=False
)

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)


def format_response_for_telegram(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', text)
    text = re.sub(r'##\s+(.*?)\n', r'*\1*\n', text)
    text = re.sub(r'#\s+(.*?)\n', r'*\1*\n', text)
    text = re.sub(r'-\s+(.*?)(?=\n|$)', r'• \1\n', text)
    if len(text) > 4000:
        text = text[:3997] + "..."
    return text.strip()


if __name__ == '__main__':
    result = agent_executor.invoke({"input": "What are the movie genres?"})
    print(result)
    result_date = agent_executor.invoke({"input": "what is the actual date?"})
    print(result_date)
