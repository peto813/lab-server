# -*- coding: utf-8 -*-

# encoding=utf8  
from bs4 import BeautifulSoup
import requests, csv

def cne_object( nacionalidad, cedula ):
	cedula = str(cedula.upper()).strip(nacionalidad.upper()).strip()
	nacionalidad = str(nacionalidad).strip().upper()
	try:
		#url = 'http://www.cne.gov.ve/web/registro_electoral/ce.php?nacionalidad=V&cedula=16717365'
		url =  'http://www.cne.gov.ve/web/registro_electoral/ce.php?nacionalidad=%s&cedula=%s' %( nacionalidad, cedula )
		res = requests.get( url, timeout=3 )
		soup = BeautifulSoup(res.text, "html.parser")
		cne_data_soup =  soup.findAll('td', align="left")
		a_list = ['nombre', 'municipio', 'estado', 'parroquia', 'centro', 'direcc']
		element_list = [soup.findAll('td', string = lambda x: x and item in x.lower() )[0].parent for item in a_list]
		data_x = {}
		for item in element_list:
			tags= item.findAll('td')
			if tags and len(tags)>=2:
				if 'direcc' in tags[0].text.encode('utf-8').lower():
					data_x['direccion'] = tags[1].text
				else:
					data_x[tags[0].text.lower().replace(':', '')] = tags[1].text
		data_x['apellidos'] = data_x['nombre'].split(' ', 2)[2]
		data_x['nombres'] = " ".join(data_x['nombre'].split(" ", 2)[:2])
		return data_x
	except:
		return {}


def seniat_object(rif):
	try:
		rif = str(rif).strip().strip('-').lower()
		url = 'http://contribuyente.seniat.gob.ve/getContribuyente/getrif?rif=%s' %(str(rif))
		res = requests.get( url )
		#print res.text
		soup = BeautifulSoup(res.text, "lxml")
		response = {
			'nombre' : soup.findAll('rif:nombre')[0].get_text().split('(')[0],
			'agente_retencion': soup.findAll('rif:agenteretencioniva')[0].get_text(),
			'tasa' :  soup.findAll('rif:tasa')[0].get_text(),
			'contribuyente_IVA' : soup.findAll('rif:contribuyenteiva')[0].get_text()
		}
		return response

	except:
		return {}