import time

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def event_stream():
    pointer = 0
    while pointer < 3:
        yield "event: error\ndata: system has some error.\n\n"
        pointer += 1
        time.sleep(1)

    while pointer < 5:
        # 必須確保回傳資訊使用 data: 字段
        yield f"data: The time is {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        pointer += 1
        time.sleep(1)

    else:
        yield "event: end\ndata: The end\n\n"


templates = Jinja2Templates(directory="static")


@app.get("/sse")
async def sse():
    return StreamingResponse(event_stream(), media_type="text/event-stream")


# create a index html page
@app.get("/", response_class=HTMLResponse)
async def index():
    return templates.TemplateResponse(name="index.html", request={})
