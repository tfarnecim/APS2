class Funcionario:

	def __init__(self, Cpf, Senha):
		self.Cpf = Cpf
		self.Senha = Senha

	def SetCpf(self, Cpf):
		self.Cpf = Cpf

	def GetCpf(self):
		return self.Cpf

	def SetSenha(self, Senha):
		self.Senha = Senha

	def GetSenha(self):
		return self.Senha
