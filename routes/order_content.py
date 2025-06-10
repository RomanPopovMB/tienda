from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from db.database import get_session
from models.order_content import OrderContent, OrderContentCreate
from crud.order_content import (
    create_order_content,
    get_order_contents,
    get_order_content_by_id,
    update_order_content,
    delete_order_content,
)
from auth.dependencies import require_role
from routes.auth import get_current_user_id

router = APIRouter()

@router.post("/", response_model = OrderContent)
def create(order_content: OrderContentCreate, session: Session = Depends(get_session), current_order_content: dict = Depends(require_role("admin"))):
    try:
        order_content_data = OrderContent(**order_content.model_dump())
        return create_order_content(session, order_content_data)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")

@router.get("/", response_model = list[OrderContent])
def read_all(session: Session = Depends(get_session), current_order_content: dict = Depends(require_role("admin"))):
    try:
        return get_order_contents(session)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")

@router.get("/{order_content_id}", response_model = OrderContent)
def read(order_content_id: int, session: Session = Depends(get_session), current_order_content: dict = Depends(require_role(["admin", "client"]))):
    order_content = get_order_content_by_id(session, order_content_id)
    if not order_content:
        raise HTTPException(status_code = 404, detail = f"OrderContent with ID {order_content_id} not found.")
    
    # If not admin, can't see order_contents if not an owner.
    current_user_id = get_current_user_id()
    if current_user_id == None:
        raise HTTPException(status_code = 403, detail = "There is no login information. Please log in.")
    if current_order_content.get("role") != "admin" and order_content.user_id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Insufficient permissions.")
    
    return order_content

@router.put("/{order_content_id}", response_model = OrderContent)
def update(
    order_content_id: int,
    order_content_data: dict = Body(
        ...,
        examples={
            "example": {
                "summary": "Update order_content example",
                "value": {
                    "name": "Updated order_content name",
                    "email": "updated_email@example.com"
                }
            }
        }
    ),
    session: Session = Depends(get_session),
    current_order_content: dict = Depends(require_role(["admin", "client"])),
):
    try:
        order_content = get_order_content_by_id(session, order_content_id)
        if not order_content:
            raise HTTPException(status_code = 404, detail = f"OrderContent with ID {order_content_id} not found.")
        
        # If not admin, can't change order_contents if not an owner.
        current_user_id = get_current_user_id()
        if current_user_id == None:
            raise HTTPException(status_code = 403, detail = "There is no login information. Please log in.")
        if current_order_content.get("role") != "admin" and order_content.user_id != current_user_id:
            raise HTTPException(status_code = 403, detail = "Insufficient permissions.")
        
        updated_order_content = update_order_content(session, order_content_id, order_content_data)
        if not updated_order_content:
            raise HTTPException(status_code = 404, detail = f"OrderContent with ID {order_content_id} not found.")
        return updated_order_content
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")

@router.delete("/{order_content_id}", response_model = OrderContent)
def delete(order_content_id: int, session: Session = Depends(get_session), current_order_content: dict = Depends(require_role(["admin", "client"]))):
    try:
        order_content = get_order_content_by_id(session, order_content_id)
        if not order_content:
            raise HTTPException(status_code = 404, detail = f"OrderContent with ID {order_content_id} not found.")
        
        # If not admin, can't see order_contents if not an owner.
        current_user_id = get_current_user_id()
        if current_user_id == None:
            raise HTTPException(status_code = 403, detail = "There is no login information. Please log in.")
        if current_order_content.get("role") != "admin" and order_content.user_id != current_user_id:
            raise HTTPException(status_code = 403, detail = "Insufficient permissions.")
        
        deleted_order_content = delete_order_content(session, order_content_id)
        if not deleted_order_content:
            raise HTTPException(status_code = 404, detail = f"OrderContent with ID {order_content_id} not found.")
        return deleted_order_content
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")