import io
import sqlite3
import csv
from flask import Flask, render_template, request, redirect, url_for, send_file
import professor
from professor import Professor
from usuario import Usuarios


prof = Professor(id = 1, nome = "João", email = "joao2016@gmail.com", senha = 1234567789, materia = "Biologia")

app = Flask(__name__)

@app.route('/')
def listar():
    alunos = prof.listar()
    return render_template("listar.html", alunos=alunos)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome")
        nota = float(request.form.get("nota"))
        prof.cadastrar(nome, nota)
        return redirect(url_for("listar"))
    else:
        return render_template('cadastrar.html')

@app.route("/excluir/<int:id>", methods=['GET'])
def excluir(id):
    prof.excluir(id)
    return redirect(url_for("listar"))

@app.route("/exportar", methods=['GET'])
def exportar():
    arquivo_csv = prof.exportar()
    return send_file(
        arquivo_csv,
        mimetype='text/csv',
        as_attachment=True,
        download_name='alunos.csv'
    )

@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nome = request.form.get("nome")
        nota = float(request.form.get("nota"))
        prof.editar(id, nome, nota)
        return redirect(url_for('listar'))
    else:
        aluno = prof.buscarPorId(id)
        return render_template("editar.html", aluno=aluno)


if __name__ == "__main__":
    app.run(debug=True)