import io
import sqlite3
import csv
from flask import Flask, render_template, request, redirect, url_for, send_file, session
import professor
from professor import Professor
from usuario import Usuarios
from aluno import Aluno


prof = Professor(id=1, nome="João", email="joao2016@gmail.com", senha=1234567789, materia="Biologia")

app = Flask(__name__)
app.secret_key = "uma_chave_secreta_qualquer"

@app.route('/', methods=['GET', 'POST'])
def landingPage():
    if request.method == 'GET':
        return render_template('landingPage.html')
    else:
        return redirect(url_for("cadastrarProfessor"))


@app.route('/cadastrarProfessor', methods=['GET', 'POST'])
def cadastrarProfessor():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")
        materia = request.form.get("materia")

        if not email.endswith("@gmail.com") or len(senha) <= 8:
            return render_template('cadastrarProfessor.html', erro=("Senha ou E-mail inválidos"))

        user = Usuarios()
        user.cadastrarProfessor(email, senha, materia)

        return redirect(url_for("logarProfessor"))

    return render_template("cadastrarProfessor.html")

@app.route('/cadastrarAluno', methods=['GET', 'POST'])
def cadastrarAluno():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")
        nome = request.form.get("nome")

        if not email.endswith("@gmail.com") or len(senha) <= 8:
            return render_template('cadastrarAluno.html', erro=("Senha ou E-mail inválidos"))

        user = Usuarios()
        user.cadastrarAluno(email, senha, nome)

        return redirect(url_for("logarAluno"))

    return render_template("cadastrarAluno.html")


@app.route('/logarProfessor', methods=['GET', 'POST'])
def logarProfessor():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email.endswith("@gmail.com") or len(senha) <= 8:
            return render_template('logarProfessor.html', erro="Senha ou E-mail inválidos!")

        user = Usuarios()
        resultado = user.logar(email, senha)

        if resultado:
            return redirect(url_for("listar"))

        else:
            return render_template('logarProfessor.html', erro="senha ou email inválidos!")

    return render_template('logarProfessor.html')


@app.route('/logarAluno', methods=['GET', 'POST'])
def logarAluno():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Validação básica
        if not email.endswith("@gmail.com") or len(senha) <= 8:
            return render_template('logarAluno.html', erro="Senha ou E-mail inválidos!")

        user = Usuarios()
        resultado = user.logar(email, senha)  # retorna uma tupla (id, email, ...)

        if resultado:
            # Salva o ID do usuário na sessão (primeiro item da tupla)
            session["usuario_id"] = resultado[0]
            return redirect(url_for("visualizarNotas"))
        else:
            return render_template('logarAluno.html', erro="Senha ou email inválidos!")

    return render_template('logarAluno.html')

@app.route("/visualizarNotas")
def visualizarNotas():
    if "usuario_id" not in session:
        return redirect(url_for("logarAluno"))

    usuario_id = session["usuario_id"]

    # Cria o objeto da classe Aluno e pega a nota
    aluno = Aluno()
    nota = aluno.visualizarNotas(usuario_id)

    return render_template("visualizarNotas.html", nota=nota)


@app.route('/listar', methods=['GET', 'POST'])
def listar():
    alunos = prof.listar()
    return render_template("listar.html", alunos=alunos)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        nota = float(request.form.get("nota"))
        prof.cadastrar(nota)
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