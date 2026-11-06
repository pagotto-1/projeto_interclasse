from logging import raiseExceptions

from flask import flash, redirect, url_for
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from database import *
from datetime import datetime
from banco import tabela_jogador

def select_todos():
    TimeOrigem = aliased(Time)
    TimeDestino = aliased(Time)

    movimentacoes_sql = (
        select(Movimentacao, Jogador, TimeOrigem, TimeDestino)
        .join(Jogador, Movimentacao.jogador_id == Jogador.id)
        .outerjoin(TimeOrigem, Movimentacao.time_origem_id == TimeOrigem.id)
        .outerjoin(TimeDestino, Movimentacao.time_destino_id == TimeDestino.id)
    )
    movimentacoes = SessionLocal.execute(movimentacoes_sql).all()
    return movimentacoes


def select_quantidade_total():
    movimentacoes_sql = select(func.count(Movimentacao.id))
    qtd_total = SessionLocal.execute(movimentacoes_sql).scalar()
    return qtd_total

def salvar(jogador_id, time_destino_id):
    try:
        jogador = tabela_jogador.select_jogador_id(jogador_id)
        if not jogador:
            flash("Jogador não encontrado", "error")
            return redirect(url_for('nova_movimentacao'))
        time_origem_id = jogador.time_id
        if time_destino_id == time_origem_id:
            flash("O jogador já pertence a esse time", "error")
            return

        data_atual = datetime.now()

        jogador.time_id = time_destino_id

        nova_movimentacao = Movimentacao(jogador_id=int(jogador_id), time_destino_id=int(time_destino_id), time_origem_id=time_origem_id, data_movimentacao=data_atual)
        SessionLocal.add(nova_movimentacao)
        SessionLocal.commit()
        flash("Movimentação realizada com sucesso", "success")
        return redirect(url_for('listar_movimentacoes'))
    except SQLAlchemyError:
        SessionLocal.rollback()
        flash("Erro ao salvar movimentação no banco de dados", "error")
        return redirect(url_for('nova_movimentacao'))
    except Exception:
        SessionLocal.rollback()
        flash("Erro inesperado", "error")
        return redirect(url_for('nova_movimentacao'))