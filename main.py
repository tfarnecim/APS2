from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QLabel, QListWidget, QTableWidgetItem, QListWidgetItem
from PyQt5 import QtGui
import datetime
from datetime import datetime,timedelta

from usuario import Usuario
from sessao import Sessao
from filme import Filme
from funcionario import Funcionario
from bilhete import Bilhete

import psycopg2

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

def CarregarFilmes():#para um filme aparecer na lista ele deve ter pelo menos uma sessão futura

    f = SELECT(["nome","id"],"filme",False,"","")

    TelaListarFilmes.listWidget.clear()

    for i in range(len(f)):
        
        s = SELECT(["ano","mes","dia","inicio_hora","inicio_minuto"],"sessao",True,"id_filme",str(f[i][1]))
        agora = datetime.now()
        cnt = 0
        
        for j in range(len(s)):
            dataj = datetime(int(s[j][0]),int(s[j][1]),int(s[j][2]),int(s[j][3]),int(s[j][4]))
            delta = timedelta(hours = 1)
            dataj = dataj - delta
            if(agora < dataj):
                cnt += 1

        if(cnt > 0):
            Item = QListWidgetItem()
            Item.setText(str(f[i][0]))
            TelaListarFilmes.listWidget.addItem(Item)

def CarregarBilhetes():
    
    #b = SELECT(["id_sessao"],"bilhete",True,"cpf_usuario",c.GetCpf())

    con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
    cur = con.cursor()
    cur.execute("select id_sessao,id from bilhete where cpf_usuario='%s'"%(c.GetCpf()))
    b = cur.fetchall()
    con.close()  

    TelaMeusBilhetes.listWidget.clear()

    for i in range(len(b)):

        ID_SESSAO = int(b[i][0])
        id_bilhete = int(b[i][1])

        l = SELECT(["ano","mes","dia","inicio_hora","inicio_minuto","id_filme"],"sessao",True,"id",str(ID_SESSAO))

        data  = datetime(int(l[0][0]),int(l[0][1]),int(l[0][2]),int(l[0][3]),int(l[0][4]))
        delta = timedelta(hours = 1)
        data  = data + delta
        
        dia = str(data.day)
        mes = str(data.month)
        ano = str(data.year)
        hora = str(data.hour)
        minuto = str(data.minute)

        if(datetime.now() < data):
            Item = QListWidgetItem()
            f = SELECT(["nome"],"filme",True,"id",str(l[0][5]))
            Item.setText(str(f[0][0]) + " | " + str(id_bilhete))
            TelaMeusBilhetes.listWidget.addItem(Item)

def CarregarSessoes():

    l = SELECT(["ano","mes","dia","inicio_hora","inicio_minuto","nsala","id"],"sessao",True,"id_filme",str(f.GetId()))

    TelaSelecionarSessao.listWidget.clear()

    for i in range(len(l)):

        data  = datetime(int(l[i][0]),int(l[i][1]),int(l[i][2]),int(l[i][3]),int(l[i][4]))
        delta = timedelta(hours = 1)
        data  = data - delta
        
        dia = str(data.day)
        mes = str(data.month)
        ano = str(data.year)
        hora = str(data.hour)
        minuto = str(data.minute)

        if(len(dia) == 1):
            dia = "0" + dia

        if(len(mes) == 1):
            mes = "0" + mes

        if(len(hora) == 1):
            hora = "0" + hora

        if(len(minuto) == 1):
            minuto = "0" + minuto

        if(datetime.now() < data):
            Item = QListWidgetItem()
            Item.setText(str(l[i][6]) + " | " + dia + "/" + mes + "/" + ano + " PM " + hora + ":" + minuto)
            TelaSelecionarSessao.listWidget.addItem(Item)

