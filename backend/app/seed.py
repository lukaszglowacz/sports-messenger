"""
Database seed script.

Creates initial test data:
- 3 users (2 athletes, 1 manager)
- 1 ACCEPTED contact exchange (Athlete 2 <-> Manager)
- Sample messages demonstrating different scenarios
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import User, UserType, ContactExchange, ContactExchangeStatus, Message


def seed_database(db: Session):
    """
    Seed database with test data.
    
    Creates scenario matching requirements:
    1. Athlete 1 <-> Athlete 2: Can message (no exchange needed)
    2. Athlete 2 <-> Manager: ACCEPTED exchange (can message with limits)
    3. Athlete 1 <-> Manager: No exchange (cannot message yet)
    
    Args:
        db: Database session
    """
    print("🌱 Seeding database...")

    # Check if already seeded
    existing_users = db.query(User).count()
    if existing_users > 0:
        print("⚠️  Database already contains data. Skipping seed.")
        return

    # Create users
    users = [
        User(
            id=1,
            name="Zawodnik 1",
            email="zawodnik1@test.com",
            type=UserType.ATHLETE,
            created_at=datetime.utcnow() - timedelta(days=30)
        ),
        User(
            id=2,
            name="Zawodnik 2",
            email="zawodnik2@test.com",
            type=UserType.ATHLETE,
            created_at=datetime.utcnow() - timedelta(days=25)
        ),
        User(
            id=3,
            name="Manager",
            email="manager@test.com",
            type=UserType.OFFICIAL,
            created_at=datetime.utcnow() - timedelta(days=20)
        ),
    ]

    print(f"👥 Creating {len(users)} users...")
    for user in users:
        db.add(user)
    db.commit()

    # Create contact exchanges
    exchanges = [
        # Athlete 2 and Manager have ACCEPTED exchange
        ContactExchange(
            id=1,
            athlete_id=2,
            official_id=3,
            status=ContactExchangeStatus.ACCEPTED,
            initiated_by=2,  # Athlete 2 initiated
            created_at=datetime.utcnow() - timedelta(days=7),
            responded_at=datetime.utcnow() - timedelta(days=6)
        ),
    ]

    print(f"🤝 Creating {len(exchanges)} contact exchanges...")
    for exchange in exchanges:
        db.add(exchange)
    db.commit()

    # Create sample messages
    messages = [
        # Athlete 1 <-> Athlete 2 (can message without exchange)
        Message(
            sender_id=1,
            recipient_id=2,
            content="Cześć! Idziesz dziś na trening?",
            created_at=datetime.utcnow() - timedelta(hours=4),
            read=True
        ),
        Message(
            sender_id=2,
            recipient_id=1,
            content="Tak! O 17:00 😊",
            created_at=datetime.utcnow() - timedelta(hours=3),
            read=True
        ),
        Message(
            sender_id=1,
            recipient_id=2,
            content="Super, do zobaczenia!",
            created_at=datetime.utcnow() - timedelta(hours=2),
            read=False
        ),
        
        # Athlete 2 <-> Manager (have ACCEPTED exchange)
        Message(
            sender_id=2,
            recipient_id=3,
            content="Dzień dobry, czy mogę prosić o konsultację?",
            created_at=datetime.utcnow() - timedelta(hours=1),
            read=True
        ),
        Message(
            sender_id=3,
            recipient_id=2,
            content="Oczywiście! Zapraszam jutro o 10:00",
            created_at=datetime.utcnow() - timedelta(minutes=45),
            read=False
        ),
    ]

    print(f"💬 Creating {len(messages)} sample messages...")
    for message in messages:
        db.add(message)
    db.commit()

    print("✅ Database seeded successfully!")
    print("\n📊 Created:")
    print(f"   - {len(users)} users")
    print(f"   - {len(exchanges)} contact exchanges")
    print(f"   - {len(messages)} messages")
    print("\n🧪 Test scenarios:")
    print("   1. Zawodnik 1 ↔ Zawodnik 2: Can message (no exchange needed)")
    print("   2. Zawodnik 2 ↔ Manager: ACCEPTED exchange (can message, limit 5/day)")
    print("   3. Zawodnik 1 ↔ Manager: No exchange (must send request first)")
