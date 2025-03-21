from duckduckgo_search import DDGS

def search(keyword: str, max_results=5):
  return DDGS().text(keyword, max_results=max_results)
