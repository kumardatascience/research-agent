from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from research_agent.utils.config import settings
from research_agent.agent.tools import search_web, scrape_page


class ResearchState(TypedDict):
    topic:str
    questions:list[str]
    search_results:list[dict]
    scraped_content:list[str]
    iterations:int
    final_report:str
    model_choice: str


def get_llm(model_choice:str='gemini'):
    if model_choice == 'groq':
        return ChatGroq(model=settings.model_name_groq,
                        groq_api_key = settings.groq_api_key)   

    return ChatGoogleGenerativeAI(model=settings.model_name_gemini,
                                  google_api_key=settings.gemini_api_key) 


# Node 1, no tools required in this just thinking

def plan_research(state: ResearchState) -> dict:
    topic = state["topic"]
    llm = get_llm(state["model_choice"])
    
    prompt = f"""You are a research planner.
Break this topic into exactly 4 specific research questions.
Topic: {topic}

Return ONLY a numbered list like this:
1. First question
2. Second question
3. Third question
4. Fourth question

No intro text. No explanations. Just 4 numbered questions."""

    response = llm.invoke(prompt)
    response_text = response.content
    
    lines = [line.strip() for line in response_text.split("\n") if line.strip()]
    questions = []
    for line in lines:
        if ". " in line:
            question = line.split(". ", 1)[1]
            questions.append(question)
    
    return {
        "questions": questions
    }

# NODE 2: search_web_node
# → uses: search_web() tool from tools.py
# → tool does the actual Tavily search
# → node organizes results into state

def search_web_node(state: ResearchState) -> dict:
    questions = state["questions"]
    all_results = []

    for question in questions:
        results = search_web(question)
        for result in results:
            result["question"] = question
        all_results.extend(results)

    return {
        "search_results": all_results
    }

# NODE 3: scrape_pages_node

# → uses: scrape_page() tool from tools.py
# → tool does the actual scraping
# → node organizes content into state

def scrape_pages_node(state: ResearchState) -> dict:
    search_results = state["search_results"]
    scraped_content = []

    for result in search_results[:8]:
        url = result["url"]
        content = scrape_page(url)

        if not content.startswith("Could not scrape"):
            scraped_content.append(
                f"SOURCE: {result['title']}\n"
                f"URL: {url}\n"
                f"CONTENT:\n{content}"
            )

    return {
        "scraped_content": scraped_content,
        "iterations": state["iterations"] + 1
    }

# NODE 4: synthesize
# → uses: Gemini/Groq LLM directly
# → no tool needed, just thinking

def synthesize(state: ResearchState) -> dict:
    topic = state["topic"]
    scraped_content = state["scraped_content"]
    llm = get_llm(state["model_choice"])

    combined = "\n\n---\n\n".join(scraped_content)

    if len(combined) > 12000:
        combined = combined[:12000]

    prompt = f"""You are a professional research analyst.
Based on the sources below write a comprehensive research report.

TOPIC: {topic}

SOURCES:
{combined}

Write the report in this EXACT structure:

## Executive Summary
(3-4 sentences summarizing key findings)

## Key Findings
(5 bullet points of most important discoveries)

## Detailed Analysis
(3 paragraphs analyzing the topic in depth)

## Source Comparison
(How do sources agree or disagree?)

## Conclusion
(2-3 sentences wrapping up)

Be specific. Cite sources. Be professional."""

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }

def should_continue(state: ResearchState) -> str:
    scraped_count = len(state["scraped_content"])
    iterations = state["iterations"]

    if scraped_count >= 6 or iterations >= settings.max_iterations:
        return "done"
    return "continue"

def build_graph(model_choice: str = "gemini"):
    graph = StateGraph(ResearchState)

    graph.add_node("plan_research", plan_research)
    graph.add_node("search_web", search_web_node)
    graph.add_node("scrape_pages", scrape_pages_node)
    graph.add_node("synthesize", synthesize)

    graph.set_entry_point("plan_research")

    graph.add_edge("plan_research", "search_web")
    graph.add_edge("search_web", "scrape_pages")

    graph.add_conditional_edges(
        "scrape_pages",
        should_continue,
        {
            "continue": "search_web",
            "done": "synthesize"
        }
    ) 
    graph.add_edge("synthesize", END)

    return graph.compile()
