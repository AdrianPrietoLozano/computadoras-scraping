import requests
from bs4 import BeautifulSoup
import json
import re
from separar_componentes import *


TOTAL_COMPUTADORAS = 500


def buscar_especificaciones(c):
	especificaciones = c.find(class_="pros")
	if especificaciones:
		especificaciones = especificaciones.find_all("span")
		especificaciones2 = c.find(class_="cons")
		if especificaciones2:
			especificaciones.extend(especificaciones2.find_all("span"))
		n_especific = []
		for e in especificaciones:
			n_especific.append(e.text)	
		return n_especific
	return []


def completar_compu(compu):
	procesador_encontrado = False
	storage_encontrado = False
	for i in especificaciones:
		if re.search("Intel.Apollo|Intel.Atom|Intel.Celeron|Intel.Core.M|Intel.Core.i\d|Intel.Pentium|AMD|Xeon|itanium|Ryzen", i, re.IGNORECASE) and procesador_encontrado == False:
			procesador_encontrado = True
			#print("Procesador:", i)
			compu["nombre_procesador"] = i.strip()
			compu["marca_procesador"] = separar_procesador(i)
			continue
		if re.search("RAM", i, re.IGNORECASE):
			#print("Ram:", i)
			compu["capacidad_ram"], compu["tipo_ram"] = separar_ram(i)
			continue
		if re.search("windows|apple|linux|chrome|dos|mac|ubuntu", i, re.IGNORECASE):
			#print("Sistema operativo:", i)
			compu["so"] = separar_so(i)
			continue
		if re.search("hard.disk|SSD", i, re.IGNORECASE) and storage_encontrado == False:
			#print("Almacenamiento:", i)
			compu["almacenamiento"] = separar_almacenamiento(i)
			storage_encontrado = True
			continue



url_base = "https://www.smartprix.com/laptops/"
urls = [url_base]


"""
for i in range(2, 100):
	url = url_base + "?page=" + str(i)
	urls.append(url)
"""

lista = []
contador = 1
while len(lista) < TOTAL_COMPUTADORAS:
	try:
		r = requests.get(url_base + "?page=" + str(contador))
		r.encoding = "utf-8"
	except Exception as e:
		print("break")
		break

	print(contador)

	soup = BeautifulSoup(r.text, "html.parser")
	lista_compus = soup.find(class_="list-content")
	computadoras = lista_compus.find_all("li", {"class": "f-laptops"})

	for c in computadoras:
		compu = {
	        "nombre": c.find(class_="info").h2.a.text,
	        "marca": c.find(class_="info").h2.a.text.split(" ")[0],
	        "precio": c.find(class_="price").text.replace("₹", "").replace(",", ""),
	        "imagen": c.img["src"],
	        "nombre_procesador": "N/A",
	        "marca_procesador": "N/A",
	        "so": "N/A",
	        "almacenamiento": "-1",
	        "capacidad_ram": "-1",
	        "tipo_ram": "N/A"
	    	}
		especificaciones = buscar_especificaciones(c)

		if(especificaciones):
			completar_compu(compu)
			lista.append(compu)
			
	contador += 1

print("Total:", len(lista))

with open("computadoras.json", "w") as archivo:
	json.dump(lista, archivo, sort_keys=False, indent=4)
