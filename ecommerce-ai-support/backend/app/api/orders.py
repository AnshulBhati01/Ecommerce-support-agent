from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import OrderResponse, OrderDetailResponse
from app.models.database import get_db, Order, OrderItem
from app.services.order_manager import OrderManager
from app.utils.logger import logger
import uuid

router = APIRouter()

@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(order_id: str, customer_id: str, db: Session = Depends(get_db)):
    """
    Get order details
    """
    try:
        # Verify order belongs to customer
        order = db.query(Order).filter(
            Order.order_id == order_id,
            Order.customer_id == customer_id
        ).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Get order items
        items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        
        return OrderDetailResponse(
            order_id=order.order_id,
            customer_id=order.customer_id,
            order_date=order.order_date,
            status=order.status,
            total_amount=order.total_amount,
            shipping_address=order.shipping_address,
            tracking_number=order.tracking_number,
            expected_delivery=order.expected_delivery,
            items=[
                {
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price
                }
                for item in items
            ]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving order {order_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customer/{customer_id}")
async def get_customer_orders(customer_id: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get all orders for a customer
    """
    try:
        orders = OrderManager.get_customer_orders(db, customer_id, limit)
        return {
            "customer_id": customer_id,
            "orders": orders,
            "count": len(orders)
        }
    
    except Exception as e:
        logger.error(f"Error retrieving customer orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_order(order_data: dict, db: Session = Depends(get_db)):
    """
    Create a new order
    """
    try:
        customer_id = order_data.get("customer_id")
        total_amount = order_data.get("total_amount", 0)
        items = order_data.get("items", [])
        
        if not customer_id:
            raise HTTPException(status_code=400, detail="customer_id is required")
        
        order_id = OrderManager.create_order(db, customer_id, total_amount, items)
        
        if not order_id:
            raise HTTPException(status_code=500, detail="Failed to create order")
        
        logger.info(f"Order created: {order_id}")
        
        return {
            "order_id": order_id,
            "customer_id": customer_id,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, new_status: str, db: Session = Depends(get_db)):
    """
    Update order status
    """
    try:
        success = OrderManager.update_order_status(db, order_id, new_status)
        
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {
            "order_id": order_id,
            "status": new_status,
            "message": "Order status updated successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
