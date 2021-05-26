from sqlalchemy import Column, Integer, String
from database import Base


class Text(Base):
    __tablename__ = "text"

    id = Column(Integer, primary_key=True, index=True)
    visit_counter = Column(Integer)
    text = Column(String)

    def __init__(self, id, visit_counter, text):
        self.id = id
        self.visit_counter = visit_counter
        self.text = text
