import ast
import datetime
import logging
from pathlib import Path

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.bdd.bdd import Base
from src.bdd.Scope import Scope
from src.parser.tools import *


class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    path = Column(String(200))

    external = Column(Boolean, default=False)
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

    imports_from_to = relationship("ImportFrom", back_populates="module_to", foreign_keys="ImportFrom.module_to_id",
                                   cascade="all")

    def get_imports_name(self):
        """Return name of imported modules in module."""
        imports_name = []
        for module_import in self.imports + self.imports_from:
            imports_name.append(module_import.name)
        return imports_name

    def build(self):
        """Index all scopes and imports within module."""

        # logging.info(f"building module {self.name}")

        module_path = Path(self.path)
        module_name = self.name

        if module_path.is_dir():
            module_path = module_path.joinpath('__init__.py')

        with open(str(module_path), 'r') as file:
            module_text = file.read()
        module_ast = ast.parse(module_text, module_name)

        module_scope = Scope(indent_level=0, indent_level_id=0, name=module_name)
        self.scope.append(module_scope)

        indent_table = {0: 0}

        self.build_helper(module_scope, module_ast, indent_table)

    def build_helper(self, current_scope, module_ast, indent_table):
        """Recursive method to help build module."""
        if type(module_ast) == ast.Module:
            for next_ast in module_ast.body:
                self.build_helper(current_scope, next_ast, indent_table)
        elif type(module_ast) == ast.Assign:
            if type(module_ast.targets) == list:
                for target in module_ast.targets:
                    handle_assign_node(current_scope, target)
            else:
                handle_assign_node(current_scope, module_ast.targets)
        elif type(module_ast) in COND_STMT:
            handle_cond_stmt(current_scope, module_ast, indent_table)
        elif type(module_ast) == ast.FunctionDef:
            handle_fun_def(current_scope, module_ast, indent_table)
        elif type(module_ast) == ast.ClassDef:
            handle_class_def(current_scope, module_ast, indent_table)
        elif type(module_ast) == ast.Import:
            handle_import(current_scope, module_ast)
        elif type(module_ast) == ast.ImportFrom:
            handle_import_from(current_scope, module_ast)
        else:
            pass
