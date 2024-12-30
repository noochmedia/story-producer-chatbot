import os
from serpapi import GoogleSearch
from utils.logger import logger

class SearchService:
    def __init__(self):
        """Initialize the search service with API key"""
        self.api_key = os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SERPAPI_KEY not found in environment variables")

    def search(self, query, num_results=3):
        """Perform a web search and return results"""
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "num": num_results
            })
            
            results = search.get_dict()
            
            if "error" in results:
                logger.error(f"Search error: {results['error']}")
                return None
                
            if "organic_results" not in results:
                logger.warning("No organic results found")
                return []
                
            formatted_results = []
            for result in results["organic_results"][:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}")
            return None

    def format_results_for_gpt(self, results):
        """Format search results into a string for GPT context"""
        if not results:
            return "No search results found."
            
        formatted = "Here are the relevant search results:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   URL: {result['link']}\n"
            formatted += f"   {result['snippet']}\n\n"
        
        return formatted