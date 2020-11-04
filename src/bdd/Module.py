import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from bdd.bdd import Base
from bdd.Scope import Scope

class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    path = Column(String(200))
    visit_date = Column(DateTime, default=datetime.datetime.now())

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="module")
    scope = relationship("Scope", back_populates="module", cascade="all, delete, delete-orphan")
    imports = relationship("Import", back_populates="module_from", foreign_keys="Import.module_from_id",
                           cascade="all, delete, delete-orphan")

    imports_from = relationship("ImportFrom", back_populates="module_from", foreign_keys="ImportFrom.module_from_id",
                                cascade="all, delete, delete-orphan")

    imports_to = relationship("Import", back_populates="module_to", foreign_keys="Import.module_to_id",
                              cascade="all")
