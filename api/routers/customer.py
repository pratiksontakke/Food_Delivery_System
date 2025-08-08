from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.db.database import get_db
from api.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from api.crud import customer as crud

# Initialize the router with a prefix and tags for documentation
router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerRead, status_code=201)
async def create_customer(data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new customer.
    Checks if the email is already in use before creating.
    """
    db_customer = await crud.get_customer_by_email(db, email=data.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_customer(db, data)

@router.get("/", response_model=List[CustomerRead])
async def list_customers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all customers with pagination.
    """
    return await crud.get_customers(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single customer by their ID.
    """
    db_customer = await crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(customer_id: int, data: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a customer's details by their ID.
    """
    db_customer = await crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return await crud.update_customer(db, db_customer, data)

@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a customer by their ID.
    """
    db_customer = await crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    await crud.delete_customer(db, db_customer)
    
    # A 204 No Content response should not return a body
    return None