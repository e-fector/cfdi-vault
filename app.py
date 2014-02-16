from libs.bottle import route, run, template, static_file, request, get
from libs import bottle

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


class Paginador:
	def __init__(self, ruta, *args):
		self.__where__ = []
		self.ruta = ruta
		self.__template__ = ""
		self.__tabla__ = "facturas"
		self.__where_args__ = []
		self.__que__ = "*"
		self.__group__ = False
		bottle.route(self.ruta)(self.get)

	def get(self, *args, **kwargs):
		try:
			conn = sqlite3.connect(dir_vault + "facturas.db")
			c = conn.cursor()
			query = """SELECT %s FROM %s WHERE 1 """ % (self.__que__,self.__tabla__)

			# campos en clase
			for campo in self.__where__:
				if campo[1] == "LIKE": campo[2] = "%" + campo[2] + "%"
				query += "AND %s %s '%s' " % (campo[0],campo[1],campo[2])
			# campos en uri
			for articulo, valor in kwargs.iteritems():
				query += "AND %s = '%s' " % (articulo, valor)
			# campos en metrodo get
			for campo in self.__where_args__:
				if campo[1] == "LIKE": 
					q = "%" + request.query.get(campo[0]) + "%"
				else: 
					q = request.query.get(campo[0])
				query += "AND %s %s '%s'" % (campo[0],campo[1],q)

			if self.__group__:
				query += " GROUP BY %s " % self.__group__

			print query
			datos = c.execute(query)
			resultado = template(self.__template__, datos=datos.fetchall() )
			conn.close()
			return resultado
    
		except Exception as e:
			conn.close()
			return template('ERROR!<br /> {{error}}', error = str(e))
			
	def que(self,que):
		self.__que__ = que
		return self
		
	def tabla(self,tabla):
		self.__tabla__ = tabla
		return self

	def where(self,campo,operador,condicion):
		self.__where__.append((campo,operador,condicion))
		return self

	def where_args(self,campo,operador):
		self.__where_args__.append((campo,operador))
		return self

	def template(self,tmp):
		self.__template__ = tmp
		return self

	def group(self,group):
		self.__group__ = group
		return self

Paginador("/").template("templates/listado.html")
Paginador("/factura/<cfdi>.xml").tabla("conceptos").template("templates/factura.html")
Paginador("/concepto").tabla("conceptos").where_args("noIdentificacion","=")\
		.template("templates/concepto.html")
Paginador("/ajax").tabla("conceptos").where_args("noIdentificacion", "LIKE")\
		.template("templates/json.html")
Paginador("/listado/xproveedor").que("emisor").tabla("facturas").group("emisor")\
		.template("templates/xproveedor.html")

	
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
	

@route('/pasa')
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
