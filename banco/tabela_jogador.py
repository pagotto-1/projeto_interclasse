from flask import redirect, url_for, flash
from sqlalchemy import select
from database import *
from sqlalchemy.exc import SQLAlchemyError

def select_jogadores_ativos():
    jogadores = SessionLocal.execute(select(Jogador).where(Jogador.status_jogador == 1)).scalars().all()
    return jogadores

def select_jogadores_excluidos():
    jogadores = SessionLocal.execute(select(Jogador).where(Jogador.status_jogador == 0)).scalars().all()
    return jogadores

def select_jogadores():
    jogadores = SessionLocal.execute(select(Jogador)).scalars().all()
    return jogadores

def select_jogador_id(jogador_id):
    jogador = SessionLocal.execute(select(Jogador).where(Jogador.id == jogador_id)).scalar_one_or_none()
    return jogador

def validar_jogador(nome_jogador, numero_camisa, posicao, time_id, lista_posicoes, times, jogadores):
    try:
        numero_camisa = int(numero_camisa)
        time_id = int(time_id)
    except ValueError, TypeError:
        flash('Número de camisa ou time inválido', 'error')
        return redirect(url_for('novo_jogador'))

    if not nome_jogador:
        flash('Preencha o nome de jogador', 'error')
        return redirect(url_for('novo_jogador'))
    if not numero_camisa:
        flash('Preencha o numero da camisa', 'error')
        return redirect(url_for('novo_jogador'))
    if not posicao:
        flash('Preencha a posição do jogador', 'error')
        return redirect(url_for('novo_jogador'))
    if not time_id:
        flash('Preencha o time do jogador', 'error')
        return redirect(url_for('novo_jogador'))

    if len(nome_jogador) > 100:
        flash('O nome é muito longo, digite um nome menor', 'error')
        return redirect(url_for('novo_jogador'))
    if numero_camisa < 0 or numero_camisa >= 100:
        flash('O número da camisa deve estar entre 0 e 99', 'error')
        return redirect(url_for('novo_jogador'))
    if posicao not in lista_posicoes:
        flash('A posição não existe', 'error')
        return redirect(url_for('novo_jogador'))
    if time_id <= 0 or time_id > len(times):
        flash('O time selecionado não existe', 'error')
        return redirect(url_for('novo_jogador'))

    for jogador in jogadores:
        if "".join(jogador.nome) == "".join(nome_jogador):
            flash('Este jogador já existe', 'error')
            return redirect(url_for('novo_jogador'))

def insert_jogador(nome_jogador, numero_camisa, posicao, time_id):
    try:
        jogador_novo = Jogador(nome=nome_jogador, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)
        SessionLocal.add(jogador_novo)
        SessionLocal.commit()
        flash('Jogador cadastrado com sucesso', 'sucess')
        return redirect(url_for('listar_jogadores'))
    except SQLAlchemyError:
        SessionLocal.rollback()
        flash('Erro ao salvar jogador no banco de dados', 'error')
        return redirect(url_for('novo_jogador'))
    except Exception:
        SessionLocal.rollback()
        flash('Erro inesperado', 'error')
        return redirect(url_for('novo_jogador'))