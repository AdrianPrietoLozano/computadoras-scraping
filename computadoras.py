import requests
from bs4 import BeautifulSoup
#import json

url_base = "https://www.smartprix.com/laptops/"
urls = [url_base]


for i in range(2, 100):
	url = url_base + "?page=" + str(i)
	urls.append(url)

lista = []
contador = 1
for pagina in urls:
	print()
	print(contador)
	print()
	try:
		r = requests.get(pagina)
		r.encoding = "utf-8"
	except Exception as e:
		break

	soup = BeautifulSoup(r.text, "html.parser")
	lista_compus = soup.find(class_="list-content")
	computadoras = lista_compus.find_all("li", {"class": "f-laptops"})

	for c in computadoras:
		compu = {
	        "nombre": c.find(class_="info").h2.a.text,
	        "marca": c.find(class_="info").h2.a.text.split(" ")[0],
	        "precio": c.find(class_="price").text.replace("₹", "").replace(",", ""),
	        "imagen": c.img["src"]
	        }
		especificaciones = c.find(class_="pros")
		if especificaciones:
			especificaciones = especificaciones.find_all("span")
			especificaciones2 = c.find(class_="cons")
			if especificaciones2:
				especificaciones.extend(especificaciones2.find_all("span"))
			n_especific = []

			for e in especificaciones:
				n_especific.append(e.text)

			compu["especi"] = n_especific

			lista.append(compu)
			print(compu)
	contador += 1

print(len(lista))




#print(len(computadoras))
"""
computadoras = soup.find_all(class_="f-laptops")
print(len(computadoras))
"""