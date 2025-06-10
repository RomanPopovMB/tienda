from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from db.database import get_session
from utils.api_client import fetch_catalog, fetch_catalog_dict
from auth.dependencies import require_role

router = APIRouter()

@router.get("/", response_model = dict)
async def read_all(session: Session = Depends(get_session), current_user: dict = Depends(require_role(["admin", "client"]))):
    try:
        return await fetch_catalog_dict()
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error obtaining catalog: {str(e)}")


@router.get("/{page},{amount}", response_model = [])
async def read_all(page: int, amount: int, session: Session = Depends(get_session), current_user: dict = Depends(require_role(["admin", "client"]))):
    try:
        if page < 1:
            raise HTTPException(status_code = 400, detail = f"Page should be 1 or more.")
        if amount < 1:
            raise HTTPException(status_code = 400, detail = f"Amount should be 1 or more.")
        catalog = await fetch_catalog()
        index = 0
        result = []
        for product in catalog.products:
            # (page - 1) * amount), with amount 5 and page 1, this results in 0.
            # (page * amount - 1), with amount 5 and page 1, this results in 4.
            # (page - 1) * amount), with amount 5 and page 2, this results in 5.
            # (page * amount - 1), with amount 5 and page 2, this results in 9.
            if index >= ((page - 1) * amount) and index <= (page * amount - 1):
                result.append(product)
            index += 1
        return result
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error obtaining catalog: {str(e)}")