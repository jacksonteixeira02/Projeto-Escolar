import io
import sqlite3
import csv
from bancoDados import BancoDados


class Professor:
    def __init__(self, id, nome, email, senha, materia):
        self.id = id
        self.nome = nome
        self.materia = materia

    def listar(self):
        con = BancoDados.conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM alunos")
        alunos = cur.fetchall()
        con.close()
        return alunos

    def cadastrar(self, nome, nota):
        con = BancoDados.conectarAlunos()
        cur = con.cursor()
        cur.execute("INSERT INTO alunos (nota) VALUES (?)", nota)
        con.commit()
        con.close()

    def excluir(self, id):
        con = BancoDados.conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM alunos WHERE id = ?", (id,))
        con.commit()
        con.close()

    def exportar(self):
        con = BancoDados.conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM alunos")
        buffer = io.StringIO()
        write = csv.writer(buffer)
        write.writerow(["id", "nome", "nota"])
        for aluno in cur.fetchall():
            write.writerow(aluno)
        buffer.seek(0)
        return io.BytesIO(buffer.getvalue().encode())

    def editar(self, id, nota):
        con = BancoDados.conectar()
        cur = con.cursor()
        cur.execute("UPDATE alunos SET nota = ? WHERE id = ?", (nota, id))
        con.commit()
        cur.execute("SELECT * FROM alunos WHERE id = ?", (id,))
        aluno = cur.fetchone()
        con.close()
        return aluno

    def buscarPorId(self, id):
        con = BancoDados.conectarAlunos()
        cur = con.cursor()
        cur.execute("SELECT * FROM alunos WHERE id = ?", (id,))
        aluno = cur.fetchone()
        con.close()
        return aluno
