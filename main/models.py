import typing as t
import datetime
from typing import List, Dict, Any
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(
    model_class=Base,
    # engine_options={"echo": True}
)

if t.TYPE_CHECKING:

    class Model(Base):
        pass

else:
    Model = db.Model


class Client(Model):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    credit_card: Mapped[str] = mapped_column(String(50), nullable=True)
    car_number: Mapped[str] = mapped_column(String(10), nullable=True)
    parking: Mapped[List["Parking"]] = relationship(
        secondary="client_parking", back_populates="client"
    )

    def __repr__(self):
        return (
            f"Client(id={self.id}, name={self.name}, "
            f"surname={self.surname}, credit_card={self.credit_card}, car_number={self.car_number})"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(Model):
    __tablename__ = "parking"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    opened: Mapped[bool] = mapped_column(nullable=True, default=True)
    count_places: Mapped[int] = mapped_column(nullable=False, default=10)
    count_available_places: Mapped[int] = mapped_column(nullable=False, default=10)
    client: Mapped[List["Client"]] = relationship(
        secondary="client_parking", back_populates="parking"
    )

    def __repr__(self):
        return (
            f"Parking(id={self.id}, address={self.address}, "
            f"opened={self.opened}, count_places={self.count_places}, "
            f"count_available_places={self.count_available_places})"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(Model):
    __tablename__ = "client_parking"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=True)
    parking_id: Mapped[int] = mapped_column(ForeignKey("parking.id"), nullable=True)
    time_in: Mapped[datetime.datetime] = mapped_column(nullable=True)
    time_out: Mapped[datetime.datetime] = mapped_column(nullable=True)
    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    def __repr__(self):
        return (
            f"ClientParking(id={self.id}, client_id={self.client_id}, "
            f"parking_id={self.parking_id}, time_in={self.time_in}, time_out={self.time_out})"
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
