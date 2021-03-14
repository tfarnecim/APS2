from filme import Filme

class Sessao:

	def __init__(self, Filme, NumeroDaSala, Dia, Mes, Ano, Id):
		self.NumeroDaSala = NumeroDaSala
		self.Dia = Dia
		self.Mes = Mes
		self.Ano = Ano
		self.Filme = Filme
		self.Id = Id

	def GetFilme(self):
		return self.Filme

	def SetNumeroDaSala(self, NumeroDaSala):
		self.NumeroDaSala = NumeroDaSala

	def GetNumeroDaSala(self):
		return self.NumeroDaSala

	def SetDia(self, Dia):
		self.Dia = Dia

	def GetDia(self):
		return self.Dia

	def SetMes(self, Mes):
		self.Mes = Mes

	def GetMes(self):
		return self.Mes

	def SetAno(self, Ano):
		self.Ano = Ano

	def GetAno(self):
		return self.Ano

	def SetId(self, Id):
		self.Id = Id

	def GetId(self):
		return self.Id

	