cfdi-vault
==========

Aplicacion para ordenar archivos XML

Archivos Principales
---

- Configurar aplicacion:

    `python config.py`

- Correr el servidor:

    `python app.py`
    
- Cargar archivos:

    `python vault.py`

- Descargar archivos correo electrónico:

    `python descarga_facturas.py`

Para imprimir todos los conceptos usar:
    sqlite3 -header -csv ~/facturas_vault/facturas.db "select * from conceptos;" > conceptos.txt

