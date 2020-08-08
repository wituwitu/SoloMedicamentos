from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package
import requests

print("Accediendo a los sitios...")
URL = 'https://salcobrand.cl/products/antigripal-dia-oral-polvo-solido?default_sku=1990181'
URL2 = 'https://www.cruzverde.cl/tapsin-puro-sin-cafeina-paracetamol-500-mg-16-comprimidos/266050.html'

content = requests.get(URL)
content2 = requests.get(URL2)

print("Convirtiendo con Beautiful Soup...")
soup = BeautifulSoup(content.text, 'html.parser')
soup2 = BeautifulSoup(content2.text, 'html.parser')

print("Extrayendo precios...")
precioSB = soup.find("div", {"class": "normal full"})
precioSBStr = precioSB.get_text().replace("Ahora:","")

precioCV = soup2.find("span", {"class": "value"})
precioCVStr = precioCV.get_text().replace("(Oferta)","")

print("Precio Tapsin Salcobrand: " + precioSBStr)            # Print row with HTML formatting
print("Precio Tapsin CruzVerde: " + precioCVStr)            # Print row with HTML formatting

