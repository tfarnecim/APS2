from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QLabel, QListWidget, QTableWidgetItem, QListWidgetItem
from PyQt5 import QtGui
import datetime
from datetime import date
import PyQt5

from filme import Filme
from sessao import Sessao
from bilhete import Bilhete
from usuario import Usuario
from funcionario import Funcionario
import psycopg2
import os

def SELECT(lista,tabela,where,coluna,condicao):#a condição será apenas um =
	
	comando = "select "

	for i in range(len(lista)):
		
		if(i != 0):
			comando += ","

		comando += lista[i]
	
	comando += " from " + tabela + " "

	if(where == False):
		con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
		cur = con.cursor()
		cur.execute(comando+";")
		l = cur.fetchall()
		con.close()		
		return l

	numero = True

	comando += "where " + coluna + " = "

	for j in condicao:
		if(not j.isdigit()):
			numero = False

	if(numero):
		comando += condicao
	else:
		comando += "'" + condicao + "'"

	comando += ";"

	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute(comando)
	l = cur.fetchall()
	con.close()		
	return l


def INSERT(tabela,lista):

	comando = "insert into " + tabela + " values("

	for i in range(len(lista)):

		numero = True

		for j in lista[i]:
			if(not j.isdigit()):
				numero = False

		if(i != 0):
			comando += ","

		if(numero):
			comando += lista[i]
		else:
			comando += "'" + lista[i] + "'"

	comando += ");"

	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute(comando)
	con.commit()
	con.close()

def DELETE(tabela, coluna, condicao):
	comando = "delete from " + tabela + " where " + coluna + " = " + condicao
	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute(comando)
	con.commit()
	con.close()	


#Inicio das User Stories do programa

def RemoverFilme():
	
	p = -1

	linhas = TelaRemoverFilme.listWidget.count()

	for i in range(linhas):
		Item = TelaRemoverFilme.listWidget.item(i)
		if(Item.isSelected()):
			p = i
			break

	if(p==-1):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "Selecione algum filme para remover!")
		return 1

	ItemSelecionado = TelaRemoverFilme.listWidget.item(p)

	nome = ItemSelecionado.text()

	l = SELECT(["id"],"filme",True,"nome",nome)
	Id_filme = int(l[0][0])

	ids_sessao = SELECT(["id"], "sessao", True, "id_filme", str(Id_filme))
	
	for i in range(len(ids_sessao)):
		DELETE("bilhete","id_sessao",str(ids_sessao[i][0]))		

	DELETE("sessao","id_filme",str(Id_filme))
	DELETE("filme","id",str(Id_filme))
	
	TelaRemoverFilme.listWidget.takeItem(p)

	QMessageBox.about(TelaAdicionarFilme, "Aviso", "Filme removido com sucesso")
	return 1


