from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from searcher.Searcher import Searcher
from pybars import Compiler
from problem import problem

from os import environ

compiler = Compiler()

app = FastAPI()

hbs = open('./template.hbs').read()

# Add any special helpers
def _list(this, options):
  result = [u'<div class="flex flex-col justify-center items-center">']
  for nrow, row in enumerate(problem):
    result.append(u'<div class="flex flex-row">')
    for ncol, val in enumerate(row):
      itemId = 'i-'+str(nrow)+'-'+str(ncol)
      if val == 0: result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-gray-600 flex justify-center items-center" > </div>')
      if val == 1: result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-slate-100 flex justify-center items-center" > </div>')
      if val == 'i': result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-blue-400 flex justify-center items-center" > </div>')
      if val == 'g': result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-red-400 flex justify-center items-center" > </div>')
    result.append(u'</div>')  
  result.append(u'</div>')
  return result
helpers = {'list': _list}

template = compiler.compile(hbs)
html = template({"api": environ.get("API_URL", "ws://localhost:8000")},helpers=helpers)


@app.get("/")
async def get():
  return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  agent = Searcher(problem)

  await websocket.accept()

  async def sendIteration(response):
    await websocket.send_json(response)

  while True:
    data = await websocket.receive_json()
    print(data)
    if data['action'] == 'start':
      if data['alg'] == None or data['alg'] == 'depth': await agent.startDepth(sendIteration, data["delay"])
      elif data['alg'] == 'best': await agent.startBest(sendIteration, data["delay"])
      elif data['alg'] == 'breadth': await agent.startBreadth(sendIteration, data["delay"])