# app/database/models.py
from sqlalchemy import (
    Column, Integer, String, Date, Time, Text, ForeignKey, Table, DateTime
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import text
from datetime import datetime

Base = declarative_base()

# Многие-ко-многим: мастер ↔ услуга
masters_services = Table(
    "Masters_services",
    Base.metadata,
    Column("master_id", Integer, ForeignKey("Master.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("Service.id"), primary_key=True),
    Column("price", Integer, nullable=False)
)

class Client(Base):
    __tablename__ = "Client"

    id = Column(Integer, primary_key=True)  # ← исправлено
    name = Column(String(30), nullable=False)
    surname = Column(String(80))
    phone = Column(String(20), nullable=False)  # 10 маловато, лучше 20
    tg_id = Column(String(50), unique=True, index=True)  # tgId → tg_id

    appointments = relationship("Appointment", back_populates="client_rel")


class Master(Base):
    __tablename__ = "Master"

    id = Column(Integer, primary_key=True)  # ← исправлено
    name = Column(String(30), nullable=False)
    surname = Column(String(80), nullable=False)
    phone = Column(String(20), nullable=False)

    services = relationship("Service", secondary=masters_services, back_populates="masters")
    appointments = relationship("Appointment", back_populates="master_rel")


class Service(Base):
    __tablename__ = "Service"

    id = Column(Integer, primary_key=True)  # ← исправлено
    name = Column(String(255), nullable=False)
    duration = Column(Time, nullable=False)
    description = Column(Text)
    default_price = Column(Integer, nullable=False)

    masters = relationship("Master", secondary=masters_services, back_populates="services")
    appointments = relationship("Appointment", back_populates="service_rel")


class Appointment(Base):
    __tablename__ = "Appointment"

    id = Column(Integer, primary_key=True)  # ← исправлено
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    finish_time = Column(Time, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=text("NOW()"))

    client_id = Column(Integer, ForeignKey("Client.id"), nullable=False)
    master_id = Column(Integer, ForeignKey("Master.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("Service.id"), nullable=False)

    client_rel = relationship("Client", back_populates="appointments")
    master_rel = relationship("Master", back_populates="appointments")
    service_rel = relationship("Service", back_populates="appointments")


class Business(Base):
    __tablename__ = "Business"

    id = Column(Integer, primary_key=True)  # ← исправлено
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(150))
    description = Column(Text)
    login = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=text("NOW()"))