def RegistrarCliente():
    
    cpf = TelaRegistroCliente.lineEdit.text()
    email = TelaRegistroCliente.lineEdit_2.text()
    senha   = TelaRegistroCliente.lineEdit_3.text()

    #1 Sucesso
    #2 Campo vazio
    #3 CPF inválido
    #4 Senha inválida
    #5 Email inválido
    #6 CPF já cadastrado

    if(cpf=="" or email=="" or senha==""):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "Algum campo esta vazio!")
        return 2

    l = SELECT(["cpf"],"usuario",True,"cpf",cpf)

    if(len(l) > 0):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "CPF ja cadastrado")
        return 6

    if(len(cpf) != 11):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "CPF invalido")
        return 3

    inv = False
    for i in cpf:
        if(not i.isdigit()):
            inv = True
            break

    if(inv):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "CPF invalido")
        return 3

    if(len(senha) < 5 or len(senha) > 15):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "Senha Invalida\n\nPara uma senha ser valida ela deve\nConter de 5 a 15 caracteres")
        return 4

    cnt = 0
    p = -1

    for i in range(len(email)):
        if(email[i]=='@'):
            cnt+=1
            p = i

    if(cnt!=1):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "Email invalido")
        return 5

    if(p==0 or p==len(email)-1):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "Email invalido")
        return 5

    con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
    cur = con.cursor()
    cur.execute("insert into usuario values('%s','%s','%s');"%(cpf,email,senha))
    con.commit()
    con.close()

    QMessageBox.about(TelaRegistroCliente, "Aviso", "Usuario cadastrado com Sucesso !!")

    TelaRegistroCliente.hide()
    TelaLoginCliente.show()

    return 1


def LogarCliente():

    Cpf   = TelaLoginCliente.lineEdit.text()
    Senha = TelaLoginCliente.lineEdit_3.text()

    #1 Sucesso
    #2 Cpf não cadastrado
    #3 Senha errada

    con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
    cur = con.cursor()
    cur.execute("select cpf,senha,email from usuario where cpf='%s';"%(Cpf))
    l = cur.fetchall()
    con.close()

    if(len(l)==0):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "Este CPF nao foi cadastrado")
        return 2

    if(Senha != l[0][1]):
        QMessageBox.about(TelaRegistroCliente, "Aviso", "Voce Digitou a senha errada")
        return 3

    c.SetCpf(Cpf)
    c.SetSenha(Senha)
    c.SetEmail(l[0][2])

    TelaLoginCliente.hide()
    TelaPrincipalCliente.show()

    return 1

def VoltaPrincipal():
    TelaPrincipalCliente.hide()
    TelaLoginCliente.show()

def PrincipalListar():

    TelaPrincipalCliente.hide()
    TelaListarFilmes.show()
    CarregarFilmes()

def ListarPrincipal():

    TelaListarFilmes.hide()
    TelaPrincipalCliente.show()

def ListarDescricao():

    size = TelaListarFilmes.listWidget.count()

    p = -1

    for i in range(size):
        Item = TelaListarFilmes.listWidget.item(i)
        if(Item.isSelected()):
            p = i
            break

    if(p==-1):
        QMessageBox.about(TelaListarFilmes,"Aviso","Selecione algum filme para ver as informações!")
        return 1

    ItemSelecionado = TelaListarFilmes.listWidget.item(p)

    nome = ItemSelecionado.text()

    l = SELECT(["nome","descricao","duracao_hora","duracao_minuto"],"filme",True,"nome",nome)

    TelaDescricaoFilme.label.setText(str(l[0][0]))
    TelaDescricaoFilme.label_7.setText("Duração: "+str(l[0][2])+" hora(s) e "+str(l[0][3])+" minuto(s)")
    TelaDescricaoFilme.label_5.setText(str(l[0][1]))

    TelaListarFilmes.hide()
    TelaDescricaoFilme.show()   

def DescricaoListar():
    TelaDescricaoFilme.hide()   
    TelaListarFilmes.show()

def UsaPrincipal():
    CarregarBilhetes()
    TelaPrincipalCliente.hide()
    TelaMeusBilhetes.show()

def RegistrarLogar():
    TelaRegistroCliente.hide()
    TelaLoginCliente.show()

def LogarRegistrar():
    TelaLoginCliente.hide()
    TelaRegistroCliente.show()

def ListarSelecionarSessao():
    
    p = -1

    linhas = TelaListarFilmes.listWidget.count()

    for i in range(linhas):
        Item = TelaListarFilmes.listWidget.item(i)
        if(Item.isSelected()):
            p = i
            break

    if(p==-1):
        QMessageBox.about(TelaListarFilmes, "Aviso", "Selecione algum filme!")
        return 1

    ItemSelecionado = TelaListarFilmes.listWidget.item(p)

    x = SELECT(["id"],"filme",True,"nome",ItemSelecionado.text())
    ID = int(x[0][0])
    filme = SELECT(["id","nome","descricao","cpf_funcionario"],"filme",True,"id",str(ID))

    f.SetId(ID)
    f.SetNome(str(filme[0][1]))
    f.SetDescricao(str(filme[0][2]))
    f.SetFuncionario(str(filme[0][3]))

    CarregarSessoes()

    TelaListarFilmes.hide()
    TelaSelecionarSessao.show()

    TelaSelecionarSessao.label.setText("Sessões disponíveis para " + ItemSelecionado.text())

