from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn


app = Starlette()


@app.route('/start', methods=['POST'])
async def start(request):
    return JSONResponse({'color': 'purple'})


@app.route('/move', methods=['POST'])
async def move(request):
    return JSONResponse({'move': 'down'})


@app.route('/end', methods=['POST'])
async def end(request):
    return JSONResponse({})


@app.route('/ping', methods=['POST'])
async def ping(request):
    return JSONResponse({})



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
