from libs.bottle import route, run, template

from datetime import datetime
import time

import pynotify

import sqlite3

from vault import dir_vault

@route('/listado')
def indexMain():
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = """SELECT * FROM facturas """
	datos = c.execute(query)
	return template("templates/listado.html", datos=datos.fetchall() )

@route('/factura/<id_factura>.xml')
def verFactura(id_factura):
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = """SELECT * FROM conceptos WHERE cfdi = "%s"  """ % id_factura
	datos = c.execute(query)
	return template("templates/factura.html", datos=datos.fetchall() )
	


@route('/')
def index():

	pynotify.init("Cfdi-vault")
	msg = pynotify.Notification("SERV","El servidor fue iniciado")
	msg.show()


	n = 0
	while True:
		yield template("<b>hola {{name }}" + str(datetime.now()) + "</b><br />", name=name)
		time.sleep(5)
		n += 1
		if n == 5:
			exit(0)
	
	#return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
