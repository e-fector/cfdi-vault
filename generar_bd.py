import sqlite3

from vault import dir_vault

import shutil
import os

os.remove(dir_vault + "facturas.db")
conn = sqlite3.connect(dir_vault + "facturas.db")

c = conn.cursor()

c.execute("CREATE TABLE facturas (id INTEGER PRIMARY KEY, cfdi, emisor, numero_factura,fecha NUMERIC)")
c.execute("CREATE UNIQUE INDEX facturas_id ON facturas(id ASC)")
c.execute("CREATE TABLE conceptos (id INTEGER PRIMARY KEY, cfdi TEXT, cantidad NUMERIC, noIdentificacion TEXT, descripcion TEXT, valorUnitario TEXT, importe NUMERIC)")
c.execute("CREATE INDEX conceptos_id ON conceptos(id ASC);")
