import io
import sqlite3
import csv
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

def conectar():
    return sqlite3.connect("escola.db")

@app.route('/')
def listar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM alunos")
    alunos = cur.fetchall()
    con.close()
    return render_template("listar.html", alunos=alunos)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome")
        nota = request.form.get("nota")
        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
        con.commit()
        con.close()
        return redirect(url_for("listar"))
    else:
        return render_template('cadastrar.html')

@app.route("/excluir/<int:id>", methods=['GET'])
def excluir(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM alunos WHERE id = ?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("listar"))

@app.route("/exportar", methods=['GET'])
def exportar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM alunos")
    buffer = io.StringIO()
    write = csv.writer(buffer)
    write.writerow(["id", "nome", "nota"])
    for aluno in cur.fetchall():
        write.writerow(aluno)
    buffer.seek(0)
    return send_file(io.BytesIO(buffer.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='alunos.csv')

@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        con = conectar()
        cur = con.cursor()
        nome = request.form.get("nome")
        nota = request.form.get("nota")
        cur.execute("UPDATE alunos SET nome = ?, nota = ? WHERE id = ?", (nome, nota, id))
        con.commit()
        con.close()
        return redirect(url_for('listar'))
    else:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM alunos WHERE id = ?", (id,))
        aluno = cur.fetchone()
        return render_template("editar.html", aluno=aluno)

if __name__ == "__main__":
    app.run(debug=True)