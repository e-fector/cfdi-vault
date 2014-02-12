# encoding: utf-8

import os
from factura_xml import Factura
from datetime import datetime
import shutil


from utils import genera_folder

dir_recepcion_de_archivos = "/home/sebastianavina/Dropbox/facturas_attachments/"
dir_vault = "/home/sebastianavina/facturas_vault/"

if __name__ == '__main__':
	for dirname, dirnames, filenames in os.walk(dir_recepcion_de_archivos):
		for filename in filenames:
			if ".xml" in filename or ".XML" in filename:
				try:
					factura = Factura(dir_recepcion_de_archivos + filename)
					rfc_emisor = factura.GetRFC()

					fecha = datetime.strptime(factura.GetFecha(), "%Y-%m-%dT%H:%M:%S")

					anio = fecha.year
					semana = fecha.isocalendar()[1]

					folder = genera_folder(dir_vault,rfc_emisor,anio,semana)

					conceptos = []

					for concepto in  factura.GetConceptos():
						if "noIdentificacion" in concepto.attrib:
							identificacion = concepto.attrib["noIdentificacion"]
						else:
							identificacion = ""
						conceptos.append( {
								"cantidad":concepto.attrib["cantidad"],
								"unidad":concepto.attrib["unidad"],
								"noIdentificacion":identificacion,
								"descripcion":concepto.attrib["descripcion"],
								"valorUnitario":concepto.attrib["valorUnitario"],
								"importe":concepto.attrib["importe"],
								})

					print conceptos
					
					

					
					shutil.copy(dir_recepcion_de_archivos + filename,
											folder + filename)
					pdf = ""
					if ".xml" in filename:
						pdf = filename.replace(".xml", ".pdf")
					if ".XML" in filename:
						pdf = filename.replace(".XML", ".PDF")
					shutil.copy(dir_recepcion_de_archivos + pdf,
											folder + pdf)
					
					print folder + filename



				except Exception as e:
					info = open(dir_recepcion_de_archivos + filename,"r")
					txt = ""
					print ""
					print "ERROR"
					for line in info:
						txt += line
					#print txt 
					print e
					print dir_recepcion_de_archivos + filename
					#exit(0)
					
					
				#exit(0)



