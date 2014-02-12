import os

def genera_folder(folder,rfc_emisor,anio,semana):
	

	folder = folder + str(anio) + "/"
	if not os.path.exists(folder): os.makedirs(folder)
	folder = folder + str(semana) + "/"
	if not os.path.exists(folder): os.makedirs(folder)
	folder = folder + str(rfc_emisor) + "/"
	if not os.path.exists(folder): os.makedirs(folder)
	
	return folder
	
