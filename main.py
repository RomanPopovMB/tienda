import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from utils.api_client import fetch_catalog
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routes import auth, user, product, order, order_content
from utils.seeder import seed_data

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/auth/login")

templates = Jinja2Templates(directory="templates")
# To find files under the static folder.
app.mount("/static", StaticFiles(directory="static"), name="static")
# Including routes.
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(product.router, prefix="/api/product", tags=["Product"])
app.include_router(order.router, prefix="/api/order", tags=["Order"])
app.include_router(order_content.router, prefix="/api/order_content", tags=["Order content"])

# Try a simple query, and if there is an error, seed data.
try:
    user.test()
except Exception as e:
    seed_data()

@app.get("/", response_class=HTMLResponse)
async def catalog(request: Request):
    catalog = await fetch_catalog()
    return templates.TemplateResponse("catalog.html", {"request": request, "catalog": catalog})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
