import sqlite3

class Configuracion(object):
	def __init__(self):
		conn = sqlite3.connect("config.db")
		c = conn.cursor()
		self.conn = c

	def getVar(self,nombre):
		query = "SELECT valor FROM configuracion WHERE variable = '%s'" % nombre
		print query
		res = self.conn.execute(query)
		return res.fetchone()[0]
		

if __name__ == "__main__":
	conn = sqlite3.connect("config.db")
	c = conn.cursor()
	c.execute("CREATE TABLE configuracion (id INTEGER PRIMARY KEY, variable, valor);")

	configuraciones = []
	configuraciones.append(("dir_vault", \
			raw_input('Directorio donde se van a guardar las facturas: ')))
	configuraciones.append(("dir_recepcion_de_archivos", \
			raw_input('Almacen temporal de archivos: ')))
	
	for valores in configuraciones:
		q = "INSERT INTO configuracion (variable,valor) VALUES ('%s','%s');" %\
				(valores[0],valores[1])
		print q
		c.execute(q)
		conn.commit()
		
	conn.close()
