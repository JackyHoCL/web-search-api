from typing import Union
from fastapi import FastAPI
from crawler import craw
from web_search import search
import json
import asyncio
import requests

app = FastAPI()


@app.get("/search")
async def search_controller(query: str, max_results: int = 10):
    # result_json = lihkg.get_lihkg().to_json(orient='records')
    # return json.dumps(json.loads(result_json)).replace('"', '&quot;')\
    results = search(query, max_results)
    try:
      for result in results:
        result['content'] = await craw(result['href'])
    except Exception as e:
      print("Failed to craw: " + str(e))
    return results

@app.get("/index")
async def index_controller(query: str, max_results: int = 5):
    # result_json = lihkg.get_lihkg().to_json(orient='records')
    # return json.dumps(json.loads(result_json)).replace('"', '&quot;')\
    results = search(query, max_results)
    try:
      for result in results:
        result['content'] = await craw(result['href'])
    except Exception as e:
      print("Failed to craw: " + str(e))
    
    body = {
      'name': result['title'],
      'content': result['content']
    }
    headers={'Content-Type': 'application/json'}
    index_result = requests.post('http://localhost:8088/upload/text', json=body, headers=headers)
    return index_result.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8788)