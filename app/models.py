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


class InitiativeType(Base):
    __tablename__ = "initiative_type"

    initiative_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
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


class Initiative(Base):
    __tablename__ = "initiative"

    initiative_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    initiative_type = Column(
        Integer,
        ForeignKey("initiative_type.initiative_type_id", ondelete="CASCADE"),
        nullable=False
    )

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

    status_id = Column(
        Integer,
        ForeignKey("status_code.status_id", ondelete="CASCADE"),
        nullable=False
    )

    creator = relationship("Employee")
    updater = relationship("Employee")
    status = relationship("StatusCode")


class TaskLog(Base):
    __tablename__ = "task_log"

    task_id = Column(Integer, primary_key=True, index=True)

    initiative_id = Column(
        Integer,
        ForeignKey("initiative.initiative_id", ondelete="CASCADE"),
        nullable=False
    )

    description = Column(String, nullable=False)

    logged_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    logged_by = Column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="CASCADE"),
        nullable=False
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    creator = relationship("Employee")
    updater = relationship("Employee")
    initiative = relationship("Initiative")


class Subscription(Base):
    __tablename__ = "subscription"

    subscription_id = Column(Integer, primary_key=True, index=True)

    subscribed_by = Column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="CASCADE"),
        nullable=False
    )

    initiative_id = Column(
        Integer,
        ForeignKey("initiative.initiative_id", ondelete="CASCADE"),
        nullable=False
    )

    subscribed_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    subscriber = relationship("Employee")
    initiative = relationship("Initiative")


class Review(Base):
    __tablename__ = "review"

    review_id = Column(Integer, primary_key=True, index=True)

    initiative_id = Column(
        Integer,
        ForeignKey("initiative.initiative_id", ondelete="CASCADE"),
        nullable=False
    )

    description = Column(String, nullable=False)

    given_by = Column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="CASCADE"),
        nullable=False
    )

    given_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    reviewer = relationship("Employee")
    initiative = relationship("Initiative")
