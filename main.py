from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from searcher.Searcher import Searcher
from pybars import Compiler
compiler = Compiler()

app = FastAPI()
problem = [
  ['i', 0 , 0 ,'g'],
  [ 1 , 1 , 0 , 1 ],
  [ 0 , 1 , 1 , 1 ],
  [ 0 , 0 , 0 , 1 ],
]
problem12= [
    ['i', 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1],
    [0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 'g']
]
app = FastAPI()

hbs = open('./template.hbs').read()
# Add any special helpers
def _list(this, options):
  result = [u'<div class="flex flex-col justify-center items-center">']
  for nrow, row in enumerate(problem):
    result.append(u'<div class="flex flex-row">')
    for ncol, val in enumerate(row):
      itemId = 'i-'+str(nrow)+'-'+str(ncol)
      if val == 0: result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-gray-500" > </div>')
      if val == 1: result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-slate-100" > </div>')
      if val == 'i': result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-blue-400" > </div>')
      if val == 'g': result.append(u'<div id='+itemId+ ' class="w-4 h-4 bg-red-400" > </div>')
    result.append(u'</div>')  
  result.append(u'</div>')
  return result
helpers = {'list': _list}

template = compiler.compile(hbs)
html = template({},helpers=helpers)


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
    if(data['action'] == 'start'):
      await agent.startDepth(sendIteration, data["delay"])