from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
database_url = 'mysql+pymysql://root:Senac2021@localhost:3306/locadora'

class Filme(Base):
    __tablename__ = 'filme'

    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)

    def __rep__(self):
        return f'Filme [Título: {self.titulo}, Gênero: {self.genero}, Ano: {self.ano}]'

def create_database():
    engine = create_engine(database_url, echo=True)
    try:
        engine.connect()
    except Exception as e:
        if '1049' in str(e):
            engine = create_engine(database_url.rsplit('/', 1)[0], echo=True)
            conn = engine.connect()
            conn.execute('CREATE DATABASE locadora')
            conn.close()
            print('Banco locadora criado com sucesso')
        else:
            raise e

create_database()

# configuracoes

engine = create_engine(database_url, echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    Base.metadata.create_all(engine)
    print('Tabela filme criada com sucesso!')
create_table()

# inserção no banco
data_insert = Filme(titulo='Emanuelle', ano='1987', genero='entretenimento')
session.add(data_insert)
session.commit()

# remoção no banco
session.query(Filme).filter(Filme.titulo == 'Emanuelle').delete()
session.commit()

# atualização do banco
session.query(Filme).filter(Filme.titulo == 'Batman').update({'ano' : '2022'})
session.commit()

# consultar o banco
data = session.query(Filme).all()
session.commit()
print(data)

session.close()