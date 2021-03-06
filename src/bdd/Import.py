from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

import sys
from src.bdd.bdd import Base


class Import(Base):
    __tablename__ = 'import'

    id = Column(Integer, primary_key=True)

    name = Column(String(250), default="")
    asname = Column(String(250))

    module_from_id = Column(Integer, ForeignKey("module.id"))
    module_from = relationship("Module", foreign_keys=module_from_id)

    module_to_id = Column(Integer, ForeignKey("module.id"))
    module_to = relationship("Module", foreign_keys=module_to_id)

    def __str__(self):
        result = f"Name: {self.name}, As: {self.asname}, From: {self.module_from.name}, Bound: {self.module_to_id is not None}"
        return result

