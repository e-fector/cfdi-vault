from libs.bottle import route, run, template, static_file, request, get
from libs import bottle

import sqlite3

from config import Configuracion
config = Configuracion()

class Pagina(object):
	def __init__(self, ruta, *args):
		bottle.route(self.ruta)(self.get)

	

class Paginador(Pagina):
	def __init__(self, ruta, *args):
		self.__where__ = []
		self.ruta = ruta
		self.__template__ = ""
		self.__tabla__ = "facturas"
		self.__where_args__ = []
		self.__que__ = "*"
		self.__group__ = False
		self.__limit__ = False
		bottle.route(self.ruta)(self.get)

	def get(self, *args, **kwargs):
		try:
			
			conn = sqlite3.connect(config.getVar("dir_vault") + "facturas.db")
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
			
			pagina = request.query.get("desde")
			anterior = -1
			siguiente = 50
			if pagina:
				query += " LIMIT %s, 50" % pagina
				siguiente = int(pagina) + 50
				anterior = int(pagina) - 50
			elif self.__limit__:
				query += " LIMIT %s " % self.__limit__
			else: 
				query += " LIMIT 50"

			datos = c.execute(query)
			resultado = template(self.__template__, {
					"datos":datos.fetchall(),
					"siguiente": siguiente,
					"anterior": anterior
					})
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

	def limit(self,limit):
		self.__limit__ = limit
		return self
