"""
Database initialization script
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.db.database import init_db, engine, AsyncSessionLocal
from backend.app.db.models import User, Product, Client
from passlib.context import CryptContext
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_initial_data():
    """
    Create initial data for testing
    """
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(select(User))
        if result.scalars().first():
            print("Initial data already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@startup.com",
            hashed_password=pwd_context.hash("admin123"),
            role="admin",
            department="Management"
        )
        session.add(admin_user)
        
        # Create sample rep user
        rep_user = User(
            email="rep@startup.com",
            hashed_password=pwd_context.hash("rep123"),
            role="rep",
            department="Sales"
        )
        session.add(rep_user)
        
        # Create sample products
        products = [
            Product(
                code="PROD001",
                name="Product A",
                category="Category 1",
                unit_price=1000.00,
                description="Premium product A"
            ),
            Product(
                code="PROD002",
                name="Product B",
                category="Category 2",
                unit_price=750.00,
                description="Standard product B"
            ),
            Product(
                code="PROD003",
                name="Product C",
                category="Category 1",
                unit_price=1500.00,
                description="Enterprise product C"
            )
        ]
        for product in products:
            session.add(product)
        
        # Create sample clients
        await session.flush()  # Get user IDs
        
        clients = [
            Client(
                name="Seoul Medical Center",
                type="hospital",
                address="Seoul, Gangnam-gu",
                owner_user_id=rep_user.id,
                tier="platinum",
                phone="02-1234-5678",
                email="contact@smc.kr"
            ),
            Client(
                name="Busan Clinic",
                type="clinic",
                address="Busan, Haeundae-gu",
                owner_user_id=rep_user.id,
                tier="gold",
                phone="051-1234-5678",
                email="info@busanclinic.kr"
            ),
            Client(
                name="Daegu Pharmacy",
                type="pharmacy",
                address="Daegu, Jung-gu",
                owner_user_id=rep_user.id,
                tier="silver",
                phone="053-1234-5678",
                email="pharmacy@daegu.kr"
            )
        ]
        for client in clients:
            session.add(client)
        
        await session.commit()
        print("Initial data created successfully")


async def main():
    """
    Main initialization function
    """
    print("Initializing database...")
    
    # Create tables
    await init_db()
    
    # Create initial data
    await create_initial_data()
    
    # Close connections
    await engine.dispose()
    
    print("Database initialization completed!")


if __name__ == "__main__":
    asyncio.run(main())