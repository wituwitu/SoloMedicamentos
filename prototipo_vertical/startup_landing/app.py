from flask import Flask, render_template, jsonify, request
import re

from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package
import requests

app = Flask(__name__)
def salcobrand(nombre_medicamento):

  if (nombre_medicamento.lower() == "paracetamol"):
    url_paracetamol= "https://salcobrand.cl/products/kitadol-500mg"
    content_paracetamol = requests.get(url_paracetamol)
    soupP = BeautifulSoup(content_paracetamol.text, 'html.parser')
    precio_paracetamol = soupP.find("div", {"class": "normal full"})
    precioPStr = precio_paracetamol.get_text().replace("Ahora:", "")
    return int(''.join(filter(str.isdigit, precioPStr))), url_paracetamol

  elif nombre_medicamento.lower() == "ibuprofeno":
    url_ibuprofeno = "https://salcobrand.cl/products/ibuprofeno-400mg-oral-solido"
    content_ibuprofeno = requests.get(url_ibuprofeno)
    soupI = BeautifulSoup(content_ibuprofeno.text, 'html.parser')
    precio_ibuprofeno = soupI.find("div", {"class": "normal full"})
    precioIStr = precio_ibuprofeno.get_text().replace("Ahora:", "")
    return int(''.join(filter(str.isdigit, precioIStr))), url_ibuprofeno

  elif nombre_medicamento.lower() == "mascarilla":
    url_mascarilla= "https://salcobrand.cl/products/mascarilla-plana-desechable"
    content_mascarilla=requests.get(url_mascarilla)
    soupM = BeautifulSoup(content_mascarilla.text, 'html.parser')
    precio_mascarilla=soupM.find("div", {"class": "normal full"})
    precioMStr = precio_mascarilla.get_text().replace("Ahora:","")
    return int(''.join(filter(str.isdigit, precioMStr))), url_mascarilla
  
  else:
    return 0



def cruzverde(nombre_medicamento):
  query = nombre_medicamento.lower()
  url = "https://www.cruzverde.cl/busqueda?q={}".format(query)

  #print("Buscando en " + url)
  page = requests.get(url)
  page_text = page.text

  bloque = page_text[page_text.find("<div class=\"tile-body px-3 pt-3 pb-0 d-flex flex-column pb-0\""):]
  bloque_marca = bloque[bloque.find("<a href="):]
  marca = bloque_marca[bloque_marca.find(">") + 1 : bloque_marca.find("</a>")].strip()
  bloque_nombre = bloque_marca[bloque_marca.find("<a class="):]
  nombre = bloque_nombre[bloque_nombre.find(">") + 1 : bloque_nombre.find("</a>")].strip()
  bloque_precio = bloque_nombre[bloque_nombre.find("<div class=\"price\">"):]
  precio = bloque_precio[bloque_precio.find("$") : (bloque_precio.find("$") + bloque_precio.find("</span>"))].strip()
  precio = precio[:precio.find("</span>")]

  oferta = False
  if "(Oferta)" in precio:
      oferta = True
      precio = precio[:precio.find("\n")]

  return int(''.join(filter(str.isdigit, precio))), url


def farmazon(nombre_medicamento):
  if (nombre_medicamento.lower() == "paracetamol"):
    url_paracetamol= "https://www.farmazon.cl/alividol.html"
    content_paracetamol = requests.get(url_paracetamol)
    soupP = BeautifulSoup(content_paracetamol.text, 'html.parser')
    precio_paracetamol = soupP.find("span", {"class": "price"})
    precioPStr = precio_paracetamol.get_text()
    return int(''.join(filter(str.isdigit, precioPStr))), url_paracetamol

  elif nombre_medicamento.lower() == "ibuprofeno":
    url_ibuprofeno = "https://www.farmazon.cl/ibupirac-lc-400-mg-x-10-capsulas-blandas.html"
    content_ibuprofeno = requests.get(url_ibuprofeno)
    soupI = BeautifulSoup(content_ibuprofeno.text, 'html.parser')
    precio_ibuprofeno = soupI.find("span", {"class": "price"})
    precioIStr = precio_ibuprofeno.get_text()
    return int(''.join(filter(str.isdigit, precioIStr))), url_ibuprofeno

  elif nombre_medicamento.lower() == "mascarilla":
    url_mascarilla= "https://www.farmazon.cl/categorias/muncare-mascarilla-3-pliegues-x-50-unidades.html"
    content_mascarilla=requests.get(url_mascarilla)
    soupM = BeautifulSoup(content_mascarilla.text, 'html.parser')
    precio_mascarilla=soupM.find("span", {"class": "price"})
    precioMStr = precio_mascarilla.get_text()
    return int(''.join(filter(str.isdigit, precioMStr))), url_mascarilla
  
  else:
    return 0



@app.route('/_searchMed')
def searchMed():
	medicamentos_disponibles = ["paracetamol", "ibuprofeno", "mascarilla"]
	nombre_medicamento = request.args.get('medName', '')
	if(nombre_medicamento.lower() in medicamentos_disponibles):
		result = {"Salcobrand":{ "price": salcobrand(nombre_medicamento)[0], "url": salcobrand(nombre_medicamento)[1]}, "Cruz Verde": { "price": cruzverde(nombre_medicamento)[0], "url": cruzverde(nombre_medicamento)[1]}, "Farmazon": { "price": farmazon(nombre_medicamento)[0], "url": farmazon(nombre_medicamento)[1]}}
	else:
		result = {}
	return jsonify(result=result)

@app.route('/_calculate')
def calculate():
    a = request.args.get('number1', '0')
    operator = request.args.get('operator', '+')
    b = request.args.get('number2', '0')
    # validate the input data
    m = re.match(r'^\-?\d*[.]?\d*$', a)
    n = re.match(r'^\-?\d*[.]?\d*$', b)

    if m is None or n is None or operator not in '+-*/':
        return jsonify(result='Error!')

    if operator == '/':
        result = eval(a + operator + str(float(b)))
    else:
        result = eval(a + operator + b)
    return jsonify(result=result)


@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run(debug=True)