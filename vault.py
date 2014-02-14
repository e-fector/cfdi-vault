# encoding: utf-8

import os
from factura_xml import Factura
from datetime import datetime
import calendar
import shutil
import sqlite3

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

					conn = sqlite3.connect(dir_vault + "facturas.db")
					
					c = conn.cursor()

					query = """INSERT INTO facturas (cfdi, emisor, numero_factura, fecha) 
                   VALUES ('%s', '%s', '%s', '%s' )""" % \
							(factura.GetCFDi(), rfc_emisor, factura.GetFolio(), \
								 calendar.timegm(fecha.utctimetuple()))

					c.execute(query)
					
					for concepto in conceptos:
						query = """INSERT INTO conceptos (cfdi,cantidad, noIdentificacion, descripcion,
                     valorUnitario, importe) VALUES ('%s','%s','%s','%s','%s','%s') """ % \
								(factura.GetCFDi(),concepto["cantidad"],concepto["noIdentificacion"],
								 concepto["descripcion"], concepto["valorUnitario"], concepto["importe"])
						c.execute(query)

					conn.commit()
					
					shutil.copy(dir_recepcion_de_archivos + filename,
											folder + filename)
					pdf = ""
					if ".xml" in filename:
						pdf = filename.replace(".xml", ".pdf")
					if ".XML" in filename:
						pdf = filename.replace(".XML", ".PDF")
					shutil.copy(dir_recepcion_de_archivos + pdf,
											folder + pdf)
					

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



