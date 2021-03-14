class Usuario:

	def __init__(self, Cpf, Email, Senha):
		self.Cpf = Cpf
		self.Email = Email
		self.Senha = Senha

	def SetCpf(self, Cpf):
		self.Cpf = Cpf

	def GetCpf(self):
		return self.Cpf

	def SetEmail(self, Email):
		self.Email = Email

	def GetEmail(self):
		return self.Email

	def SetSenha(self, Senha):
		self.Senha = Senha

	def GetSenha(self):
		return self.Senha

	