def SelecionarSessaoCartaoCredito():

    p = -1

    linhas = TelaSelecionarSessao.listWidget.count()

    for i in range(linhas):
        Item = TelaSelecionarSessao.listWidget.item(i)
        if(Item.isSelected()):
            p = i
            break

    if(p==-1):
        QMessageBox.about(TelaSelecionarSessao, "Aviso", "Selecione alguma Sessão!")
        return 1

    ItemSelecionado = TelaSelecionarSessao.listWidget.item(p)

    texto = ItemSelecionado.text()

    p = -1

    for i in range(len(texto)):
        if(texto[i] == "|"):
            p = i-1
            break


    strnum = ""

    for i in range(p):
        strnum += texto[i]

    id_sessao = int(strnum)

    l = SELECT(["id"],"bilhete",True,"id_sessao",str(id_sessao))

    if(len(l) > 0):
        QMessageBox.about(TelaSelecionarSessao, "Aviso", "Você já tem um bilhete para esta sessão!")
        return 1

    s.SetId(id_sessao)

    TelaSelecionarSessao.hide()
    TelaCartaoCredito.show()

    return 1

def CartaoCreditoSelecionarSessao():

    CarregarSessoes()
    TelaCartaoCredito.hide()    
    TelaSelecionarSessao.show()
    
    return 1

def SelecionarSessaoListarFilmes():
    
    CarregarFilmes()
    TelaSelecionarSessao.hide()
    TelaListarFilmes.show()

def EfetuarCompra():
    
    cartao = TelaCartaoCredito.lineEdit.text()

    ok = True

    for i in cartao:
        if(not i.isdigit()):
            ok = False
            break

    if(not ok):
        QMessageBox.about(TelaCartaoCredito, "Aviso", "Apenas são aceitos números!")
        return 1

    if(len(cartao) != 16):
        QMessageBox.about(TelaCartaoCredito, "Aviso", "O número do cartão deve conter 16 dígitos!")
        return 1

    ID_BILHETE = -1

    for i in range(1000000):
        l = SELECT(["id"],"bilhete",True,"id",str(i))
        if(len(l)==0):
            ID_BILHETE = i
            break

    #INSERT("bilhete",[str(ID_BILHETE),"'"+c.GetCpf()+"'",str(s.GetId())])
    con = psycopg2.connect(database='Cinema', user='postgres', password='postgres')
    cur = con.cursor()
    cur.execute("insert into bilhete values(%d,'%s',%d);"%(ID_BILHETE,c.GetCpf(),s.GetId()))
    con.commit()
    con.close()

    QMessageBox.about(TelaCartaoCredito, "Aviso", "Compra efetuada com sucesso!")

    TelaCartaoCredito.hide()
    TelaPrincipalCliente.show()


def MeusBilhetesInfoBilhete():

    p = -1

    linhas = TelaMeusBilhetes.listWidget.count()

    for i in range(linhas):
        Item = TelaMeusBilhetes.listWidget.item(i)
        if(Item.isSelected()):
            p = i
            break

    if(p==-1):
        QMessageBox.about(TelaMeusBilhetes, "Aviso", "Selecione algum bilhete!")
        return 1

    ItemSelecionado = TelaMeusBilhetes.listWidget.item(p)
    texto = ItemSelecionado.text()

    p = -1

    for i in range(len(texto)):
        if(texto[i]=="|"):
            p = i+2
            break

    strnum = ""

    for i in range(p,len(texto)):
        strnum += texto[i]

    ID_BILHETE = int(strnum)

    bilhetezinho = SELECT(["id_sessao"],"bilhete",True,"id",str(ID_BILHETE))

    ID_SESSAO = int(bilhetezinho[0][0])
    
    sessaozinha  = SELECT(["dia","mes","ano","inicio_hora","inicio_minuto","nsala","id_filme"],"sessao",True,"id",str(ID_SESSAO))

    ID_FILME = int(sessaozinha[0][6])

    filmezinho   = SELECT(["nome"],"filme",True,"id",str(ID_FILME))

    dia = str(sessaozinha[0][0])
    mes = str(sessaozinha[0][1])
    ano = str(sessaozinha[0][2])

    hora   = str(sessaozinha[0][3])
    minuto = str(sessaozinha[0][4])

    sala = str(sessaozinha[0][5])

    nome = str(filmezinho[0][0])

    if(len(dia) < 2):
        dia = "0" + dia

    if(len(mes) < 2):
        mes = "0" + mes

    if(len(hora) < 2):
        hora = "0" + hora

    if(len(minuto) < 2):
        minuto = "0" + minuto

    TelaDescricaoBilhete.label.setText("Informações " + nome)
    TelaDescricaoBilhete.label_2.setText("Número da sessão " + str(ID_SESSAO))
    TelaDescricaoBilhete.label_3.setText("Identificador do bilhete: " + str(ID_BILHETE))
    TelaDescricaoBilhete.label_4.setText("Data: " + dia + "/" + mes + "/" + ano)
    TelaDescricaoBilhete.label_5.setText("Sala: " + sala)
    TelaDescricaoBilhete.label_6.setText("Horário de início: " + hora + ":" + minuto)

    TelaMeusBilhetes.hide()
    TelaDescricaoBilhete.show()    


