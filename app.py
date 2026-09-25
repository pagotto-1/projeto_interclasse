from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from banco import tabela_time, tabela_jogador, tabela_partida
from database import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

app = Flask(__name__)
app.secret_key = "lana-linda-incrivel-maravilhosa"

lista_posicoes = ['GOL', 'ZAG', 'VOL', 'LAT', 'MEI', 'ATA']
lista_turmas = ['6 Fundamental', '7 Fundamental', '8 Fundamental', '9 Fundamental', '1 Médio', '2 Médio', '3 Médio']

@app.route("/")
def dashboard():
    jogadores = tabela_jogador.select_jogadores_ativos()
    times = tabela_time.select_times_ativos()
    partidas = tabela_partida.select_partidas_ativas()
    return render_template("dashboard.html", total_jogadores=len(jogadores), total_times=len(times), total_partidas=len(partidas))

@app.route("/times")
def listar_times():
    times = tabela_time.select_times_ativos()
    return render_template("times.html", times=times)

@app.route("/times/excluidos")
def listar_times_excluidos():
    times_excluidos = tabela_time.select_times_excluidos()
    return render_template("times.html", times=times_excluidos)

@app.route("/times/resgatar/<time_id>", methods=["GET", "POST"])
def resgatar_time(time_id):
    time_excluido = tabela_time.select_time_id(time_id=time_id)
    if time_excluido:
        time_excluido.status_time = True
        SessionLocal.commit()
    return redirect(url_for('listar_times_excluidos'))

@app.route("/times/excluir/<time_id>", methods=["GET", "POST"])
def excluir_time(time_id):
    time = tabela_time.select_time_id(time_id=time_id)
    if time:
        time.status_time = False
        SessionLocal.commit()
    return redirect(url_for('listar_times'))

@app.route("/times/alterar/<time_id>", methods=["GET", "POST"])
def alterar_time(time_id):
    time = tabela_time.select_time_id(time_id=time_id)
    if request.method == "POST":
        pass
    times = tabela_time.select_times()
    time = tabela_time.select_time_id(time_id=time_id)
    return render_template("times.html", times=times, time=time, lista_turmas=lista_turmas)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    times = tabela_time.select_times()

    if request.method == "POST":
        nome_time = request.form.get("nome", "")
        turma = request.form.get("turma", "")
        responsavel = request.form.get("responsavel", "")

        tabela_time.validar_time(nome_time=nome_time, turma=turma, responsavel=responsavel, lista_turmas=lista_turmas, times=times)
        tabela_time.insert_time(nome_time=nome_time, turma=turma, responsavel=responsavel)

    times = tabela_time.select_times()
    return render_template("times.html", times=times, lista_turmas=lista_turmas)

@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_jogadores_ativos()
    times = tabela_time.select_times()
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/excluidos")
def listar_jogadores_excluidos():
    jogadores_excluidos = tabela_jogador.select_jogadores_excluidos()
    times = tabela_time.select_times()
    return render_template("jogadores.html", jogadores=jogadores_excluidos, times=times)

@app.route("/jogadores/resgatar/<jogador_id>")
def resgatar_jogador(jogador_id):
    jogador_excluido = tabela_jogador.select_jogador_id(jogador_id)
    if jogador_excluido:
        jogador_excluido.status_jogador = True
        SessionLocal.commit()
    return redirect(url_for('listar_jogadores_excluidos'))

@app.route("/jogador/excluir/<jogador_id>", methods=["GET", "POST"])
def excluir_jogador(jogador_id):
    jogador = tabela_jogador.select_jogador_id(jogador_id)
    if jogador:
        jogador.status_jogador = False
        SessionLocal.commit()
    return redirect(url_for('listar_jogadores'))

@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    times = tabela_time.select_times()
    jogadores = tabela_jogador.select_jogadores()

    if request.method == "POST":
        nome_jogador = request.form.get("nome", "")
        numero_camisa = request.form.get("numero_camisa")
        posicao = request.form.get("posicao", "")
        time_id = request.form.get("time_id")

        tabela_jogador.validar_jogador(nome_jogador=nome_jogador, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id, lista_posicoes=lista_posicoes, times=times, jogadores=jogadores)
        tabela_jogador.insert_jogador(nome_jogador=nome_jogador, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    jogadores = tabela_jogador.select_jogadores()
    return render_template("jogadores.html", jogadores=jogadores, times=times, lista_posicoes=lista_posicoes)

@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_partidas_ativas()
    times = tabela_time.select_times()
    return render_template("partidas.html", partidas=partidas, times=times)

@app.route("/partidas/excluidas")
def listar_partidas_excluidas():
    partidas_excluidas = tabela_partida.selecet_partidas_excluidas()
    times = tabela_time.select_times()
    return render_template("partidas.html", partidas=partidas_excluidas, times=times)

@app.route("/partidas/excluir/<partida_id>", methods=["GET", "POST"])
def excluir_partida(partida_id):
    partida = tabela_partida.select_partidas_id(partida_id=partida_id)
    if partida:
        partida.status_partida = False
        SessionLocal.commit()
    return redirect(url_for('listar_partidas'))

@app.route("/partidas/resgatar/<partida_id>", methods=["GET", "POST"])
def resgatar_partida(partida_id):
    partida = tabela_partida.select_partidas_id(partida_id=partida_id)
    if partida:
        partida.status_partida = True
        SessionLocal.commit()
    return redirect(url_for('listar_partidas_excluidas'))

@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    times = tabela_time.select_times()

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa")
        gols_visitante = request.form.get("gols_visitante")
        data_partida = request.form.get("data_partida", "")

        data_partida = datetime.strptime(data_partida, "%Y-%m-%d").date()

        tabela_partida.validar_partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida, times=times)
        tabela_partida.insert_partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = SessionLocal.execute(select(Partida)).scalars().all()
    return render_template("partidas.html", partidas=partidas, times=times)

if __name__ == "__main__":
    app.run(debug=True)