from base_datos import conexion as con

#Funcion para agregar dueno
def agregar_dueno(dueno_dict):
    try:
        db = con.conectar()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO tabla_duenos (nombre, telefono, direccion) VALUES (?, ?, ?)",
            (dueno_dict["nombre"], dueno_dict["telefono"], dueno_dict["direccion"])
        )

        db.commit()
        id_generado = cursor.lastrowid
        db.close()
        return {"Respuesta": True, "Mensaje": "Dueño registrado", "id": id_generado}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": str(e)}

#Funcion para agregar mascota
def agregar_mascota(mascota):
    try:
        db = con.conectar()
        miCursor = db.cursor()
        
        # Convertir el objeto Mascota a diccionario
        mascota_dict = {
            "nombre": mascota.nombre,
            "especie": mascota.especie,
            "raza": mascota.raza,
            "edad": mascota.edad,
            "id_dueno": mascota.dueno.id
        }

        columnas = tuple(mascota_dict.keys())
        valores = tuple(mascota_dict.values())

        # Para que el string SQL funcione con columnas dinámicas, hay que formar bien la consulta
        campos = ", ".join(columnas)
        placeholders = ", ".join("?" for _ in valores)

        sql = f"INSERT INTO tabla_mascotas ({campos}) VALUES ({placeholders})"
        miCursor.execute(sql, valores)

        creada = miCursor.rowcount > 0
        db.commit()
        db.close()

        if creada:
            return {"Respuesta": True, "Mensaje": "Mascota registrada en la base de datos "}
        else:
            return {"Respuesta": False, "Mensaje": "Mascota no fue agregada a la base de datos "}

    except Exception as ex:
        try:
            db.close()
        except:
            pass
        return {"Respuesta": False, "Mensaje": str(ex)}
    
    
#Funcion de listar dueno por id especifico
def listar_dato_dueno(id_dueno):
    try:
        db = con.conectar()
        miCursor = db.cursor()

        sql="SELECT * FROM tabla_duenos WHERE id="+id_dueno
        miCursor.execute(sql)
        dueno= miCursor.fetchall()
        db.commit()
        if dueno:
            info= dueno[0]
            DatoBusqueda ={"id":info[0], "nombre":info[1], "telefono":info[2], "direccion":info[3]}
            miCursor.close()
            db.close()
            return{"Respuesta":True, "Mensaje":DatoBusqueda}
        else :
            miCursor.close()
            db.close()
            return{"Respuesta":False, "Mensaje":"no existe información en la base de datos"}

    except Exception as ex:
        miCursor.close()
        db.close()
        return{"Respuesta":False, "Mensaje":str(ex)}
    
#Funcion de listar mascota por id especifico
def listar_dato_mascota(id_mascota):
    try:
        db = con.conectar()
        miCursor = db.cursor()

        sql="SELECT * FROM tabla_mascotas WHERE id="+id_mascota
        miCursor.execute(sql)
        mascota= miCursor.fetchall()
        db.commit()
        if mascota:
            info= mascota[0]
            DatoBusqueda ={"id":info[0], "nombre":info[1], "especie":info[2], "raza":info[3], "edad":info[4], "id_dueno":info[5]}
            miCursor.close()
            db.close()
            return{"Respuesta":True, "Mensaje":DatoBusqueda}
        else :
            miCursor.close()
            db.close()
            return{"Respuesta":False, "Mensaje":"no existe información en la base de datos"}

    except Exception as ex:
        miCursor.close()
        db.close()
        return{"Respuesta":False, "Mensaje":str(ex)}
    
#Funcion de listar mascota con el dueño relacionado 
def listar_mascota_dueno():
    try:
        db = con.conectar()
        miCursor = db.cursor()

        sql="SELECT m.nombre, m.especie,m.raza,m.edad,d.nombre,d.telefono,d.direccion FROM tabla_mascotas m INNER JOIN tabla_duenos d ON m.id_dueno = d.id ORDER BY m.nombre"
        miCursor.execute(sql)
        mascota_dueno= miCursor.fetchall()
        db.commit()
        miCursor.close()
        db.close()

        if mascota_dueno:
            lista_mascotas_dueno = []
            for fila in mascota_dueno:
                mascota_info = {
                    "Nombre Mascota": fila[0],
                    "Especie": fila[1],
                    "Raza": fila[2],
                    "Edad": fila[3],
                    "Nombre Dueño": fila[4],
                    "Teléfono": fila[5],
                    "Dirección": fila[6]
                }
                lista_mascotas_dueno.append(mascota_info)
            
            return {"Respuesta": True, "Datos": lista_mascotas_dueno}
        else:
            return {"Respuesta": False, "Mensaje": "No hay datos en la base de datos"}

    except Exception as ex:
        miCursor.close()
        db.close()
        return{"Respuesta":False, "Mensaje":str(ex)}

