import datetime

from flask import redirect, url_for, flash
from sqlalchemy import select
from database import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def select_partidas_ativas():
    partidas = SessionLocal.execute(select(Partida).where(Partida.status_partida == 1)).scalars().all()
    return partidas

def selecet_partidas_excluidas():
    partidas = SessionLocal.execute(select(Partida).where(Partida.status_partida == 0)).scalars().all()
    return partidas

def select_partidas_id(partida_id):
    partida = SessionLocal.execute(select(Partida).where(Partida.id == partida_id)).scalar_one_or_none()
    return partida

def select_partidas():
    partidas = SessionLocal.execute(select(Partida)).scalars().all()
    return partidas

def validar_partida(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida, times):
    if not time_casa_id:
        flash('Preencha o time da casa', 'error')
        return redirect(url_for('nova_partida'))
    if not time_visitante_id:
        flash('Preencha o time visitante', 'error')
        return redirect(url_for('nova_partida'))
    if not gols_casa:
        flash('Preencha os gols da casa', 'error')
        return redirect(url_for('nova_partida'))
    if not gols_visitante:
        flash('Preencha os gols do visitante', 'error')
        return redirect(url_for('nova_partida'))
    if not data_partida:
        flash('Preencha a data da partida', 'error')
        return redirect(url_for('nova_partida'))

    try:
        time_casa_id = int(time_casa_id)
        time_visitante_id = int(time_visitante_id)
    except ValueError, TypeError:
        flash('Time da casa ou visitante inválido', 'error')
        return redirect(url_for('nova_partida'))

    try:
        gols_casa = int(gols_casa)
        gols_visitante = int(gols_visitante)
    except ValueError, TypeError:
        flash('Quantidade de gols inválida, insira apenas números', 'error')
        return redirect(url_for('nova_partida'))

    if time_casa_id <= 0 or time_visitante_id <= 0 or time_casa_id > len(times) or time_visitante_id > len(times):
        flash('Time inexistente', 'error')
        return redirect(url_for('nova_partida'))
    if time_casa_id == time_visitante_id:
        flash('Selecione times diferentes', 'error')
        return redirect(url_for('nova_partida'))

def insert_partida(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa,
                               gols_visitante=gols_visitante, data_partida=data_partida)
        SessionLocal.add(partida_nova)
        SessionLocal.commit()
        flash('Partida cadastrada com sucesso', 'sucess')
        return redirect(url_for('listar_partidas'))
    except SQLAlchemyError:
        SessionLocal.rollback()
        flash('Erro ao salvar partida no banco de dados', 'error')
        return redirect(url_for('nova_partida'))
    except Exception:
        SessionLocal.rollback()
        flash('Erro inesperado', 'error')
        return redirect(url_for('nova_partida'))