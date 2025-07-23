import sqlite3

conUsuario = sqlite3.connect("bancoDados/usuarios.db")
curUsuario = conUsuario.cursor()

def conectarUsuarios():
    return sqlite3.connect("bancoDados/usuarios.db")

class Usuarios:
    def __init__(self, id, email, senha):
        self.id = id
        self.email = email
        self.senha = senha

    def logar(self, email, senha):
        conUsuario = conectarUsuarios()
        curUsuario = conUsuario.cursor()
        curUsuario.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
        conUsuario.commit()
        conUsuario.close()

