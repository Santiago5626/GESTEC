from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class PushSubscription(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String, unique=True, index=True)
    p256dh = Column(String)
    auth = Column(String)
    
    # Optional: Technician ID to optimizing polling
    technician_id = Column(String, nullable=True)

    user = relationship("User", back_populates="subscriptions")

# Add backref to User model dynamically to avoid circular imports if needed, 
# or assume user.py will remain simple.
