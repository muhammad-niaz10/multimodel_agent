from agents_prompts import search_agent, scrape_agent, writer_chain, critic_chain
from rich import print


def main(query):
    state_memory={}
    search_agent_instance = search_agent()
    search_results = search_agent_instance.invoke({"messages":[{"role":"user","content":f"search the query : {query} and keep the accurate links from tavily search on ai message format and return the links in a list format so that i can scrap the most relevant link for deeper content"}]})
    state_memory["search_results"]= search_results["messages"][-1].content
    

    print("\n"+"="*50+"\n")
    print("[bold blue]Reader Agent is scraping top sources.......:[/bold blue]")
    print("\n"+"="*50+"\n")

    scrap_agent_instance = scrape_agent()
    reader_results = scrap_agent_instance.invoke({
    "messages": [{
        "role": "user",
        "content": (
            f"Based on the following search results about '{query}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state_memory['search_results'][:800]}"
        )
    }]
})

    state_memory["reader_results"] = reader_results["messages"][-1].content
    
    print("\n" + "=" * 50 + "\n")
    print("[bold cyan]Writer Agent is generating final report.......[/bold cyan]")
    print("\n" + "=" * 50 + "\n")

    research_combined = (f"Search Results:\n{state_memory['search_results']}\n\n"
                         f"Reader Results:\n{state_memory['reader_results']}")

    state_memory["writer_results"] = writer_chain.invoke({
        "topic": query,
        "research": research_combined
    })

    print("\n" + "=" * 50 + "\n")
    print("[bold yellow]Critic Agent is evaluating and refining the report.......[/bold yellow]")
    print("\n" + "=" * 50 + "\n")

    
    state_memory["critic_results"] = critic_chain.invoke({
        "report": state_memory["writer_results"]
    })

    return state_memory

query=input("Enter your research topic: ")
state_memory = main(query)
print("[bold green]Search Results:[/bold green]")
print(state_memory["search_results"])
print("[bold green]Reader Results:[/bold green]")
print(state_memory["reader_results"])
print("[bold green]Writer Drafted Report:[/bold green]")
print(state_memory["writer_results"])
print("[bold green]Critic Final Evaluation:[/bold green]")
print(state_memory["critic_results"])