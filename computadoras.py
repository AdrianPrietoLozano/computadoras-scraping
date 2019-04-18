import requests
from bs4 import BeautifulSoup
import json
import re
from separar_componentes import *

"""
procesadores = [
"Intel Core i9 9th Gen",
"AMD A4-9125",
"AMD A9 APU",
"Intel Core i5 8th Gen",
"Intel Core i3 7th Gen",
"Ryzen 5",
"Intel Core i7 8th Gen",
"Intel Core i5 7th Gen",
"Intel Core i3 8th Gen",
"AMD APU A6",
"Intel Core i3 6th Gen",
"AMD Ryzen 5",
"N/A",
"Intel Pentium 8th Gen",
"Intel Core i5 5th Gen",
"Intel Core i9 8th Gen",
"AMD Ryzen 3",
"AMD A9 7th Gen",
"Intel Core i7 6th Gen",
"AMD A6-9210",
"AMD APU",
"AMD Radeon R5",
"AMD A6 APU 7th Gen",
"Ryzen 3",
"AMD APU E2 E2-6110",
"AMD AMD A9-9425",
"Intel Pentium Intel Pentium N4200",
"Intel Celeron",
"AMD APU A4",
"AMD A4-9120",
"2 GB AMD Graphics Card",
"Intel Core i7 7th Gen",
"AMD Dual Core E2 9000",
"AMD Ryzen 5 AMD Ryzen 5 3550H",
"AMD AMD A4-9120C",
"Intel Pentium Gold",
"Intel Atom Z8350",
"Intel Atom",
"Intel Core i5 8250U 8th Gen",
"Intel Core i5 8300H 8th Gen",
"Intel Atom QuadCore X5 Z8300",
"4 GB AMD Graphics Card",
"AMD Radeon R2",
"AMD A12 APU",
"Intel Pentium",
"Intel Pentium N4200",
"Intel Apollo Lake Intel Apollo Lake N3450",
"Intel Celeron Intel Celeron N3350",
"Intel Celeron 4th Gen",
"AMD E2-9000e",
"AMD APU E2",
"Intel Core M3 8th Gen",
"Intel Celeron N4000",
"AMD AMD A4",
"AMD AMD A9425",
"Intel Celeron 3855U",
"Dual Core Ryzen 5",
"Intel Core M3-7Y32 7th Gen",
"AMD Ryzen 5 2500U",
"AMD APU A4-9120",
"AMD A6-9225",
"AMD APU A9",
"Intel Pentium 4415U 7th Gen",
"Intel Apollo Lake Celeron",
"Intel Celeron Celeron Dual Core",
"AMD E2-9000",
"Intel Pentium N5000",
"AMD A9-9425",
"Intel Atom 7th Gen",
"Intel Celeron Dual Core N4000",
"Intel Core m3 7th Gen",
"Intel Celeron N3450",
"AMD APU FX"]
"""

TOTAL_COMPUTADORAS = 500


expresion = "Intel.Core.i\d|Intel.Atom|Intel.Celeron|Intel.Pentium|Intel.Apollo"\
			"AMD.APU.Ad|AMD.\S\d|AMD.Ryzen.\d|Ryzen \d"

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
		resultado = re.search(expresion, i, re.IGNORECASE)
		if resultado and procesador_encontrado == False:
			procesador_encontrado = True
			procesador_simple = resultado.group(0)

			if re.search("^Ryzen", procesador_simple, re.IGNORECASE):
				procesador_simple = "AMD " + procesador_simple; 

			compu["nombre_procesador"] = i.strip()
			compu["procesador_reducido"] = procesador_simple
			compu["marca_procesador"] = separar_procesador(procesador_simple)
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


lista = []
contador = 1

r = requests.get("https://es.coinmill.com/INR_MXN.html?INR=1")
soup = BeautifulSoup(r.text, "html.parser")
conversion = float(soup.find_all("input", {"class":"currencyField"})[1]["value"])
print(conversion)

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
	        "precio": float(c.find(class_="price").text.replace("₹", "").replace(",", "")) * conversion,
	        "imagen": c.img["src"],
	        "nombre_procesador": "N/A",
	        "marca_procesador": "N/A",
	        "procesador_reducido": "N/A",
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