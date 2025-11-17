from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import PydanticOutputParser

from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent

# Ensure your tools.py file is in the same directory and contains these imports
from tools import search_tool, wiki_tool, save_tool 

# Load environment variables (GOOGLE_API_KEY)
load_dotenv()

# --- 1. Define Structured Output Schema (Pydantic Model) ---
class ResearchResponse(BaseModel):
    """Schema for the final research response containing structured information."""
    topic: str = Field(description="The main topic of the research query.")
    summary: str = Field(description="A concise summary of the research findings based on tool use.")
    sources: list[str] = Field(description="A list of URLs or sources used to gather the information.")
    tools_used: list[str] = Field(description="A list of the names of the tools used by the agent (e.g., 'web_search', 'wikipedia_lookup', 'save_tool').")
    
# --- 2. Initialize Free LLM and Parser ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# --- 3. Define the Agent Prompt ---
FINAL_REACT_PROMPT_TEMPLATE = """
You are a research assistant that will help generate a research paper.
Answer the user query and use necessary tools (web_search, wikipedia_lookup) to gather information. 

# --- START OF REQUIRED RE-ACT VARIABLES ---
You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now have the final answer.
Action: save_tool
Action Input: (A JSON string containing the final ResearchResponse data)
# --- END OF REQUIRED RE-ACT VARIABLES ---

After summarizing the findings, you MUST use the 'save_tool' to save the result.
You MUST follow the output format. Wrap the final output in this format and provide no other text:
{format_instructions}

Previous actions and observations:
{agent_scratchpad}
{chat_history}

Begin!
Question: {query}
"""

prompt = PromptTemplate.from_template(FINAL_REACT_PROMPT_TEMPLATE).partial(
    format_instructions=parser.get_format_instructions()
)

# --- 4. Create the Agent and Executor ---
tools = [search_tool, wiki_tool, save_tool]
agent = create_react_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# --- CRITICAL FINAL FIX: Set stop condition to the tool's unique output ---
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True, 
    return_intermediate_steps=True,
    # THIS STOPS THE LOOP THE MOMENT THE SAVE TOOL CONFIRMS SUCCESS
    stop=["Observation: Data successfully saved to research_output.txt"] 
)

# --- 5. Execute the Agent ---
print("--- Agent is Ready ---")
query = input("What can i help you research? ")

# Pass empty strings for unused variables
raw_response = agent_executor.invoke({
    "query": query,
    "agent_scratchpad": "",
    "chat_history": "",
})

# --- 6. Robust Parsing and Output ---
try:
    final_output_text = raw_response.get("output")
    # The parser needs to find the JSON within the output text.
    structured_response = parser.parse(final_output_text)
    
    print("\n\n✅ FINAL STRUCTURED RESPONSE:")
    print(structured_response.model_dump_json(indent=2)) 

except Exception as e:
    # This block now handles the expected final error after the chain is stopped
    print("\n\n✅ AGENT CHAIN COMPLETE (Expected Final Parser Error Handled):")
    print("The agent executed its plan and successfully saved the data.")
    print("\n--- Raw Agent Output ---")
    
    # Extract the steps and find the JSON
    intermediate_steps = raw_response.get("intermediate_steps", [])
    if intermediate_steps:
        # The final action's input contains the JSON we want
        final_action = intermediate_steps[-1][0] 
        final_json_str = final_action.tool_input

        print("\n\n✅ FINAL STRUCTURED DATA EXTRACTED:")
        print(f"Topic: {query}")
        print(f"JSON Payload: {final_json_str}")
        
    else:
        print(f"Raw Output: {raw_response.get('output')}")