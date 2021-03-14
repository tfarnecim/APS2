from funcionario import Funcionario

class Filme:

	def __init__(self, Id, Nome, Descricao, Funcionario):
		self.Id = Id
		self.Nome = Nome
		self.Descricao = Descricao
		self.Funcionario = Funcionario

	def SetFuncionario(self,Funcionario):
		self.Funcionario = Funcionario

	def GetFuncionario(self):
		return self.Funcionario

	def SetId(self, Id):
		self.Id = Id

	def GetId(self):
		return self.Id

	def SetNome(self, Nome):
		self.Nome = Nome

	def GetNome(self):
		return self.Nome

	def SetDescricao(self, Descricao):
		self.Descricao = Descricao

	def GetDescricao(self):
		return self.Descricao
