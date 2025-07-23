import sqlite3

conAluno = sqlite3.connect("bancoDados/alunos.db")
curAluno = conAluno.cursor()

def conectarAlunos():
    return sqlite3.connect("bancoDados/alunos.db")
class Aluno:
    def __init__(self, id, nome, nota, matricula):
        self.id = id
        self.nome = nome
        self.nota = nota
        self.matricula = matricula