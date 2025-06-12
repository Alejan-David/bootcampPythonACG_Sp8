from base_datos.conexion import conectar
def inicializar_bd():
    miConexion = conectar()
    miCursor = miConexion.cursor()
    try:
        # Crear tabla_duenos
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla_duenos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                documento TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                activo TEXT NOT NULL DEFAULT 's'
            );
        ''')

        # Crear tabla_mascotas
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla_mascotas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT NOT NULL,
                raza TEXT NOT NULL,
                edad INTEGER NOT NULL,
                id_dueno INTEGER NOT NULL,                
                activo TEXT NOT NULL DEFAULT 's',
                FOREIGN KEY (id_dueno) REFERENCES tabla_duenos(id)
            );
        ''')

         # Crear tabla_consultas
        miCursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            motivo TEXT NOT NULL,
            diagnostico TEXT NOT NULL, 
            id_mascota INTEGER NOT NULL,
            activo TEXT NOT NULL DEFAULT 's',
            FOREIGN KEY (id_mascota) REFERENCES tabla_mascotas(id)
        );
        ''')

        miConexion.commit()
    finally:
        miConexion.close()
