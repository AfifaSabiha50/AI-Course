from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool # <-- Changed import for the decorator
from datetime import datetime

# --- 1. Custom Save Tool (using @tool decorator) ---
@tool
def save_tool(data: str) -> str:
    """
    Saves structured research data to a text file. Use this at the end 
    of the research process after summarizing the findings.
    The input MUST be the final summary text and sources.
    """
    filename = "research_output.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# The variable name is the function name, which is also the tool name

# --- 2. Web Search Tool ---
# The DuckDuckGoSearchRun class acts as a tool directly. 
# Explicitly name it for clarity in the agent's thought process.
search_tool = DuckDuckGoSearchRun(
    name="web_search", 
    description="Search the web for current, real-time, or general information."
)

# --- 3. Wikipedia Tool ---
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(
    api_wrapper=api_wrapper, 
    name="wikipedia_lookup",
    description="Provides summary information from Wikipedia on broad, encyclopedic topics."
)