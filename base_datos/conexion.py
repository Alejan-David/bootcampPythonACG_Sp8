import sqlite3
import os


def conectar():
    miConexion = sqlite3.connect("bd_clinica_veterinaria")
    miCursor= miConexion.cursor()
    try:
    # Tabla dueños
        miCursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_duenos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL
        )
        ''')

        # Tabla mascotas
        miCursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especie TEXT NOT NULL,
            raza TEXT NOT NULL,
            edad INTEGER NOT NULL,
            id_dueno INTEGER NOT NULL,
            FOREIGN KEY (id_dueno) REFERENCES tabla_duenos (id)
        )
        ''')

        # Tabla consultas
        miCursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            motivo TEXT NOT NULL,
            diagnostico TEXT NOT NULL, 
            id_mascota INTEGER NOT NULL,
            FOREIGN KEY (id_mascota) REFERENCES tabla_mascotas(id)
        )
        ''')


        miConexion.commit()
        print("Base de datos creada con éxito ")

    except Exception as ex:
        print("Error en la conexión: ", ex)
    return miConexion