def AdicionarFilme():

	nome = TelaAdicionarFilme.lineEdit.text()

	if(nome=="" or len(nome) > 40):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "O campo 'nome do filme' deve ser preenchido\ne deve conter no máximo 40 caracteres.")
		return 1

	l = SELECT(["nome"],"filme",True,"nome",nome)

	if(len(l) > 0):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "Um filme com este nome já está cadastrado no catálogo!")
		return 1

	strduracaohora = TelaAdicionarFilme.lineEdit_2.text()

	if(len(strduracaohora) == 0 or len(strduracaohora) > 1):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "O campo 'duração (horas)' deve ser preenchido\ne deve ter no máximo um dígito")
		return 1		

	if(not strduracaohora.isdigit()):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "O campo 'duração (horas)' deve ser um número")
		return 1

	strduracaominuto = TelaAdicionarFilme.lineEdit_3.text()

	if(len(strduracaominuto) == 0 or len(strduracaominuto) > 2):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "O campo 'duração (minutos)' deve ser preenchido\ne deve ter no máximo dois dígitos")
		return 1		

	if(len(strduracaominuto) == 1):
		strduracaominuto = "0" + strduracaominuto

	if((not strduracaominuto[0].isdigit()) or (not strduracaominuto[1].isdigit())):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "O campo 'duração (minutos)' deve ser um número")
		return 1

	sinopse = TelaAdicionarFilme.textEdit.toPlainText()

	if(sinopse=="" or len(sinopse) > 400):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "O campo 'sinopse do filme' deve ser preenchido\ne deve conter no máximo 400 caracteres.")
		return 1


	linhas = TelaAdicionarFilme.tableWidget.rowCount()

	if(linhas == 0):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "Você deve adicionar pelo menos uma sessão ao filme")
		return 1

	dia          = []
	mes          = []
	ano          = []
	numsala      = []
	iniciohora   = []
	iniciominuto = []

	for i in range(linhas):

		itemdata    = TelaAdicionarFilme.tableWidget.item(i,0)
		iteminicio  = TelaAdicionarFilme.tableWidget.item(i,1)
		itemnumsala = TelaAdicionarFilme.tableWidget.item(i,2)

		strdata    = itemdata.text()
		strinicio  = iteminicio.text()
		strnumsala = itemnumsala.text()

		dia.append(int(strdata[0]+strdata[1]))
		mes.append(int(strdata[3]+strdata[4]))
		ano.append(int(strdata[6]+strdata[7]+strdata[8]+strdata[9]))

		numsala.append(int(strnumsala))

		iniciohora.append(int(strinicio[0]+strinicio[1]))
		iniciominuto.append(int(strinicio[3]+strinicio[4]))

		#strduracaominuto
		#strduracaohora

	IDFILME = -1

	for i in range(1000000):
		
		l = SELECT(["id"],"filme",True,"id",str(i))

		if(len(l) == 0):
			IDFILME = i
			break

	INSERT("filme",[str(IDFILME),sinopse,nome,f.GetCpf(),strduracaominuto,strduracaohora])
	
	for i in range(linhas):

		IDSESSAO = -1
		
		for j in range(1000000):
		
			l = SELECT(["id"],"sessao",True,"id",str(j))

			if(len(l) == 0):
				IDSESSAO = j
				break

		INSERT("sessao",[str(IDSESSAO),str(dia[i]),str(mes[i]),str(ano[i]),str(numsala[i]),str(IDFILME),str(iniciohora[i]),str(iniciominuto[i])])

	QMessageBox.about(TelaAdicionarFilme, "Aviso", "O filme foi adicionado ao catálogo com sucesso!")
	
	TelaAdicionarFilme.lineEdit.setText("")
	TelaAdicionarFilme.lineEdit_2.setText("")
	TelaAdicionarFilme.lineEdit_3.setText("")

	while(TelaAdicionarFilme.tableWidget.rowCount() > 0):
		TelaAdicionarFilme.tableWidget.removeRow(0)
	
	TelaAdicionarFilme.textEdit.setText("")

	TelaAdicionarFilme.hide()
	TelaPrincipalFuncionario.show()
	return 1