def InfoBilheteMeusBilhetes():
    CarregarBilhetes()
    TelaDescricaoBilhete.hide()
    TelaMeusBilhetes.show()

def MeusBilhetesPrincipal():
    TelaMeusBilhetes.hide()
    TelaPrincipalCliente.show()

#cria a aplicação
app = QtWidgets.QApplication([])

#carrega todas as telas criadas
#exemplo
TelaRegistroCliente   = uic.loadUi("Telas/TelaRegistroCliente.ui")
TelaLoginCliente      = uic.loadUi("Telas/TelaLoginCliente.ui")
TelaPrincipalCliente  = uic.loadUi("Telas/TelaPrincipalCliente.ui")
TelaListarFilmes      = uic.loadUi("Telas/TelaListarFilmes.ui")
TelaDescricaoFilme    = uic.loadUi("Telas/TelaDescricaoFilme.ui")
TelaSelecionarSessao  = uic.loadUi("Telas/TelaSelecionarSessao.ui")
TelaCartaoCredito     = uic.loadUi("Telas/TelaCartaoCredito.ui")
TelaDescricaoBilhete  = uic.loadUi("Telas/TelaDescricaoBilhete.ui") 
TelaMeusBilhetes      = uic.loadUi("Telas/TelaMeusBilhetes.ui")

#explica aos botões quais funções devem ser acionadas ao serem clicados

TelaRegistroCliente.pushButton.clicked.connect(RegistrarCliente)
TelaRegistroCliente.pushButton_2.clicked.connect(RegistrarLogar)

TelaLoginCliente.pushButton.clicked.connect(LogarCliente)
TelaLoginCliente.pushButton_2.clicked.connect(LogarRegistrar)

TelaPrincipalCliente.pushButton.clicked.connect(PrincipalListar)
TelaPrincipalCliente.pushButton_2.clicked.connect(UsaPrincipal)
TelaPrincipalCliente.pushButton_3.clicked.connect(VoltaPrincipal)

TelaListarFilmes.pushButton.clicked.connect(ListarPrincipal)
TelaListarFilmes.pushButton_2.clicked.connect(ListarDescricao)
TelaListarFilmes.pushButton_3.clicked.connect(ListarSelecionarSessao)

TelaDescricaoFilme.pushButton.clicked.connect(DescricaoListar)

TelaSelecionarSessao.pushButton.clicked.connect(SelecionarSessaoCartaoCredito)
TelaSelecionarSessao.pushButton_2.clicked.connect(SelecionarSessaoListarFilmes)

TelaCartaoCredito.pushButton.clicked.connect(CartaoCreditoSelecionarSessao)
TelaCartaoCredito.pushButton_2.clicked.connect(EfetuarCompra)

TelaMeusBilhetes.pushButton.clicked.connect(MeusBilhetesPrincipal)
TelaMeusBilhetes.pushButton_2.clicked.connect(MeusBilhetesInfoBilhete)

TelaDescricaoBilhete.pushButton.clicked.connect(InfoBilheteMeusBilhetes)


#cria o usuario que está usando o programa

c = Usuario("","","")
f = Filme(0,"","","")
s = Sessao(0,0,0,0,0,0)
id_bilhete = -1

#chama a tela em que o programa deve começar
TelaLoginCliente.show()

#começa o programa
app.exec()