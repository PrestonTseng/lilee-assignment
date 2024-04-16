import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(200), unique=False, nullable=False)

    def __init__(self, name):
        self.name = name

    def get_dict(self):
        return {"id": self.id, "name": self.name}