def AdicionarSessao():

	data = TelaAdicionarSessao.calendarWidget.selectedDate()
	
	dia = data.day()
	mes = data.month()
	ano = data.year()

	data1 = date(int(ano),int(mes),int(dia))
	data2 = datetime.datetime.now()
	data3 = date(int(data2.year),int(data2.month),int(data2.day))

	data4 = data1 - data3

	if(data4.days < 2):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "A data da sessão deve estar a no mínimo 2 dias da hora atual.")
		return 1

	ok = True

	numsala = TelaAdicionarSessao.lineEdit_4.text()
	
	if(numsala == ""):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "O campo 'número da sala' deve ser preenchido")
		return 1

	iniciohora  = TelaAdicionarSessao.lineEdit_5.text()

	if(iniciohora == ""):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "O campo 'hora de início' deve ser preenchido")
		return 1

	iniciominuto = TelaAdicionarSessao.lineEdit_6.text()

	if(iniciominuto == ""):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "O campo 'minuto de início' deve ser preenchido")
		return 1

	for caractere in numsala:
		if(not caractere.isdigit()):
			ok = False
			break

	if(not ok):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "No campo 'número da sala', apenas são aceitos números")
		return 1

	for caractere in iniciohora:
		if(not caractere.isdigit()):
			ok = False
			break

	if(not ok):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "No campo 'horário de início(horas)', apenas são aceitos números no intervalo [0,23]")
		return 1

	for caractere in iniciominuto:
		if(not caractere.isdigit()):
			ok = False
			break

	if(not ok):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "No campo 'horário de início(minutos)', apenas são aceitos números no intervalo [0,59]")
		return 1

	NUMSALA = int(numsala)
	INICIOHORA  = int(iniciohora)
	INICIOMINUTO = int(iniciominuto)

	if(INICIOHORA > 23):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "No campo 'horário de início(horas)', apenas são aceitos números no intervalo [0,23]")
		return 1

	if(INICIOMINUTO > 59):
		QMessageBox.about(TelaAdicionarSessao, "Aviso", "No campo 'horário de início(minutos)', apenas são aceitos números no intervalo [0,59]")
		return 1

	ultimaposicao = TelaAdicionarFilme.tableWidget.rowCount()
	TelaAdicionarFilme.tableWidget.insertRow(ultimaposicao)

	datacorreta = ""

	if(len(str(dia)) < 2):
		datacorreta += '0'+str(dia)
	else:
		datacorreta += str(dia)

	datacorreta += '/'

	if(len(str(mes)) < 2):
		datacorreta += '0'+str(mes)
	else:
		datacorreta += str(mes)

	datacorreta += '/' + str(ano)

	#ARRUMANDO A HORA

	horacorreta = ""

	if(len(str(INICIOHORA)) < 2):
		horacorreta += '0'+str(INICIOHORA)
	else:
		horacorreta += str(INICIOHORA)

	horacorreta += ':'

	if(len(str(INICIOMINUTO)) < 2):
		horacorreta += '0'+str(INICIOMINUTO)
	else:
		horacorreta += str(INICIOMINUTO)	

	TelaAdicionarFilme.tableWidget.setItem(ultimaposicao, 0, QtWidgets.QTableWidgetItem(datacorreta))
	TelaAdicionarFilme.tableWidget.setItem(ultimaposicao, 1, QtWidgets.QTableWidgetItem(horacorreta))
	TelaAdicionarFilme.tableWidget.setItem(ultimaposicao, 2, QtWidgets.QTableWidgetItem(str(NUMSALA)))

	QMessageBox.about(TelaAdicionarSessao, "Aviso", "Sessão adicionada com sucesso!")

	TelaAdicionarSessao.lineEdit_4.setText("")
	TelaAdicionarSessao.lineEdit_5.setText("")
	TelaAdicionarSessao.lineEdit_6.setText("")

	TelaAdicionarSessao.hide()

def RemoverSessao():
	
	linhas = TelaAdicionarFilme.tableWidget.rowCount()

	l = -1

	for i in range (linhas):
		for j in range (3):

			item = QtWidgets.QTableWidgetItem()

			item = TelaAdicionarFilme.tableWidget.item(i,j)

			if(item.isSelected()):
				l = i
				i = linhas
				break

	if(l==-1):
		QMessageBox.about(TelaAdicionarFilme, "Aviso", "Selecione uma sessão para remover!")
		return 1

	TelaAdicionarFilme.tableWidget.removeRow(i-1)


def AdicionarsAdicionarf():
	TelaAdicionarSessao.hide()

def AdicionarfAdicionars():
	TelaAdicionarSessao.show()

def PrincipalAdicionar():
	TelaPrincipalFuncionario.hide()
	TelaAdicionarFilme.show()

def PrincipalRemover():
	
	TelaPrincipalFuncionario.hide()
	TelaRemoverFilme.show()

	TelaRemoverFilme.listWidget.clear()

	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute("select nome from filme;")
	l = cur.fetchall()
	con.close()

	for i in range(len(l)):
		Item = QListWidgetItem()
		Item.setText(str(l[i][0]))
		TelaRemoverFilme.listWidget.addItem(Item)


def RemoverPrincipal():
	TelaRemoverFilme.hide()
	TelaPrincipalFuncionario.show()

def AdicionarPrincipal():
	TelaAdicionarFilme.hide()
	TelaPrincipalFuncionario.show()

def LoginRegistro():
	TelaLoginFuncionario.hide()
	TelaRegistroFuncionario.show()

def RegistroLogin():
	TelaRegistroFuncionario.hide()
	TelaLoginFuncionario.show()

