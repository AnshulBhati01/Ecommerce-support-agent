from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.database import Order, OrderItem, Customer
from app.utils.logger import logger
import uuid

class OrderManager:
    """Manage order operations"""
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve order by ID"""
        try:
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if not order:
                return None
            
            items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
            
            return {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "order_date": order.order_date,
                "status": order.status,
                "total_amount": order.total_amount,
                "shipping_address": order.shipping_address,
                "tracking_number": order.tracking_number,
                "expected_delivery": order.expected_delivery,
                "items": [
                    {
                        "product_name": item.product_name,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                        "total_price": item.total_price
                    }
                    for item in items
                ]
            }
        except Exception as e:
            logger.error(f"Error retrieving order {order_id}: {e}")
            return None
    
    @staticmethod
    def get_customer_orders(db: Session, customer_id: str, limit: int = 10) -> list:
        """Get all orders for a customer"""
        try:
            orders = db.query(Order).filter(
                Order.customer_id == customer_id
            ).order_by(Order.order_date.desc()).limit(limit).all()
            
            return [
                {
                    "order_id": order.order_id,
                    "status": order.status,
                    "total_amount": order.total_amount,
                    "order_date": order.order_date,
                    "tracking_number": order.tracking_number
                }
                for order in orders
            ]
        except Exception as e:
            logger.error(f"Error retrieving orders for customer {customer_id}: {e}")
            return []
    
    @staticmethod
    def update_order_status(db: Session, order_id: str, new_status: str) -> bool:
        """Update order status"""
        try:
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if order:
                order.status = new_status
                db.commit()
                logger.info(f"Order {order_id} status updated to {new_status}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating order {order_id}: {e}")
            db.rollback()
            return False
    
    @staticmethod
    def create_order(db: Session, customer_id: str, total_amount: float, items: list) -> Optional[str]:
        """Create a new order"""
        try:
            order_id = str(uuid.uuid4())
            order = Order(
                order_id=order_id,
                customer_id=customer_id,
                status="pending",
                total_amount=total_amount
            )
            db.add(order)
            
            # Add order items
            for item in items:
                order_item = OrderItem(
                    item_id=str(uuid.uuid4()),
                    order_id=order_id,
                    product_id=item.get("product_id"),
                    product_name=item.get("product_name"),
                    quantity=item.get("quantity", 1),
                    unit_price=item.get("unit_price", 0),
                    total_price=item.get("quantity", 1) * item.get("unit_price", 0)
                )
                db.add(order_item)
            
            db.commit()
            logger.info(f"Order {order_id} created successfully")
            return order_id
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            db.rollback()
            return None
