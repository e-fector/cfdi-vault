# encoding: utf-8

from xml.etree import ElementTree
import codecs


class Factura:
	def __init__(self,xml):
		self.xml = xml
		self.arbol = ElementTree.parse(self.xml)
		#codecs.open(self.xml, encoding="UTF-8"))
		self.raiz = self.arbol.getroot()

		version = self.raiz.tag.replace("{http://www.sat.gob.mx/cfd/","").\
				replace("}Comprobante","")
		
		if version == "2":
			self.__class__ = FacturaCFD2
		elif version == "3":
			self.__class__ = FacturaCFDi3
		else:
			raise NotImplementedError()

			
		return None

	def GetFecha(self): 		
		raise NotImplementedError()
	def GetConceptos(self):
		raise NotImplementedError()
	def GetRFC(self): 
		raise NotImplementedError()
	def GetFolio(self): 
		raise NotImplementedError()
	def GetCFDi(self): 
		raise NotImplementedError()
	def TipoComprobante(self):
		self.raiz.attrib["tipoDeComprobante"]

	


class FacturaCFDi3(Factura):
	"""
	CFDi
	"""

	def __init__(self, xml):
		pass
		
	def GetFecha(self):
		return self.raiz.attrib["fecha"]

	def GetConceptos(self):
		conceptos = self.raiz.iter("{http://www.sat.gob.mx/cfd/3}Concepto")
		return conceptos

	def GetRFC(self): 
		Emisor = self.raiz.find("{http://www.sat.gob.mx/cfd/3}Emisor")
		return Emisor.attrib["rfc"]

	def GetFolio(self): 		
		return self.raiz.attrib["folio"]

		
	def GetCFDi(self): 
		Timbre = self.raiz.find("{http://www.sat.gob.mx/cfd/3}Complemento")
		a = Timbre.iter("{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital").next()
		return a.attrib["UUID"]



class FacturaCFD2(Factura):
	""" 
	Clase para representar una factura
	"""
	
	def __init__(self, xml):
		pass

	def GetFecha(self):
		return self.raiz.attrib["fecha"]

	def GetConceptos(self):
		conceptos = self.raiz.iter("{http://www.sat.gob.mx/cfd/2}Concepto")
		return conceptos

	def GetRFC(self):
		Emisor = self.raiz.find("{http://www.sat.gob.mx/cfd/2}Emisor")
		return Emisor.attrib["rfc"]
	
	def GetFolio(self):
		serie = self.raiz.attrib["serie"] 
		folio = self.raiz.attrib["folio"]
		ret = "%s-%s" % (serie, folio)
		return ret

	def GetCFDi(self):
		return self.GetFolio()

