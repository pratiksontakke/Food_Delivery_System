from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from api.models.customer import Customer
from api.schemas.customer import CustomerCreate, CustomerUpdate

async def create_customer(db: AsyncSession, data: CustomerCreate) -> Customer:
    customer = Customer(**data.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Customer]:
    result = await db.execute(select(Customer).offset(skip).limit(limit))
    return result.scalars().all()

async def get_customer(db: AsyncSession, customer_id: int) -> Optional[Customer]:
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    return result.scalar_one_or_none()
    
async def get_customer_by_email(db: AsyncSession, email: str) -> Optional[Customer]:
    result = await db.execute(select(Customer).where(Customer.email == email))
    return result.scalar_one_or_none()

async def update_customer(db: AsyncSession, customer: Customer, data: CustomerUpdate) -> Customer:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    await db.commit()
    await db.refresh(customer)
    return customer

async def delete_customer(db: AsyncSession, customer: Customer):
    await db.delete(customer)
    await db.commit()