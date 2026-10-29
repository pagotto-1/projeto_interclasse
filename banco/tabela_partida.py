from flask import redirect, url_for, flash
from sqlalchemy import select, func, or_
from database import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

def select_partidas_ativas():
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_select = (
        select(Partida, TimeCasa, TimeVisitante).
        where(Partida.status_partida == 1).
        join(TimeCasa, Partida.time_casa_id == TimeCasa.id).
        join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )
    partidas = SessionLocal.execute(partidas_select).all()
    return partidas

def select_partidas_excluidas():
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_select = (
        select(Partida, TimeCasa, TimeVisitante).
        where(Partida.status_partida == 0).
        join(TimeCasa, Partida.time_casa_id == TimeCasa.id).
        join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )
    partidas = SessionLocal.execute(partidas_select).all()
    return partidas

def select_partida_id(partida_id):
    partidas_select = (
        select(Partida).
        where(Partida.id == partida_id)
    )
    partida = SessionLocal.execute(partidas_select).scalar_one_or_none()
    return partida

def select_partidas():
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_select = (
        select(Partida, TimeCasa, TimeVisitante).
        where(Partida.status_partida == 1).
        join(TimeCasa, Partida.time_casa_id == TimeCasa.id).
        join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )
    partidas = SessionLocal.execute(partidas_select).all()
    return partidas

def select_partidas_time(time_id):
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_select = (
        select(Partida, TimeCasa, TimeVisitante).
        where(or_(Partida.time_casa_id == time_id, Partida.time_visitante_id == time_id)).
        join(TimeCasa, Partida.time_casa_id == TimeCasa.id).
        join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )
    partidas = SessionLocal.execute(partidas_select).all()
    return partidas

def select_quantidade_partidas():
    quantidade_select = (
        select(func.count(Partida.id)).
        where(Partida.status_partida == 1)
    )
    quantidade_partidas = SessionLocal.execute(quantidade_select).scalar()
    return quantidade_partidas

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
        partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
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