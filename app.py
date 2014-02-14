from libs.bottle import route, run, template

from datetime import datetime
import time

import pynotify

@route('/hello/<name>')
def index(name):

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
