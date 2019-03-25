import glob
import json
import mysql.connector


def buscar_ram(tipo, capacidad):
	select = "SELECT * FROM ram WHERE tipo=%s AND capacidad=%s"
	cursor.execute(select, (tipo, capacidad))
	return cursor.fetchall()

def insertar_ram(tipo, capacidad):
	insert = "INSERT INTO ram(tipo, capacidad) VALUES(%s, %s)"
	cursor.execute(insert, (tipo, capacidad))
	conexion.commit()
	return cursor.lastrowid

def buscar_so(nombre_so):
	select = "SELECT * FROM sistema_operativo WHERE nombre=%s"
	cursor.execute(select, (nombre_so, ))
	return cursor.fetchall()

def insertar_so(nombre_so):
	insert = "INSERT INTO sistema_operativo(nombre) VALUES(%s)"
	cursor.execute(insert, (nombre_so, ))
	conexion.commit()
	return cursor.lastrowid

def buscar_procesador(nombre, marca):
	select = "SELECT * FROM procesador WHERE nombre=%s AND marca=%s"
	cursor.execute(select, (nombre, marca))
	return cursor.fetchall()

def insertar_procesador(nombre, marca):
	insert = "INSERT INTO procesador(nombre, marca) VALUES(%s, %s)"
	cursor.execute(insert, (nombre, marca))
	conexion.commit()
	return cursor.lastrowid

def buscar_almacenamiento(capacidad):
	select = "SELECT * FROM almacenamiento WHERE capacidad=%s"
	cursor.execute(select, (capacidad, ))
	return cursor.fetchall()

def insertar_almacenamiento(capacidad):
	insert = "INSERT INTO almacenamiento(capacidad) VALUES(%s)"
	cursor.execute(insert, (capacidad, ))
	conexion.commit()
	return cursor.lastrowid

def buscar_computadora(nombre, marca, id_ram, id_so, id_almacenamiento, id_procesador):
	select = "SELECT * FROM computadora WHERE nombre=%s AND marca=%s AND id_ram=%s AND "\
				"id_so=%s AND id_almacenamiento=%s AND id_procesador=%s"
	cursor.execute(select, (nombre, marca, id_ram, id_so, id_almacenamiento, id_procesador))
	return cursor.fetchall()

def insertar_computadora(nombre, marca, precio, ram, so, almacenamiento, procesador):
	insert = "INSERT INTO computadora(nombre, precio, marca, id_ram, "\
			"id_procesador, id_so, id_almacenamiento) VALUES(%s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(insert, (nombre, precio, marca, ram, procesador, so, almacenamiento))
	conexion.commit()
	return cursor.lastrowid

def actualizar_precio(id_computadora, nuevo_precio):
	update = "UPDATE computadora SET precio=%s WHERE id=%s"
	cursor.execute(update, (nuevo_precio, id_computadora))
	conexion.commit()

files = glob.glob("computadoras.json") # regresa una lista
print(files)

conexion = mysql.connector.connect(
	user="usuario",
	password="12345",
	database="proyecto_computadoras"
	)
cursor = conexion.cursor()

with open(files[0]) as f:
	computadoras = json.load(f) # lista de diccionarios

for computadora in computadoras:
	
	#RAM
	rows = buscar_ram(computadora["tipo_ram"], computadora["capacidad_ram"])
	if len(rows) == 0: # no existe la ram en la BD
		id_ram = insertar_ram(computadora["tipo_ram"], computadora["capacidad_ram"])
	else: # ya existe la ram
		id_ram = rows[0][0]

	#SO
	rows = buscar_so(computadora["so"])
	if len(rows) == 0: # no existe el sistema operativo en la BD
		id_so = insertar_so(computadora["so"])
	else: # ya existe el SO
		id_so = rows[0][0]

	#ALMACENAMIENTO
	rows = buscar_almacenamiento(computadora["almacenamiento"])
	if len(rows) == 0: # no existe el almacenamiento en la BD
		id_almacenamiento = insertar_almacenamiento(computadora["almacenamiento"])
	else: # ya existe el SO
		id_almacenamiento = rows[0][0]

	#PROCESADOR
	try:
		rows = buscar_procesador(computadora["nombre_procesador"], computadora["marca_procesador"])
		if len(rows) == 0: # no existe el procesador en la BD
			id_procesador = insertar_procesador(computadora["nombre_procesador"], computadora["marca_procesador"])
		else: # ya existe el SO
			id_procesador = rows[0][0]
	except Exception as e:
		print("Esta computadora no tiene procesador. No se agregará")
		continue


	#COMPUTADORA
	rows = buscar_computadora(computadora["nombre"],
							computadora["marca"],
							id_ram,
							id_so,
							id_almacenamiento,
							id_procesador)
	if len(rows) == 0: # no existe la computadora en la BD
		id_computadora = insertar_computadora(computadora["nombre"],
											computadora["marca"],
											computadora["precio"], # falta convertirlo a pesos
											id_ram,
											id_so,
											id_almacenamiento,
											id_procesador)
	else: # si ya existe la computadora se actualiza el precio
		id_computadora = rows[0][0]
		actualizar_precio(id_computadora, computadora["precio"])


conexion.close()
#print(computadoras)