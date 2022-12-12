#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from AnimatedGIF import *
import os
import linsimpy
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

class Server(object):
   
    def __init__(self):
        self.space = linsimpy.TupleSpaceEnvironment()

        self.nuvens = []

        self.startSpace()

    def startSpace(self):
        self.space.out(("Nuvens", tuple(self.nuvens)))

    def createNuvem(self, name, hostName, vmName, procName):
        auxNuvens = self.space.inp(("Nuvens", object))
        aux = list(auxNuvens[1])
        aux.append(name)
        self.space.out(("Nuvens", tuple(aux)))
        self.createHost(name, hostName, vmName, procName)
        # print("Nuvens: " + str(aux))

    def createHost(self, nameNuvem, nameHost, nameVm, nameProc):
        host = [nameHost]
        self.space.out(("Host", nameNuvem, tuple(host)))
        self.createVm(nameHost, nameVm, nameProc)

    def createVm(self, nameHost, nameVm, nameProc):
        vm = [nameVm]
        self.space.out(("Vm", nameHost, tuple(vm)))
        self.createProc(nameVm, nameProc)

    def createProc(self, nameVm, nameProc):
        proc = [nameProc]
        message = []
        self.space.out(("Proc", nameVm, tuple(proc)))
        self.space.out(("Message", nameProc, tuple(message)))

    def sendMessage(self, senderProc, receiverProc, message):
        messages = self.space.inp(("Message", receiverProc, object))
        aux = list(messages[2])
        aux.append("<" + senderProc + "> " + message)

        self.space.out(("Message", receiverProc, tuple(aux)))

    def readMessages(self, procName):
        messages = self.space.rdp(("Message", procName, object))
        return list(messages[2])

    def addHost(self, nuvemName, newHost):
        host = self.space.inp(("Host", nuvemName, object))
        aux = list(host[2])

        for i in aux:
            if i == newHost:
                return False

        aux.append(newHost)
        self.space.out(("Host", nuvemName, tuple(aux)))
        return True

    def removeHost(self, nuvemName, nameHost):
        host = self.space.inp(("Host", nuvemName, object))
        aux = list(host[2])
        aux.remove(nameHost)
        self.space.out(("Host", nuvemName, tuple(aux)))

    def deleteHost(self, nuvemName, hostName):
        host = self.space.inp(("Vm", hostName, object))
        aux = list(host[2])

        if aux != []:
            self.space.out(("Vm", hostName, tuple(aux)))
            return False

        self.removeHost(nuvemName, hostName)
        return True

    def migrateHost(self, oldNuvem, newNuvem, hostName):
        nNuvem = self.space.inp(("Host", newNuvem, object))
        aux = list(nNuvem[2])

        for i in aux:
            if i == hostName:
                self.space.out(("Host", newNuvem, tuple(aux)))
                return False #sinaliza para mudar o nome

        self.space.out(("Host", newNuvem, tuple(aux)))
        self.addHost(newNuvem, hostName)
        self.removeHost(oldNuvem, hostName)
        return True

    def listHost(self, nuvemName):
        host = self.space.rdp(("Host", nuvemName, object))
        return list(host[2])

    def addVm(self, hostName, newVm):
        vm = self.space.inp(("Vm", hostName, object))
        aux = list(vm[2])

        for i in aux:
            if i == newVm:
                return False

        aux.append(newVm)
        self.space.out(("Vm", hostName, tuple(aux)))
        return True

    def removeVm(self, hostName, nameVm):
        vm = self.space.inp(("Vm", hostName, object))
        aux = list(vm[2])
        aux.remove(nameVm)
        self.space.out(("Vm", hostName, tuple(aux)))

    def deleteVm(self, hostName, vmName):
        vm = self.space.inp(("Proc", vmName, object))
        aux = list(vm[2])

        if aux != []:
            self.space.out(("Proc", vmName, tuple(aux)))
            return False

        self.removeVm(hostName, vmName)
        return True

    def migrateVm(self, oldHost, newHost, vmName):
        nHost = self.space.inp(("Vm", newHost, object))
        aux = list(nHost[2])

        for i in aux:
            if i == vmName:
                self.space.out(("Vm", newHost, tuple(aux)))
                return False #sinaliza para mudar o nome

        self.space.out(("Vm", newHost, tuple(aux)))
        self.addVm(newHost, vmName)
        self.removeVm(oldHost, vmName)
        return True

    def listVm(self, hostName):
        vm = self.space.rdp(("Vm", hostName, object))
        return list(vm[2])

    def addProc(self, vmName, newProc):
        proc = self.space.inp(("Proc", vmName, object))
        aux = list(proc[2])

        for i in aux:
            if i == newProc:
                return False

        newMessage = []
        aux.append(newProc)
        self.space.out(("Proc", vmName, tuple(aux)))
        self.space.out(("Message", newProc, tuple(newMessage)))
        return True

    def removeProc(self, vmName, nameProc):
        proc = self.space.inp(("Proc", vmName, object))
        messages = self.space.inp(("Message", nameProc, object))
        aux = list(proc[2])
        aux.remove(nameProc)
        self.space.out(("Proc", vmName, tuple(aux)))

    def migrateProc(self, oldVm, newVm, procName):
        nVm = self.space.inp(("Proc", newVm, object))
        aux = list(nVm[2])

        for i in aux:
            if i == procName:
                self.space.out(("Proc", newVm, tuple(aux)))
                return False #sinaliza para mudar o nome

        self.space.out(("Proc", newVm, tuple(aux)))
        self.addProc(newVm, procName)
        self.removeProc(oldVm, procName)
        return True

    def listProc(self, vmName):
        proc = self.space.rdp(("Proc", vmName, object))
        return list(proc[2])

    def deleteNuvem(self, name):
        nuvem = self.space.inp(("Host", name, object))
        aux = list(nuvem[2])

        if aux != []:
            self.space.out(("Host", name, tuple(aux)))
            return False

        auxNuvens = self.space.inp(("Nuvens", object))
        aux = list(auxNuvens[1])
        aux.remove(name)
        self.space.out(("Nuvens", tuple(aux)))
        # print("Nuvens: " + str(aux))

    def listNuvem(self):
        auxNuvens = self.space.rdp(("Nuvens", object))
        # print(auxNuvens)

        return list(auxNuvens[1])

    def addNewHost(self, nuvemName, newHost):
        host = self.space.inp(("Host", nuvemName, object))
        aux = list(host[2])
        for i in aux:
            if i == newHost:
                return False

        aux.append(newHost)
        self.space.out(("Host", nuvemName, tuple(aux)))
        self.space.out(("Vm", newHost, tuple([])))
        return True
    
    def addNewVm(self, hostName, addnewVm):
        vm = self.space.inp(("Vm", hostName, object))
        aux = list(vm[2])

        for i in aux:
            if i == addnewVm:
                return False

        aux.append(addnewVm)
        self.space.out(("Vm", hostName, tuple(aux)))
        self.space.out(("Proc", addnewVm, tuple([])))
        return True
    
    def addNewProc(self, vmName, addnewProc):
        proc = self.space.inp(("Proc", vmName, object))
        aux = list(proc[2])

        for i in aux:
            if i == addnewProc:
                return False

        newMessage = []
        aux.append(addnewProc)
        self.space.out(("Proc", vmName, tuple(aux)))
        self.space.out(("Message", addnewProc, tuple(newMessage)))
        return True






