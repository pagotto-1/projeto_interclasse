from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session, DeclarativeBase
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

engine = create_engine("mysql+pymysql://root:senaisp@localhost:3306/interclasse_db")

SessionLocal = scoped_session(sessionmaker(bind=engine))

# Base = declarative_base()

class Base(DeclarativeBase):
    pass

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    turma = Column(String(20))
    responsavel = Column(String(100))
    status_time = Column(Boolean, default=True)

class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    numero_camisa = Column(Integer)
    posicao = Column(String(50))
    time_id = Column(Integer, ForeignKey("times.id", ondelete="SET NULL"))
    status_jogador = Column(Boolean, default=True)

class Partida(Base):
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_casa_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)
    time_visitante_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)
    gols_casa = Column(Integer, default=0)
    gols_visitante = Column(Integer, default=0)
    data_partida = Column(Date)
    status_partida = Column(Boolean, default=True)

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jogador_id = Column(Integer, ForeignKey("jogadores.id", ondelete="SET NULL"))
    time_origem_id = Column(Integer, ForeignKey("times.id", ondelete="SET NULL"))
    time_destino_id = Column(Integer, ForeignKey("times.id", ondelete="SET NULL"))
    data_movimentacao = Column(DateTime)

    def __repr__(self):
        return f"<Movimentação: ID={self.id}, JogadorID={self.jogador_id}, TimeAntigoID={self.time_origem_id}, TimeDestinoID={self.time_destino_id}>"

class Usuario(Base, UserMixin):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
    atualizado_em = Column(DateTime, nullable=False, onupdate=func.now())

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)