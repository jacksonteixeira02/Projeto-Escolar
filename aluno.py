import sqlite3
from bancoDados import BancoDados

class Aluno:
    def __init__(self, id, nome, nota, matricula):
        self.id = id
        self.nome = nome
        self.nota = nota
        self.matricula = matricula
