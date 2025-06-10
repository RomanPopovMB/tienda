from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from db.database import get_session
from models.order import Order, OrderCreate
from crud.order import (
    create_order,
    get_orders,
    get_order_by_id,
    update_order,
    delete_order,
)
from auth.dependencies import require_role
from routes.auth import get_current_user_id

router = APIRouter()

@router.post("/", response_model = Order)
def create(order: OrderCreate, session: Session = Depends(get_session), current_order: dict = Depends(require_role("admin"))):
    try:
        order_data = Order(**order.model_dump())
        return create_order(session, order_data)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")

@router.get("/", response_model = list[Order])
def read_all(session: Session = Depends(get_session), current_order: dict = Depends(require_role("admin"))):
    try:
        return get_orders(session)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")

@router.get("/{order_id}", response_model = Order)
def read(order_id: int, session: Session = Depends(get_session), current_order: dict = Depends(require_role(["admin", "client"]))):
    order = get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code = 404, detail = f"Order with ID {order_id} not found.")
    
    # If not admin, can't see orders if not an owner.
    current_user_id = get_current_user_id()
    if current_user_id == None:
        raise HTTPException(status_code = 403, detail = "There is no login information. Please log in.")
    if current_order.get("role") != "admin" and order.user_id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Insufficient permissions.")
    
    return order

@router.put("/{order_id}", response_model = Order)
def update(
    order_id: int,
    order_data: dict = Body(
        ...,
        examples={
            "example": {
                "summary": "Update order example",
                "value": {
                    "name": "Updated order name",
                    "email": "updated_email@example.com"
                }
            }
        }
    ),
    session: Session = Depends(get_session),
    current_order: dict = Depends(require_role(["admin", "client"])),
):
    try:
        order = get_order_by_id(session, order_id)
        if not order:
            raise HTTPException(status_code = 404, detail = f"Order with ID {order_id} not found.")
        
        # If not admin, can't change orders if not an owner.
        current_user_id = get_current_user_id()
        if current_user_id == None:
            raise HTTPException(status_code = 403, detail = "There is no login information. Please log in.")
        if current_order.get("role") != "admin" and order.user_id != current_user_id:
            raise HTTPException(status_code = 403, detail = "Insufficient permissions.")
        
        updated_order = update_order(session, order_id, order_data)
        if not updated_order:
            raise HTTPException(status_code = 404, detail = f"Order with ID {order_id} not found.")
        return updated_order
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")

@router.delete("/{order_id}", response_model = Order)
def delete(order_id: int, session: Session = Depends(get_session), current_order: dict = Depends(require_role(["admin", "client"]))):
    try:
        order = get_order_by_id(session, order_id)
        if not order:
            raise HTTPException(status_code = 404, detail = f"Order with ID {order_id} not found.")
        
        # If not admin, can't see orders if not an owner.
        current_user_id = get_current_user_id()
        if current_user_id == None:
            raise HTTPException(status_code = 403, detail = "There is no login information. Please log in.")
        if current_order.get("role") != "admin" and order.user_id != current_user_id:
            raise HTTPException(status_code = 403, detail = "Insufficient permissions.")
        
        deleted_order = delete_order(session, order_id)
        if not deleted_order:
            raise HTTPException(status_code = 404, detail = f"Order with ID {order_id} not found.")
        return deleted_order
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Unexpected error: {str(e)}")