def Logar():

	Cpf   = TelaLoginFuncionario.lineEdit.text()
	Senha = TelaLoginFuncionario.lineEdit_2.text()

	#1 Sucesso
	#2 Cpf não cadastrado
	#3 Senha errada

	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute("select cpf,senha from funcionario where cpf='%s';"%(Cpf))
	l = cur.fetchall()
	con.close()

	if(len(l)==0):
		QMessageBox.about(TelaLoginFuncionario, "Aviso", "Este CPF nao foi cadastrado")
		return 2

	if(Senha != l[0][1]):
		QMessageBox.about(TelaLoginFuncionario, "Aviso", "Voce digitou a senha errada")
		return 3

	f.SetCpf(Cpf)
	f.SetSenha(Senha)

	TelaLoginFuncionario.hide()
	TelaPrincipalFuncionario.show()

	return 1

def Cadastro():

	cpf   = TelaRegistroFuncionario.lineEdit.text()
	senha = TelaRegistroFuncionario.lineEdit_2.text()

	#1 Sucesso
	#2 Campo vazio
	#3 CPF inválido
	#4 Senha inválida
	#5 CPF já cadastrado

	if(cpf=="" or senha==""):
		QMessageBox.about(TelaRegistroFuncionario, "Aviso", "Algum campo esta vazio!")
		return 2

	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute("select cpf from funcionario where cpf='%s';"%(cpf))
	l = cur.fetchall()
	con.close()

	if(len(l) > 0):
		QMessageBox.about(TelaRegistroFuncionario, "Aviso", "CPF já cadastrado!")
		return 5

	if(len(cpf) != 11):
		QMessageBox.about(TelaRegistroFuncionario, "Aviso", "CPF inválido")
		return 3

	inv = False
	for i in cpf:
		if(not i.isdigit()):
			inv = True
			break

	if(inv):
		QMessageBox.about(TelaRegistroFuncionario, "Aviso", "CPF inválido")
		return 3

	if(len(senha) < 5 or len(senha) > 15):
		QMessageBox.about(TelaRegistroFuncionario, "Aviso", "Senha inválida")
		return 4

	con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
	cur = con.cursor()
	cur.execute("insert into funcionario values('%s','%s');"%(cpf,senha))
	con.commit()
	con.close()

	QMessageBox.about(TelaRegistroFuncionario, "Aviso", "Funcionario Cadastrado com sucesso!")
	TelaRegistroFuncionario.hide()
	TelaLoginFuncionario.show()

	return 1


#cria o usuario que está usando o programa
f = Funcionario("","")

#cria a aplicação
app = QtWidgets.QApplication([])

#carrega todas as telas criadas
TelaLoginFuncionario     = uic.loadUi("Telas/TelaLoginFuncionario.ui")
TelaRegistroFuncionario  = uic.loadUi("Telas/TelaRegistroFuncionario.ui")
TelaPrincipalFuncionario = uic.loadUi("Telas/TelaPrincipalFuncionario.ui")
TelaAdicionarFilme       = uic.loadUi("Telas/TelaAdicionarFilme.ui")
TelaRemoverFilme         = uic.loadUi("Telas/TelaRemoverFilme.ui")
TelaAdicionarSessao      = uic.loadUi("Telas/TelaAdicionarSessao.ui")

#explica aos botões quais funções devem ser acionadas ao serem clicados
TelaRegistroFuncionario.pushButton.clicked.connect(Cadastro)
TelaRegistroFuncionario.pushButton_2.clicked.connect(RegistroLogin)

TelaLoginFuncionario.pushButton.clicked.connect(LoginRegistro)
TelaLoginFuncionario.pushButton_2.clicked.connect(Logar)

TelaPrincipalFuncionario.pushButton.clicked.connect(PrincipalAdicionar)  
TelaPrincipalFuncionario.pushButton_2.clicked.connect(PrincipalRemover)

TelaAdicionarFilme.pushButton.clicked.connect(AdicionarPrincipal)
TelaAdicionarFilme.pushButton_2.clicked.connect(AdicionarfAdicionars)
TelaAdicionarFilme.pushButton_3.clicked.connect(AdicionarFilme)
TelaAdicionarFilme.pushButton_4.clicked.connect(RemoverSessao)

TelaAdicionarSessao.pushButton.clicked.connect(AdicionarsAdicionarf)
TelaAdicionarSessao.pushButton_2.clicked.connect(AdicionarSessao)

TelaRemoverFilme.pushButton.clicked.connect(RemoverPrincipal)
TelaRemoverFilme.pushButton_2.clicked.connect(RemoverFilme)

#chama a tela em que o programa deve começar
TelaLoginFuncionario.show()

#começa o programa
app.exec()