class ServerScreen:

    def __init__(self, newServer):
        self.server = newServer
        self.numNuvem = 0
        self.maxNuvem = 6
        self.root = Tk()
        self.root.withdraw()

        self.mainScreen() #mudou

        self.root.mainloop()

    def resource_path(self, relative_path):
      try:
          base_path = sys._MEIPASS
      except Exception:
          base_path = os.path.abspath(".")

      return os.path.join(base_path, relative_path)
    

    def mainScreen(self):
        
        newWindow = Toplevel(self.root)
        newWindow.title("Ambientes Multinuvens")
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.protocol("WM_DELETE_WINDOW", lambda:self.close(newWindow))


        
        gif_bg_asset_url = self.resource_path('recursos/gifs/chat_bubble_GIF.gif') 
        lbl_with_my_gif = AnimatedGif(newWindow, gif_bg_asset_url,0.30)
        lbl_with_my_gif.config(bg='#70ad47')
        lbl_with_my_gif.place(x=135, y=40)
        lbl_with_my_gif.start()


        lbltitle = Label(newWindow, text="Sistema de Gerenciamento de \n Ambiente Multinuvem", font='bold', background="#70ad47")
        lbltitle.place(x=60, y=180)


        btn = Button(newWindow, text="Adicionar Nuvem", command=lambda: self.addNuvemScreen(newWindow))
        btn.place(x=50, y=280)

        btn = Button(newWindow, text="Remover Nuvem", command=lambda: self.rmNuvemScreen(newWindow))
        btn.place(x=200, y=280)

        lNuvem = self.server.listNuvem()
        yVal = 90

        if lNuvem != []:
            for i in lNuvem:
                yVal += 30
                self.addNuvemButton(newWindow, i, yVal)
               

    def addNuvemButton(self, Toplevel, nameNuvem, yAxis):
        btnNuvem = Button(Toplevel, text=nameNuvem, command=lambda: self.hostListScreen(nameNuvem), width=35, height=1)
        btnNuvem.place(x=50, y=yAxis)




    def hostListScreen(self, nameNuvem):
        lHost = self.server.listHost(nameNuvem)
        yVal = 90

        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Host List")

        lbl = Label(newWindow, text = "Hosts", bg='#70ad47', font='bold')
        lbl.place(x=140, y=30)

        btn1 = Button(newWindow, text="Adicionar Host", command=lambda: self.addHostScreen(newWindow, nameNuvem))
        btn1.place(x=120, y=310)

        btn2 = Button(newWindow, text="Remover Host", command=lambda: self.rmHostScreen(newWindow, nameNuvem))
        btn2.place(x=50, y=350)

        btn3 = Button(newWindow, text="Migrar Host", command=lambda: self.mgHostScreen(newWindow, nameNuvem))
        btn3.place(x=200, y=350)

        if lHost != []:
            for i in lHost:
                yVal += 30
                self.addHostButton(newWindow, i, yVal)

    def addHostButton(self, Toplevel, btnName, yAxis):
        btnHost = Button(Toplevel, text=btnName, command=lambda: self.vmListScreen(btnName), width=35, height=1)
        btnHost.place(x=40, y=yAxis)






    def vmListScreen(self, nameHost):
        lVm = self.server.listVm(nameHost)
        yVal = 90

        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambiente: Vm List")
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')

        lbl = Label(newWindow, text = "Vms", bg='#70ad47', font='bold')
        lbl.place(x=140, y=30)

        btn1 = Button(newWindow, text="Adicionar Vm", command=lambda: self.addVmScreen(newWindow, nameHost))
        btn1.place(x=120, y=310)

        btn2 = Button(newWindow, text="Remover Vm", command=lambda: self.rmVmScreen(newWindow, nameHost))
        btn2.place(x=50, y=350)

        btn3 = Button(newWindow, text="Migrar Vm", command=lambda: self.mgVmScreen(newWindow, nameHost))
        btn3.place(x=200, y=350)

        if lVm != []:
            for i in lVm:
                yVal += 30
                self.addVmButton(newWindow, i, yVal)

    def addVmButton(self, Toplevel, btnName, yAxis):
        btnHost = Button(Toplevel, text=btnName, command=lambda: self.procListScreen(btnName), width=35, height=1)
        btnHost.place(x=40, y=yAxis)




    def procListScreen(self, nameVm):
        lProc = self.server.listProc(nameVm)
        yVal = 90

        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambiente: Processo List")
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')

        lbl = Label(newWindow, text = "Processo",  bg='#70ad47', font='bold')
        lbl.place(x=130, y=30)

        btn1 = Button(newWindow, text="Adicionar Processo", command=lambda: self.addProcScreen(newWindow, nameVm))
        btn1.place(x=120, y=310)

        btn2 = Button(newWindow, text="Remover Processo", command=lambda: self.rmProcScreen(newWindow, nameVm))
        btn2.place(x=50, y=350)

        btn3 = Button(newWindow, text="Migrar Processo", command=lambda: self.mgProcScreen(newWindow, nameVm))
        btn3.place(x=200, y=350)

        if lProc != []:
            for i in lProc:
                yVal += 30
                self.addProcButton(newWindow, nameVm, i, yVal)

    def addProcButton(self, Toplevel, vmName, btnName, yAxis):
        btnHost = Button(Toplevel, text=btnName, command=lambda: self.messageScreen(vmName, btnName), width=35, height=1)
        btnHost.place(x=50, y=yAxis)




    def messageScreen(self, nameVm, nameProc):
        lMessage = self.server.readMessages(nameProc)
        yVal = 50

        newWindow = Toplevel(self.root)
        newWindow.title("Messages")
        newWindow.geometry("330x400")

        lbl = Label(newWindow, text = "Messages",  bg='#70ad47', font='bold')
        lbl.place(x=130, y=30)

        btn = Button(newWindow, text="Send Message", command=lambda: self.sendMessageScreen(newWindow, nameVm, nameProc))
        btn.place(x=20, y=350)

        if lMessage != []:
            for i in lMessage:
                yVal += 30
                self.messageLabel(newWindow, i, yVal)

    def messageLabel(self, Toplevel, message, yAxis):
        lbl = Label(Toplevel, text=message)
        lbl.place(x=50, y=yAxis)




