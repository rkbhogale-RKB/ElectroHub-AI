from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import CreatedAtMixin


class Employee(CreatedAtMixin, Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint(
            "employment_status IN ('ACTIVE', 'ON_LEAVE', 'TERMINATED')",
            name="ck_employees_status",
        ),
        CheckConstraint("salary >= 0", name="ck_employees_salary_nonneg"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_code: Mapped[str] = mapped_column(String(20), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(20))

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"), index=True
    )
    primary_store_id: Mapped[int | None] = mapped_column(
        ForeignKey("stores.id", ondelete="RESTRICT"), index=True
    )
    manager_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"), index=True
    )

    job_title: Mapped[str] = mapped_column(String(100))
    date_joined: Mapped[date] = mapped_column(Date)
    employment_status: Mapped[str] = mapped_column(String(20), server_default="ACTIVE")
    salary: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    department: Mapped["Department"] = relationship()
    primary_store: Mapped["Store | None"] = relationship()
    manager: Mapped["Employee | None"] = relationship(
        remote_side="Employee.id"
    )