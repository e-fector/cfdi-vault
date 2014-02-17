import sqlite3

import shutil
import os

from config import Configuracion
config = Configuracion()

os.remove(config.getVar("dir_vault") + "facturas.db")
conn = sqlite3.connect(config.getVar("dir_vault") + "facturas.db")

c = conn.cursor()

c.execute("CREATE TABLE facturas (id INTEGER PRIMARY KEY, cfdi, emisor, receptor, numero_factura,fecha NUMERIC, tipo)")
c.execute("CREATE UNIQUE INDEX facturas_id ON facturas(id ASC)")
c.execute("CREATE TABLE conceptos (id INTEGER PRIMARY KEY, cfdi TEXT, cantidad NUMERIC, noIdentificacion TEXT, descripcion TEXT, valorUnitario TEXT, importe NUMERIC)")
c.execute("CREATE INDEX conceptos_id ON conceptos(id ASC);")

conn.close()
