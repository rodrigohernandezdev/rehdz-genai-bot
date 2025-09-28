from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.tools.themoviedb import themoviedb_tools
from src.config import GEMINI_KEY

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GEMINI_KEY)

tools = themoviedb_tools

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == '__main__':
    result = agent_executor.invoke({"input": "What are the movie genres?"})
    print(result)
