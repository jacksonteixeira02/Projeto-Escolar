import sqlite3
from bancoDados import BancoDados
import random

class Aluno:
    def __init__(self, id, nome, nota, matricula):
        self.id = id
        self.nome = nome
        self.nota = nota
        self.matricula = matricula

    def gerarMatricula():
        return ''.join([str(random.randint(0, 9)) for _ in range(11)])