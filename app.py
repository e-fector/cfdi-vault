from libs.bottle import route, run, template, static_file, request, get
from libs import bottle

from datetime import datetime
import time

import sqlite3

from config import Configuracion
config = Configuracion()

@route('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@route('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@route('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

from handler import Paginador

Paginador("/").template("templates/listado.html")
Paginador("/factura/<cfdi>.xml").tabla("conceptos").template("templates/factura.html")
Paginador("/concepto").tabla("conceptos").where_args("noIdentificacion","=")\
		.template("templates/concepto.html")
Paginador("/ajax").tabla("conceptos").where_args("noIdentificacion", "LIKE")\
		.template("templates/json.html").limit(6)

Paginador("/listado/xproveedor").que("emisor").tabla("facturas").group("emisor")\
		.template("templates/xproveedor.html")
Paginador("/listado/xproveedor/<emisor>").tabla("facturas")\
		.template("templates/proveedor.html")

Paginador("/listado/xreceptor").que("receptor").tabla("facturas").group("receptor")\
		.template("templates/xreceptor.html")
Paginador("/listado/xreceptor/<receptor>").tabla("facturas")\
		.template("templates/receptor.html")

@route("/listado/xmes/<ano>/<mes>/<orden>")
def xmes(ano,mes,orden):
	conn = sqlite3.connect(config.getVar("dir_vault") + "facturas.db")
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
	
@route("/listado/xmes")
def xmeses():
	conn = sqlite3.connect(config.getVar("dir_vault") + "facturas.db")
	c = conn.cursor()
	query = """SELECT fecha FROM facturas ORDER by fecha ASC LIMIT 1 """
	datos = c.execute(query)
	import time
	fecha = time.gmtime(int(datos.fetchone()[0]))
	conn.close()
	return template("templates/xmes.html", {"datos":fecha, "hoy":datetime.now()} )

#Ejecutamos servidor
if __name__ == "__main__":
	run(host='localhost', port=8001)
