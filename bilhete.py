from usuario import Usuario
from sessao import Sessao

class Bilhete:
	
	def __init__(self, Id, Usuario, Sessao):
		self.Id = Id
		self.Usuario = Usuario
		self.Sessao = Sessao

	def GetUsuario(self):
		return self.Usuario

	def GetSessao(self):
		return self.Sessao

	def GetId(self):
		return self.Id

	'''

	NAO FAZ SENTIDO

	def SetId(self, Id):
		self.Id = Id

	'''