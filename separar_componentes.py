import re


def separar_so(cadena):
	cadena = cadena.lower()
	m = re.search("windows|apple|linux|chrome|dos|mac|ubuntu", cadena, re.IGNORECASE)
	if(m):
		return m.group(0)
	return "N/A"

def separar_ram(cadena):
	capacidad = -1
	tipo = "N/A"
	cadena = cadena.lower()
	m = re.search("\d?\d?\d?\d.gb", cadena, re.IGNORECASE)
	if(m):
		capacidad = int(m.group(0).replace("gb", "").strip())
	else:
		m = re.search("\d?\d?\d?\d.mb", cadena, re.IGNORECASE)
		if(m):
			capacidad = float(m.group(0).replace("mb", "").strip()) / 1000.0

	m = re.search("ddr4|lpddr3|ddr3", cadena, re.IGNORECASE)
	if(m):
		tipo = m.group(0)
	return capacidad, tipo

def separar_almacenamiento(cadena):
	cadena = cadena.lower()
	m = re.search("\d?\d?\d?\d.tb", cadena, re.IGNORECASE)
	if(m):
		return int(m.group(0).replace("tb", "").strip()) * 1000
	else:
		m = re.search("\d?\d?\d?\d.gb", cadena, re.IGNORECASE)
		if(m):
			return int(m.group(0).replace("gb", "").strip())
	return -1

def separar_procesador(cadena):
	cadena = cadena.lower()
	marca = "N/A"
	m = re.search("intel|amd|xeon|itanium", cadena, re.IGNORECASE)
	if(m):
		cadena = m.group(0)
	return cadena