#######################################################################################




    def addNuvemScreen(self, oldWindow):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambientes: Criar Nuvem")
        newWindow.geometry("330x250")
        newWindow.config(bg='#70ad47')

        lblNome = Label(newWindow, text = "Digite os Nomes", font='bold', bg='#70ad47')
        lblNome.place(x=20, y=15)

        lblNuvem = Label(newWindow, text = "Nuvem:",  font='bold', background="#70ad47")
        lblNuvem.place(x=20, y=50)
        nomeNuvem = Entry(newWindow)
        nomeNuvem.place(x=100, y=50, width=180, height=20)

        lblHost = Label(newWindow, text="Host:",  font='bold', background="#70ad47")
        lblHost.place(x=20, y=80)
        nomeHost = Entry(newWindow)
        nomeHost.place(x=100, y=80, width=180, height=20)

        lblVm = Label(newWindow, text="Vm:",  font='bold', background="#70ad47")
        lblVm.place(x=20, y=110)
        nomeVm = Entry(newWindow)
        nomeVm.place(x=100, y=110, width=180, height=20)

        lblProc = Label(newWindow, text="Processo:",  font='bold', background="#70ad47")
        lblProc.place(x=20, y=140)
        nomeProc = Entry(newWindow)
        nomeProc.place(x=100, y=140, width=180, height=20)

        btnNuvem = Button(newWindow, text="Criar", command=lambda: self.newNuvem( oldWindow,nomeNuvem.get(), nomeHost.get(), nomeVm.get(), nomeProc.get(), newWindow), width=10, height=1)
        btnNuvem.place(x=200, y=180)

    def rmNuvemScreen(self, oldWindow):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambientes: Remover Nuvem")
        newWindow.geometry("330x250")
        newWindow.config(bg='#70ad47')

        lblNuvem = Label(newWindow, text = "Nome Nuvem", bg='#70ad47')
        lblNuvem.place(x=20, y=50)
        nomeNuvem = Entry(newWindow)
        nomeNuvem.place(x=100, y=50, width=180, height=20)

        btnNuvem = Button(newWindow, text="Remover", command=lambda: self.rmNuvem( oldWindow, nomeNuvem.get(), newWindow), width=10, height=1)
        btnNuvem.place(x=200, y=180)

    def addHostScreen(self, oldWindow, nameNuvem):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Criar Hosts")

        lblHost = Label(newWindow, text="Nome Host",  bg='#70ad47', font='bold')
        lblHost.place(x=20, y=50)
        nomeHost = Entry(newWindow)
        nomeHost.place(x=110, y=50, width=180, height=20)

        btnHost = Button(newWindow, text="Adicionar", command=lambda: self.newHost(nameNuvem, nomeHost.get(), newWindow, oldWindow), width=10, height=1)
        btnHost.place(x=200, y=180)

    def rmHostScreen(self, oldWindow, nameNuvem):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Remover Hosts")

        lblHost = Label(newWindow, text="Nome Host",  bg='#70ad47', font='bold')
        lblHost.place(x=20, y=50)
        nomeHost = Entry(newWindow)
        nomeHost.place(x=110, y=50, width=180, height=20)

        btnHost = Button(newWindow, text="Remover", command=lambda: self.rmHost(nameNuvem, nomeHost.get(), newWindow, oldWindow), width=10, height=1)
        btnHost.place(x=200, y=180)

    def mgHostScreen(self, oldWindow, nameNuvem):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Migrar Hosts")

        lblNuvem2 = Label(newWindow, text="De " + nameNuvem + " para")
        lblNuvem2.place(x=20, y=50)
        nomeNuvem2 = Entry(newWindow)
        nomeNuvem2.place(x=100, y=50, width=180, height=20)

        lblHost = Label(newWindow, text="Nome Host")
        lblHost.place(x=20, y=80)
        nomeHost = Entry(newWindow)
        nomeHost.place(x=100, y=80, width=180, height=20)

        btnHost = Button(newWindow, text="Migrar", command=lambda: self.mgHost(nameNuvem, nomeNuvem2.get(), nomeHost.get(), newWindow, oldWindow), width=10, height=1)
        btnHost.place(x=200, y=180)

    def addVmScreen(self, oldWindow, nameHost):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Criar Vm's")

        lblVm = Label(newWindow, text="Nome Vm",  bg='#70ad47', font='bold')
        lblVm.place(x=20, y=50)
        nomeVm = Entry(newWindow)
        nomeVm.place(x=100, y=50, width=180, height=20)

        btnVm = Button(newWindow, text="Adicionar", command=lambda: self.newVm(nameHost, nomeVm.get(), newWindow, oldWindow), width=10, height=1)
        btnVm.place(x=200, y=180)

    def rmVmScreen(self, oldWindow, nameHost):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Remover Vm's")

        lblVm = Label(newWindow, text="Nome Vm",  bg='#70ad47', font='bold')
        lblVm.place(x=20, y=50)
        nomeVm = Entry(newWindow)
        nomeVm.place(x=100, y=50, width=180, height=20)

        btnVm = Button(newWindow, text="Remover", command=lambda: self.rmVm(nameHost, nomeVm.get(), newWindow, oldWindow), width=10, height=1)
        btnVm.place(x=200, y=180)

    def mgVmScreen(self, oldWindow, nameHost):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Migrar Vm's")

        lblHost2 = Label(newWindow, text="De " + nameHost + " para")
        lblHost2.place(x=20, y=50)
        nomeHost2 = Entry(newWindow)
        nomeHost2.place(x=100, y=50, width=180, height=20)

        lblVm = Label(newWindow, text="Nome Vm")
        lblVm.place(x=20, y=80)
        nomeVm = Entry(newWindow)
        nomeVm.place(x=100, y=80, width=180, height=20)

        btnVm = Button(newWindow, text="Migrar", command=lambda: self.mgVm(nameHost, nomeHost2.get(), nomeVm.get(), newWindow, oldWindow), width=10, height=1)
        btnVm.place(x=200, y=180)

    def addProcScreen(self, oldWindow, nameVm):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Criar Processo")

        lblProc = Label(newWindow, text="Processo",  bg='#70ad47', font='bold')
        lblProc.place(x=20, y=50)
        nomeProc = Entry(newWindow)
        nomeProc.place(x=100, y=50, width=180, height=20)

        btnProc = Button(newWindow, text="Adicionar", command=lambda: self.newProc(nameVm, nomeProc.get(), newWindow, oldWindow), width=10, height=1)
        btnProc.place(x=200, y=180)

    def rmProcScreen(self, oldWindow, nameVm):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Remover Processo")

        lblProc = Label(newWindow, text="Nome Processo",  bg='#70ad47', font='bold')
        lblProc.place(x=20, y=50)
        nomeProc = Entry(newWindow)
        nomeProc.place(x=100, y=50, width=180, height=20)

        btnProc = Button(newWindow, text="Remover", command=lambda: self.rmProc(nameVm, nomeProc.get(), newWindow, oldWindow), width=10, height=1)
        btnProc.place(x=200, y=180)

    def mgProcScreen(self, oldWindow, nameVm):
        newWindow = Toplevel(self.root)
        newWindow.title("Migrar Processo")
        newWindow.geometry("330x250")

        lblVm2 = Label(newWindow, text="De " + nameVm + " para")
        lblVm2.place(x=20, y=50)
        nomeVm2 = Entry(newWindow)
        nomeVm2.place(x=100, y=50, width=180, height=20)

        lblProc = Label(newWindow, text="Nome Processo")
        lblProc.place(x=20, y=80)
        nomeProc = Entry(newWindow)
        nomeProc.place(x=100, y=80, width=180, height=20)

        btnProc = Button(newWindow, text="Migrar", command=lambda: self.mgProc(nameVm, nomeVm2.get(), nomeProc.get(), newWindow, oldWindow), width=10, height=1)
        btnProc.place(x=200, y=180)

    def sendMessageScreen(self, oldWindow, nameVm, nameProc):
        newWindow = Toplevel(self.root)
        newWindow.title("Send Message")
        newWindow.geometry("330x250")

        lblProc2 = Label(newWindow, text="De " + nameProc + " para")
        lblProc2.place(x=20, y=50)
        nomeProc2 = Entry(newWindow)
        nomeProc2.place(x=100, y=50, width=180, height=20)

        lblMessage = Label(newWindow, text="Message")
        lblMessage.place(x=20, y=80)
        message = Entry(newWindow)
        message.place(x=100, y=80, width=180, height=20)

        btnMessage = Button(newWindow, text="Send", command=lambda: self.sendMessage(nameVm, nameProc, nomeProc2.get(), message.get(), newWindow, oldWindow), width=10, height=1)
        btnMessage.place(x=200, y=180)







    def newNuvem(self, TopLevel, nameNuvem, nameHost, nameVm, nameProc, oldWindow):
        if(self.numNuvem < self.maxNuvem):
            self.numNuvem += 1
            self.server.createNuvem(nameNuvem, nameHost, nameVm, nameProc)
            print(self.server.listNuvem())

        self.closeTab(oldWindow)
        self.closeTab(TopLevel)
        self.mainScreen()

    def rmNuvem(self, TopLevel, nameNuvem, oldWindow):
        if self.server.deleteNuvem(nameNuvem):
            self.numNuvem -= 1
            self.closeTab(oldWindow)
            self.closeTab(TopLevel)
            self.mainScreen()
        else:
            self.closeTab(oldWindow)

    def newHost(self, nameNuvem, nameHost, oldWindow, newWindow):
        if self.server.addNewHost(nameNuvem, nameHost):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.hostListScreen(nameNuvem)
        else:
            self.closeTab(oldWindow)

    def rmHost(self, nameNuvem, nameHost, oldWindow, newWindow):
        if self.server.deleteHost(nameNuvem, nameHost):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.hostListScreen(nameNuvem)
        else:
            self.closeTab(oldWindow)

    def mgHost(self, nameNuvem, nameNewHost, nameHost, oldWindow, newWindow):
        if self.server.migrateHost(nameNuvem, nameNewHost, nameHost):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.hostListScreen(nameNuvem)
        else:
            self.closeTab(oldWindow)

    def newVm(self, nameHost, nameVm, oldWindow, newWindow):
        if self.server.addNewVm(nameHost, nameVm):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.vmListScreen(nameHost)
        else:
            self.closeTab(oldWindow)

    def rmVm(self, nameHost, nameVm, oldWindow, newWindow):
        if self.server.deleteVm(nameHost, nameVm):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.vmListScreen(nameHost)
        else:
            self.closeTab(oldWindow)

    def mgVm(self, nameHost, nameNewHost, nameVm, oldWindow, newWindow):
        if self.server.migrateVm(nameHost, nameNewHost, nameVm):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.vmListScreen(nameHost)
        else:
            self.closeTab(oldWindow)

    def newProc(self, nameVm, nameProc, oldWindow, newWindow):
        if self.server.addNewProc(nameVm, nameProc):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.procListScreen(nameVm)
        else:
            self.closeTab(oldWindow)

    def rmProc(self, nameVm, nameProc, oldWindow, newWindow):
        self.server.removeProc(nameVm, nameProc)
        self.closeTab(oldWindow)
        self.closeTab(newWindow)
        self.procListScreen(nameVm)

    def mgProc(self, nameVm, nameNewVm, nameProc, oldWindow, newWindow):
        if self.server.migrateProc(nameVm, nameNewVm, nameProc):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.procListScreen(nameVm)
        else:
            self.closeTab(oldWindow)

    def sendMessage(self, nameVm, nameProdSender, nameProcReceiver, message, oldWindow, newWindow):
        lProc = self.server.listProc(nameVm)
        ok = False

        for i in lProc:
            if i == nameProcReceiver:
                ok = True

        if ok:
            self.server.sendMessage(nameProdSender, nameProcReceiver, message)
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.messageScreen(nameVm, nameProdSender)
        else:
            self.closeTab(oldWindow)


    def close(self, TopLevel):
        TopLevel.destroy()
        TopLevel.quit()
        self.root.destroy()

    def closeTab(self, TopLevel):
        TopLevel.destroy()




if __name__ == "__main__":
    server = Server()
    ServerScreen(server)
    #root.mainloop()
    