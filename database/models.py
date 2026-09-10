"""ORM models — the relational schema.

LOCAL STAND-IN FOR: Azure SQL Database tables.
Matches the class diagram in ``docs/architecture/component-diagram.md``:
``drones`` / ``telemetry`` / ``incidents`` / ``response_plans``, plus ``alerts``
(added in Phase-2 for the Public/Responder Alert Service — see
``docs/architecture/alert-recipients.md``).

Only portable column types are used (String/Integer/Float/DateTime/Text/Boolean)
so this schema runs unchanged on Azure SQL.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Drone(Base):
    __tablename__ = "drones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    call_sign: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    model: Mapped[str] = mapped_column(String(64), default="sim-quad")
    status: Mapped[str] = mapped_column(String(32), default="patrolling")
    battery_pct: Mapped[float] = mapped_column(Float, default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    telemetry: Mapped[list["Telemetry"]] = relationship(back_populates="drone")
    incidents: Mapped[list["Incident"]] = relationship(back_populates="drone")


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    drone_id: Mapped[int] = mapped_column(ForeignKey("drones.id"), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, index=True)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    altitude_m: Mapped[float] = mapped_column(Float, default=90.0)
    battery_pct: Mapped[float] = mapped_column(Float, default=100.0)
    bearing_deg: Mapped[float] = mapped_column(Float, default=0.0)

    drone: Mapped[Drone] = relationship(back_populates="telemetry")


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    drone_id: Mapped[int | None] = mapped_column(ForeignKey("drones.id"), nullable=True, index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, index=True)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    detected_class: Mapped[str] = mapped_column(String(32), default="smoke")
    confidence: Mapped[float] = mapped_column(Float)
    snapshot_key: Mapped[str | None] = mapped_column(String(256), nullable=True)
    # weather / fuel context used to build the RAG query
    wind_speed_kmh: Mapped[float] = mapped_column(Float, default=0.0)
    wind_dir_deg: Mapped[float] = mapped_column(Float, default=0.0)
    temperature_c: Mapped[float] = mapped_column(Float, default=25.0)
    fuel_dryness: Mapped[str] = mapped_column(String(16), default="moderate")
    status: Mapped[str] = mapped_column(String(32), default="open")

    drone: Mapped[Drone | None] = relationship(back_populates="incidents")
    plan: Mapped["ResponsePlan | None"] = relationship(back_populates="incident", uselist=False)
    alerts: Mapped[list["Alert"]] = relationship(back_populates="incident")


class ResponsePlan(Base):
    __tablename__ = "response_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), unique=True, index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    plan_markdown: Mapped[str] = mapped_column(Text)
    llm_mode: Mapped[str] = mapped_column(String(32), default="mock")
    retrieved_sources: Mapped[str] = mapped_column(Text, default="")  # JSON list of {source, distance}
    insufficient_context: Mapped[bool] = mapped_column(Boolean, default=False)

    incident: Mapped[Incident] = relationship(back_populates="plan")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, index=True)
    alert_class: Mapped[str] = mapped_column(String(16))  # "immediate" | "enriched"
    recipient_role: Mapped[str] = mapped_column(String(64))
    channel: Mapped[str] = mapped_column(String(32), default="sms")
    body: Mapped[str] = mapped_column(Text)
    delivered: Mapped[bool] = mapped_column(Boolean, default=True)  # mock provider always "delivers"

    incident: Mapped[Incident] = relationship(back_populates="alerts")
