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
    employee_type = relationship(
        "EmployeeType",
        foreign_keys=[employee_type_id]
    )


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

    creator = relationship("Employee", foreign_keys=[created_by])
    updater = relationship("Employee", foreign_keys=[updated_by])


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

    creator = relationship("Employee", foreign_keys=[created_by])
    updater = relationship("Employee", foreign_keys=[updated_by])


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

    init_type = relationship("InitiativeType", foreign_keys=[initiative_type])
    creator = relationship("Employee", foreign_keys=[created_by])
    updater = relationship("Employee", foreign_keys=[updated_by])
    status = relationship("StatusCode", foreign_keys=[status_id])


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

    creator = relationship("Employee", foreign_keys=[logged_by])
    initiative = relationship("Initiative", foreign_keys=[initiative_id])


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

    subscriber = relationship("Employee", foreign_keys=[subscribed_by])
    initiative = relationship("Initiative", foreign_keys=[initiative_id])


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

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    reviewer = relationship("Employee", foreign_keys=[given_by])
    initiative = relationship("Initiative", foreign_keys=[initiative_id])


class Rating(Base):
    __tablename__ = "rating"

    rating_id = Column(Integer, primary_key=True, index=True)

    initiative_id = Column(
        Integer,
        ForeignKey("initiative.initiative_id", ondelete="CASCADE"),
        nullable=False
    )

    point = Column(Integer, nullable=False)

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

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    rater = relationship("Employee", foreign_keys=[given_by])
    initiative = relationship("Initiative", foreign_keys=[initiative_id])
