import sqlite3
from bancoDados import BancoDados
import random

class Aluno:
    def __init__(self, id=None, nome=None, nota=None, matricula=None):
        self.id = id
        self.nome = nome
        self.nota = nota
        self.matricula = matricula

    def gerarMatricula():
        return ''.join([str(random.randint(0, 9)) for _ in range(11)])

    def visualizarNotas(self, usuario_id):
        con = BancoDados.conectarAlunos()
        cur = con.cursor()
        cur.execute("SELECT nota FROM alunos WHERE id = ?", (usuario_id,))
        resultado = cur.fetchone()
        con.close()
        return resultado if resultado else None
