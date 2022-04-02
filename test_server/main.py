from aiohttp import web
import json


async def handle(request):
    response_obj = {"eh":str(request.query)}
    return web.Response(text=json.dumps(response_obj))

app = web.Application()
app.router.add_get("/offset", handle)
app.router.add_static("/", "./public")

web.run_app(app)