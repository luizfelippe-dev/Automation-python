from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey, Text, BLOB, Float, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, date
import os
from pathlib import Path


# Cria o caminho para o banco de dados no diretório pai
PATH = Path(__file__).parent 
path_db = os.path.join(PATH, 'database', 'database.db')

CONN = f"sqlite:///{path_db}"

engine = create_engine(CONN,echo=False)
Session =  sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Arquivos(Base):
   __tablename__='arquivos'
   id = Column(Integer, primary_key=True, autoincrement=True)
   name_arquivo = Column(String)
   tipo = Column(String,default=None ,comment="Se ele for SW ou não")
   cidade = Column(String,comment='A cidade da pasta que esta sendo executado')
   ano = Column(String,comment='O ano da pasta no qual esta sendo executado')
   sistema = Column(String)
   caminho_completo = Column(String)
   data_criacao = Column(DateTime)
   data_modificacao = Column(DateTime)
   tamanho_arquivo = Column(Float)
   data_arquivo = Column(DateTime,comment="Data e hora que está no nome do arquivo")
   firebird = Column(String)
   excluir = Column(String,comment="Caso for S, apagar se for N nao apagar")
   log_inclusao = Column(DateTime, default=datetime.now())


class ArquivosExcluidos(Base):
   __tablename__='arquivos_excluidos'
   id = Column(Integer, primary_key=True, autoincrement=True)
   old_id = Column(Integer)
   name_arquivo = Column(String)
   tipo = Column(String,default=None ,comment="Se ele for SW ou não")
   cidade = Column(String,comment='A cidade da pasta que esta sendo executado')
   ano = Column(String,comment='O ano da pasta no qual esta sendo executado')
   sistema = Column(String)
   caminho_completo = Column(String)
   data_criacao = Column(DateTime)
   data_modificao = Column(DateTime)
   tamanho_arquivo = Column(Float)
   data_arquivo = Column(DateTime,comment="Data e hora que está no nome do arquivo")
   firebird = Column(String)
   excluir = Column(String,comment="Caso for S, apagar se for N nao apagar")
   log_inclusao = Column(DateTime)
   log_exclusao = Column(DateTime, default=datetime.now())

if not os.path.exists(path_db):
   Base.metadata.create_all(bind=engine) 

def get_arquivos(id:int = 0, nome_arquivo: str = None):
   
   pass

def execute_direct_sql():
    output = []
    with engine.connect() as connection:
        result = connection.execute(text("SELECT MAX(DATA_ARQUIVO) FROM ARQUIVOS "))
        for row in result:
            output.append(row)
    connection.close()
# Chama a função para executar a SQL direta