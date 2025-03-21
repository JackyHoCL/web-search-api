from typing import Union
from fastapi import FastAPI
from crawler import craw
from web_search import search
import json
import asyncio

app = FastAPI()


@app.get("/craw")
async def craw_lihkg(query: str, max_results: int = 5):
    # result_json = lihkg.get_lihkg().to_json(orient='records')
    # return json.dumps(json.loads(result_json)).replace('"', '&quot;')\
    results = search(query, max_results)
    try:
      for result in results:
        result['content'] = await craw(result['href'])
    except Exception as e:
      print("Failed to craw: " + str(e))
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8788)