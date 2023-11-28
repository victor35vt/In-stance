from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float, select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

import time
#import pymysql

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Instance_BD"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    inicio: Mapped[float] = mapped_column(Float)           
    estado: Mapped[str] = mapped_column(String(50)) 
    
    def _repr_(self) -> str:
        return f"User(id={self.id!r}, nome={self.nome!r}, inicio={self.inicio!r}, estado={self.estado})"

#conexão com o banco de dados
engine = create_engine("mysql+pymysql://admin:Laranacompany#2728)&$%#%@in-stance.clzez51mwuu2.us-east-1.rds.amazonaws.com/Instance_BD")
User.metadata.create_all(engine)
with Session(engine) as session:
    Laranacompany = User(
        nome="Gabriel",
        inicio= time.time(),
        estado="correta"
    )
    session.add_all([Laranacompany])
    session.commit()
