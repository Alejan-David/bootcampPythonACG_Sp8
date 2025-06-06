import sqlite3

def conectar():
    return sqlite3.connect("bd_clinica_veterinaria")
