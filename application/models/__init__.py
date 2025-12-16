from sqlalchemy import Column, Integer, String, Date, DateTime, func, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"


    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    emp_org_id = Column(Integer, unique=True, nullable=False)
    last_name = Column(String(100), nullable=False)
    work_email = Column(String(200), unique=True, nullable=False)
    compentency = Column(String(100))
    reporting_to = Column(Integer)
    grade = Column(String(20))
    project_id = Column(Integer)
    doj = Column(Date)
    allocation_type = Column(String(50))
    allocation_percent = Column(Integer)
    designation = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Users(Base):
    __tablename__ = 'users'  # Table name

    # Auto-increment primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    theme = Column(String(50), nullable=False, server_default='light')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Reportinmanagers(Base):
    __tablename__ = 'reporting_managers'  # Table name

    # Auto-increment primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Bussinessgroups(Base):
    __tablename__ = 'bussiness_groups'  # Table name

    # Auto-increment primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Customers(Base):
    __tablename__ = 'customers'  # Table name

    # Auto-increment primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    bussiness_group_id = Column(Integer, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_code = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Projects table mapping
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    bussines_group = Column(Text)  # Matches TEXT type
    hd = Column(Integer)  # Hours a day
    customer_id = Column(Integer, nullable=False)
    project_currency = Column(String(50), nullable=False, default='INR')
    status = Column(String(50), nullable=False, default='ongoing')
    created_at = Column(TIMESTAMP, server_default=func.now())