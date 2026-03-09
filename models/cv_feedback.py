from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class CVFeedback(Base):
    __tablename__ = "cv_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_link = Column(String, nullable=False)
    feedback = Column(Text, nullable=True)
    status = Column(String, default="loading", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cv_feedbacks")
