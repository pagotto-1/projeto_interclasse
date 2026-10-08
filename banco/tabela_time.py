from flask import redirect, url_for, flash
from sqlalchemy import select, func
from database import *
from sqlalchemy.exc import SQLAlchemyError

def select_times_ativos():
    times_select = (
        select(Time, func.count(Jogador.id).label('jogadores')).
        where(Time.status_time == 1).
        outerjoin(Jogador, Jogador.time_id == Time.id).
        group_by(Time.id)
    )
    times = SessionLocal.execute(times_select).all()
    return times

def select_times_excluidos():
    times_select = (
        select(Time, func.count(Jogador.id).label('jogadores')).
        where(Time.status_time == 0).
        outerjoin(Jogador, Jogador.time_id == Time.id).
        group_by(Time.id)
    )
    times = SessionLocal.execute(times_select).all()
    return times

def select_times():
    times_select = (
        select(Time, func.count(Time.id).label('jogadores')).
        outerjoin(Jogador, Jogador.time_id == Time.id).
        group_by(Time.id)
    )
    times = SessionLocal.execute(times_select).all()
    return times

def select_quantidade_times():
    quantidade_select = (
        select(func.count(Time.id)).
        where(Time.status_time == 1)
    )
    quantidade_times = SessionLocal.execute(quantidade_select).scalar()
    return quantidade_times

def select_time_id(time_id):
    time_select = (
        select(Time).
        where(Time.id == time_id)
    )
    time = SessionLocal.execute(time_select).scalar_one_or_none()
    return time

def validar_time(nome_time, turma, responsavel, lista_turmas, times):
    if not nome_time:
        flash('Preencha o nome do time', 'error')
        return redirect(url_for('novo_time'))
    if not turma:
        flash('Preencha a turma do time', 'error')
        return redirect(url_for('novo_time'))
    if not responsavel:
        flash('Preencha o responsavel do time', 'error')
        return redirect(url_for('novo_time'))

    if len(nome_time) > 100:
        flash('O nome do time é muito longo', 'error')
        return redirect(url_for('novo_time'))
    if turma not in lista_turmas:
        flash('Turma inválida', 'error')
        return redirect(url_for('novo_time'))
    if len(responsavel) > 100:
        flash('O nome do responsável é muito longo', 'error')
        return redirect(url_for('novo_time'))

    for time in times:
        if "".join(time.nome) == "".join(nome_time):
            flash('O time já existe ou já existiu', 'error')
            return redirect(url_for('novo_time'))

def insert_time(nome_time, turma, responsavel):
    try:
        time_novo = Time(nome=nome_time, turma=turma, responsavel=responsavel)
        SessionLocal.add(time_novo)
        SessionLocal.commit()
        flash('Time cadastrado com sucesso', 'sucess')
        return redirect(url_for('listar_times'))
    except SQLAlchemyError:
        SessionLocal.rollback()
        flash('Erro ao salvar time no banco de dados', 'error')
        return redirect(url_for('novo_time'))
    except Exception:
        SessionLocal.rollback()
        flash('Erro inesperado', 'error')
        return redirect(url_for('novo_time'))