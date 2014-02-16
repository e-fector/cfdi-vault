from libs.bottle import route, run, template, static_file, request, get

from datetime import datetime
import time

import pynotify

import sqlite3

from vault import dir_vault

@route('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@route('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@route('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@get('/ajax')
def indexMain():
	args = request.query.get("input")
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = "SELECT * FROM conceptos WHERE noIdentificacion LIKE \"%"+args+"%\" GROUP BY noIdentificacion "
	datos = c.execute(query)
	return template("templates/json.html", datos=datos.fetchall() )

@route('/concepto')
def indexMain():
	args = request.query.get("concepto")
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = """SELECT * FROM conceptos WHERE noIdentificacion = "%s" """ % args
	datos = c.execute(query)
	return template("templates/concepto.html", datos=datos.fetchall() )


@route('/')
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
	
@route("/listado/xmes")
def xmeses():
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = """SELECT fecha FROM facturas ORDER by fecha ASC LIMIT 1 """
	datos = c.execute(query)
	import time
	fecha = time.gmtime(int(datos.fetchone()[0]))
	
	return template("templates/xmes.html", {"datos":fecha, "hoy":datetime.now()} )

@route("/listado/xmes/<ano>/<mes>/<orden>")
def xmes(ano,mes,orden):
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	import calendar
	from dateutil.relativedelta import relativedelta

	primer_dia_de_mes_fecha = datetime.strptime("%s-%s-%s" % (ano, mes,1), "%Y-%m-%d")
	ultimo_dia_de_mes_fecha = primer_dia_de_mes_fecha + relativedelta(months=1)
	primer_dia_de_mes = calendar.timegm(primer_dia_de_mes_fecha.utctimetuple())
	ultimo_dia_de_mes = calendar.timegm(ultimo_dia_de_mes_fecha.utctimetuple())
	
	query = """SELECT * FROM facturas WHERE fecha > "%s" AND fecha < "%s" ORDER by %s ASC""" % \
			(primer_dia_de_mes, ultimo_dia_de_mes, orden)
	datos = c.execute(query)
	
	return template("templates/xmes_listado.html", {"datos":datos} )
	

@route("/listado/xproveedor")
def xproveedor():
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = """SELECT emisor FROM facturas  GROUP BY emisor """
	datos = c.execute(query)
	return template("templates/xproveedor.html", {"datos":datos} )

@route("/listado/xproveedor/<proveedor>")
def xproveedor(proveedor):
	conn = sqlite3.connect(dir_vault + "facturas.db")
	c = conn.cursor()
	query = """SELECT * FROM facturas WHERE emisor = "%s" ORDER BY fecha DESC """ % proveedor
	datos = c.execute(query)
	return template("templates/proveedor.html", {"datos":datos} )


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

run(host='localhost', port=8001)
