from datetime import date

from sqlalchemy import (
    CheckConstraint, Date, ForeignKey, Index, String, text
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EmployeeStoreAssignment(Base):
    __tablename__ = "employee_store_assignments"
    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="ck_assignment_dates",
        ),
        CheckConstraint(
            "assignment_type IN ('PERMANENT', 'TEMPORARY', 'COVER')",
            name="ck_assignment_type",
        ),
        # An employee can have at most ONE currently-open primary assignment
        Index(
            "uq_one_open_primary_assignment",
            "employee_id",
            unique=True,
            postgresql_where=text("is_primary AND end_date IS NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"), index=True
    )
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="RESTRICT"), index=True
    )
    assignment_type: Mapped[str] = mapped_column(String(20), server_default="PERMANENT")
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    is_primary: Mapped[bool] = mapped_column(server_default=text("false"))