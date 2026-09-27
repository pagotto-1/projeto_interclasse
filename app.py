from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from database import *
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = "lana-linda-incrivel-maravilhosa"

@app.route("/")
def dashboard():
    times = db_session.execute(select(Time)).scalars().all()
    jogadores = db_session.execute(select(Jogador)).scalars().all()
    partidas = db_session.execute(select(Partida)).scalars().all()

    return render_template(
        "dashboard.html",
        total_jogadores=len(jogadores),
        total_times=len(times),
        total_partidas=len(partidas)
    )

@app.route("/jogadores")
def listar_jogadores():
    jogadores = db_session.execute(select(Jogador)).scalars().all()
    times = db_session.execute(select(Time)).scalars().all()

    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    times = db_session.execute(select(Time)).scalars().all()

    if request.method == "POST":
        nome_jogador = request.form.get("nome", "")
        numero_camisa = request.form.get("numero_camisa")
        posicao = request.form.get("posicao", "")
        time_id = request.form.get("time_id")

        try:
            numero_camisa = int(numero_camisa)
            time_id = int(time_id)
        except ValueError, TypeError:
            flash('Número da camisa e time inválidos', 'error')
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
            flash('O nome do jogador deve ter no máximo 100 caracteres', 'error')
            return redirect(url_for('novo_jogador'))
        if numero_camisa < 0 or numero_camisa > 100:
            flash('Insira um número válido (Entre 0 e 99)', 'error')
            return redirect(url_for('novo_jogador'))
        if len(posicao) > 50:
            flash('Posição de jogador inválida', 'error')
            return redirect(url_for('novo_jogador'))
        if time_id < 0 or time_id > len(times):
            flash('Time inválido', 'error')
            return redirect(url_for('novo_jogador'))

        try:
            jogador_novo = Jogador(nome=nome_jogador, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)
            db_session.add(jogador_novo)
            db_session.commit()
            flash('Jogador cadastrado com sucesso', 'sucess')
            return redirect(url_for('listar_jogadores'))
        except SQLAlchemyError:
            db_session.rollback()
            flash('Erro ao salvar jogador no banco de dados', 'error')
            return redirect(url_for('novo_jogador'))
        except:
            db_session.rollback()
            flash('Erro inesperado', 'error')
            return redirect(url_for('novo_jogador'))

    return render_template("jogadores.html", jogadores=[], times=times)

@app.route("/times")
def listar_times():
    times = db_session.execute(select(Time)).scalars().all()
    return render_template("times.html", times=times)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        nome_time = request.form.get("nome", "")
        turma = request.form.get("turma", "")
        responsavel = request.form.get("responsavel", "")

        if not nome_time:
            flash('Preencha o nome do time', 'error')
            return redirect(url_for('novo_time'))
        if not turma:
            flash('Preencha a turma do time', 'error')
            return redirect(url_for('novo_time'))
        if not responsavel:
            flash('Preencha o responsavel do time', 'error')
            return redirect(url_for('novo_time'))

        try:
            time_novo = Time(nome=nome_time, turma=turma, responsavel=responsavel)
            db_session.add(time_novo)
            db_session.commit()
            flash('Time cadastrado com sucesso', 'sucess')
            return redirect(url_for('listar_times'))
        except SQLAlchemyError:
            db_session.rollback()
            flash('Erro ao salvar time no banco de dados', 'error')
            return redirect(url_for('novo_time'))
        except:
            db_session.rollback()
            flash('Erro inesperado', 'error')
            return redirect(url_for('novo_time'))

    times = db_session.execute(select(Time)).scalars().all()

    return render_template("times.html", times=times)

@app.route("/partidas")
def listar_partidas():
    partidas = db_session.execute(select(Partida)).scalars().all()
    times = db_session.execute(select(Time)).scalars().all()

    return render_template("partidas.html", partidas=partidas, times=times)

@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "")

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
            partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
            db_session.add(partida_nova)
            db_session.commit()
            flash('Partida cadastrado com sucesso', 'sucess')
            return redirect(url_for('listar_partidas'))
        except SQLAlchemyError:
            db_session.rollback()
            flash('Erro ao salvar partida no banco de dados', 'error')
            return redirect(url_for('nova_partida'))
        except:
            db_session.rollback()
            flash('Erro inesperado', 'error')
            return redirect(url_for('nova_partida'))

    times = db_session.execute(select(Time)).scalars().all()

    return render_template("partidas.html", partidas=[], times=times)

if __name__ == "__main__":
    app.run(debug=True)