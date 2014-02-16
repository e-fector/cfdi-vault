print "Estabilizando APP"
import time
time.sleep(10)

print "Arrancando Navegador"
import webbrowser
new = 2 # open in a new tab, if possible

# open a public URL, in this case, the webbrowser docs
url = "http://localhost:8001"
webbrowser.open(url,new=new)

print "Ready"