#Funcion de listar mascota con el dueño relacionado filtrando
def obtener_mascotas_duenos_filtrado(nombre_mascota, nombre_dueno):
    try:
        db = con.conectar()
        miCursor = db.cursor()
        sql ="SELECT m.nombre, m.especie, m.raza, m.edad, d.nombre, d.telefono, d.direccion FROM tabla_mascotas m INNER JOIN tabla_duenos d ON m.id_dueno = d.id WHERE m.nombre LIKE ? AND d.nombre LIKE ? ORDER BY m.nombre"
        miCursor.execute(sql, (f"%{nombre_mascota}%", f"%{nombre_dueno}%"))
        mascota_dueno = miCursor.fetchall()
        db.commit()
        db.close()
        if mascota_dueno:
            return {"mascota_info": True, "Datos": [{
                    "Nombre Mascota": fila[0],
                    "Especie": fila[1],
                    "Raza": fila[2],
                    "Edad": fila[3],
                    "Nombre Dueño": fila[4],
                    "Teléfono": fila[5],
                    "Dirección": fila[6]
                } for fila in mascota_dueno]}
        else:
            return {"Respuesta": False, "Mensaje": "No hay datos en la base de datos"}

    except Exception as ex:
        return {"Respuesta": False, "Mensaje": str(ex)}

#Funcion de actualizar mascota con el dueño relacionado filtrando
def actualizar_mascota_dueno(nombre_mascota, nombre_dueno, nuevos_datos):
    try:
        db = con.conectar()
        miCursor = db.cursor()
        #Obtener el id de la mascota y del dueño
        miCursor.execute("SELECT m.id, d.id FROM tabla_mascotas m JOIN tabla_duenos d ON m.id_dueno = d.id WHERE m.nombre LIKE ? AND d.nombre LIKE ?", (f"%{nombre_mascota}%", f"%{nombre_dueno}%"))
        mascota_dueno = miCursor.fetchone()
        if not mascota_dueno:
            return {"Respuesta": False, "Mensaje": "No se encontró la mascota con ese dueño."}

        id_mascota, id_dueno = mascota_dueno

        #Actualizar mascota
        miCursor.execute("UPDATE tabla_mascotas SET nombre = ?, especie = ?, raza = ?, edad = ? WHERE id = ?", (nuevos_datos["nombre_mascota"], nuevos_datos["especie"], nuevos_datos["raza"], nuevos_datos["edad"], id_mascota))

        #Actualizar dueño
        miCursor.execute("UPDATE tabla_duenos SET nombre = ?, telefono = ?, direccion = ? WHERE id = ?", (nuevos_datos["nombre_dueno"], nuevos_datos["telefono"], nuevos_datos["direccion"], id_dueno))

        db.commit()
        db.close()

        return {"Respuesta": True, "Mensaje": "Mascota y dueño actualizados correctamente"}

    except Exception as ex:
        return {"Respuesta": False, "Mensaje": str(ex)}


#Funcion de eliminar dueño on id 
def eliminar_dueno(id_dueno):
    try:
        db = con.conectar()
        miCursor = db.cursor()
        #Obtener el id de la mascota y del dueño
        miCursor.execute("DELETE FROM tabla_duenos WHERE id = ?", (id_dueno))

        db.commit()
        db.close()

        return {"Respuesta": True, "Mensaje": "Dueño eliminada correctamente"}

    except Exception as ex:
        return {"Respuesta": False, "Mensaje": str(ex)}
 
#Funcion de eliminar mascota con el dueño relacionado filtrando
def eliminar_mascota_dueno(nombre_mascota, nombre_dueno, nuevos_datos):
    try:
        db = con.conectar()
        miCursor = db.cursor()
        #Obtener el id de la mascota y del dueño
        miCursor.execute("SELECT m.id, d.id FROM tabla_mascotas m JOIN tabla_duenos d ON m.id_dueno = d.id WHERE m.nombre LIKE ? AND d.nombre LIKE ?", (f"%{nombre_mascota}%", f"%{nombre_dueno}%"))
        mascota_dueno = miCursor.fetchone()

        if not mascota_dueno:
            return {"Respuesta": False, "Mensaje": "No se encontró la mascota con ese dueño."}

        id_mascota, id_dueno = mascota_dueno

        #Eliminar mascota
        miCursor.execute("DELETE FROM tabla_mascotas WHERE id = ?", (id_mascota))

        #Eliminar dueño
        miCursor.execute("DELETE FROM tabla_duenos WHERE id = ?", (id_dueno))

        db.commit()
        db.close()

        return {"Respuesta": True, "Mensaje": "Mascota y dueño eliminado correctamente"}

    except Exception as ex:
        return {"Respuesta": False, "Mensaje": str(ex)}
    