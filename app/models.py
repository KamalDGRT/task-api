# Every model represents a table in our database.

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class EmployeeType(Base):
    __tablename__ = "employee_type"

    employee_type_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, index=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    employee_type_id = Column(
        Integer,
        ForeignKey("employee_type.employee_type_id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    # This is gonna create another property for us for our employee table
    # so that when we retrieve our employee details, it will fetch the
    # properties of the employee_type table
    employee_type = relationship("EmployeeType")


class StatusCode(Base):
    __tablename__ = "status_code"

    status_id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    created_by = Column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="CASCADE"),
        nullable=False
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    updated_by = Column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="CASCADE"),
        nullable=False
    )

    creator = relationship("Employee")
    updater = relationship("Employee")
