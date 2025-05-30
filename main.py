import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from utils.api_client import fetch_catalog
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
# To find files under the static folder.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def catalog(request: Request):
    catalog = await fetch_catalog()
    return templates.TemplateResponse("catalog.html", {"request": request, "catalog": catalog})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
