"""
************************************************************************************************************************
* Chat_Espaco_de_Tuplas.py
* Programação Paralela e Distribuida(PPD) - 2022.2 - Prof.Cidcley
********************************************************************************************************************************
"""
"""
*******************
*  Bibliotecas utilizada 
********************
"""
import sys
import os
import  time, random

# Bibliotecas sobre MANIPULAÇÃO DE ESPAÇO DE TUPLAS em 'Python' 
import linsimpy

#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

# Importo do arquivo 'AnimatedGIF.py' que encontrei na web para animar gifs no tkinter.
from AnimatedGIF import *

"""Principais variáveis (GLOBAIS) utilizadas"""
# Espaço de Tuplas
tse = None

# Lista que vai registrar o nome dos usuários criados e sua 'flags' de recebimento de novas msgs ('0' quando não detectou nenhuma msg nova e '1' quando detectou)
lista_registro_nuvens = []

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


"""
*********************************
* Parte que Mexe com Espaço de Tuplas ()
**********************************
"""

#
# Obs. Aqui usa-se 'ts' para abreviar 'Tuple Spaces', os 'prints' vistos nas funções são apenas para 'debug' apenas!
#
# Criação da Sala e das matrizes para armazenar os INTEGRANTES e as MENSAGENS
def criaConteiner(ts, nomeConteiner):
    mensagens = []
    integrantes = []
    ts.out(("Conteiner", nomeConteiner, tuple(mensagens)))
    ts.out(("INT", nomeConteiner, tuple(integrantes)))

    Conteiners = ts.inp(("ConteinerS", object))
    temp = list(Conteiners[1])
    temp.append(nomeConteiner)
    ts.out(("Conteiners", tuple(temp)))

# Add as mensagens a Lista de mensagens que a Conteiner em específico do chat do usuário possui
def mandaMensagem(ts, nomeConteiner, remetente, destinatario, mensagem):
    mensagens = ts.inp(("Conteiner", nomeConteiner, object))
    temp = list(mensagens[2])
    temp.clear()
    
    if destinatario != "Todos":
        temp.append((destinatario,"<" + remetente + " - *Msg Privada para vc>: " + mensagem),)
    else:
        temp.append((destinatario,"<" + remetente + ">: " + mensagem),)
        
    ts.out(("Conteiner", nomeConteiner, tuple(temp)))
    print("Destinatario " + str(destinatario))
    print("Mandou MSG " + str(temp))

# Retorna a ''última mensagem enviada'' no chat de Tuplas
def recebeMensagem(ts, nomeConteiner):
    mensagens = ts.rdp(("Conteiner", nomeConteiner, object))
    #print("Recebe MSG " + str(mensagens))
    return list(mensagens[2])
    
# Add usuário na Conteiner em que entrou
def entraConteiner(ts, nome, nomeHost, nomeVm, nomeProcess, nomeConteiner):
    integrantes = ts.inp(("INT", nomeConteiner, object))
    temp = list(integrantes[2])
    temp.append(nome)
    temp.append(nomeHost)
    temp.append(nomeVm)
    temp.append(nomeProcess)
    ts.out(("INT", nomeConteiner, tuple(temp)))
    print("Entrou Conteiner " + nomeConteiner)

# Retira usuário da Conteiner em que entrou
def saiConteiner(ts, nome, nomeHost, nomeVm, nomeProcess,nomeConteiner):
    integrantes = ts.inp(("INT", nomeConteiner, object))
    temp = list(integrantes[2])
    temp.remove(nome)
    temp.remove(nomeHost)
    temp.remove(nomeVm)
    temp.remove(nomeProcess)
    ts.out(("INT", nomeConteiner, tuple(temp)))
    print("Saiu Conteiner " + nomeConteiner)

# Cria a tupla DA NUVEM e coloca ela na tupla 'nuvens' para ser armazenada
def criaNuvem(ts, nome, nomeHost, nomeVm, nomeProcess):
    nuvens = ts.inp(("nuvens", object))
    temp = list(nuvens[1])
    temp.append(nome)
    ts.out(("nuvens", tuple(temp)))
    print("nuvens: " + str(temp))

    hosts = ts.inp(("hosts", object))
    tempH = list(hosts[1])
    tempH.append(nomeHost)
    ts.out(("hosts", tuple(tempH)))
    print("hosts: " + str(tempH))

    vms = ts.inp(("vms", object))
    tempV = list(vms[1])
    tempV.append(nomeVm)
    ts.out(("vms", tuple(tempV)))
    print("vms: " + str(tempV))

    process = ts.inp(("process", object))
    tempP = list(process[1])
    tempP.append(nomeProcess)
    ts.out(("process", tuple(tempP)))
    print("process: " + str(tempP))

# Retira a tupla DA NUVEM da tupla 'nuvens' aonde foi armazenada
def deletaNuvem(ts, nome, nomeHost, nomeVm, nomeProcess):
    nuvens = ts.inp(("nuvens", object))
    temp = list(nuvens[1])
    print(temp)
    temp.remove(nome)
    ts.out(("nuvens", tuple(temp)))

    hosts = ts.inp(("hosts", object))
    tempH = list(hosts[1])
    temp.remove(nomeHost)
    ts.out(("hosts", tuple(tempH)))

    vms = ts.inp(("vms", object))
    tempV = list(vms[1])
    temp.remove(nomeVm)
    ts.out(("vms", tuple(tempV)))

    Process = ts.inp(("Process", object))
    tempP = list(Process[1])
    temp.remove(nomeProcess)
    ts.out(("Process", tuple(tempP)))

# Lista integrantes de uma Conteiner em específico 'nomeConteiner' 
def listarIntegrantes(ts, nomeConteiner):
    integrantes = ts.rdp(("INT", nomeConteiner, object))
    print(integrantes)
    return list(integrantes[2])

# Lista TODOS as NUVENS do 'ts' ('Tuple Space')
def listaNuvens(ts):
    nuvens = ts.rdp(("NUVENS", object))
    print(nuvens)
    
    return list(nuvens[1])

# Lista TODAS as ConteinerS do 'ts' ('Tuple Space')
def listarConteiners(ts):
    Conteiners = ts.rdp(("CONTAINER", object))
    print(Conteiners)
    
    return list(Conteiners[1]) 

"""
*******************************************************
*Construção de Interface Gráfica com a biblioteca Tkinter
*******************************************************
"""

root = Tk()
root.withdraw()

path_img_botao_Entrar_asset = resource_path('recursos/botao_Entrar.png')
img_botao_Entrar_asset = PhotoImage(file=path_img_botao_Entrar_asset, master=root)

path_img_botao_Conversar_asset = resource_path('recursos/botao_Conversar.png')
img_botao_Conversar_asset = PhotoImage(file=path_img_botao_Conversar_asset, master=root)

path_img_botao_mandar_msg_asset = resource_path('recursos/botao_mandar_msg.png')
img_botao_mandar_msg_asset = PhotoImage(file=path_img_botao_mandar_msg_asset, master=root)

path_img_bg_usuario_lobby_asset = resource_path('recursos/bg_usuario_lobby.png')
img_bg_usuario_lobby_asset = PhotoImage(file=path_img_bg_usuario_lobby_asset, master=root)

path_img_bg_usuario_Chat_asset = resource_path('recursos/bg_usuario_Chat.png')
img_bg_usuario_Chat_asset = PhotoImage(file=path_img_bg_usuario_Chat_asset, master=root)

path_img_bg_configurar_Usuario_asset = resource_path('recursos/bg_configurar_Usuario.png')
img_bg_configurar_Usuario_asset = PhotoImage(file=path_img_bg_configurar_Usuario_asset, master=root)

path_img_botao_Conversar_privado_asset = resource_path('recursos/botao_Conversar_privado.png')
img_botao_Conversar_privado_asset = PhotoImage(file=path_img_botao_Conversar_privado_asset, master=root)

path_img_bg_Gera_Usuario_asset = resource_path('recursos/bg_Gera_Usuario.png')
img_bg_Gera_Usuario_asset = PhotoImage(file=path_img_bg_Gera_Usuario_asset, master=root)

path_img_botao_gerar_Usuario_asset = resource_path('recursos/botao_gerar_Usuario.png')
img_botao_gerar_Usuario_asset = PhotoImage(file=path_img_botao_gerar_Usuario_asset, master=root)

path_img_bg_nome_repetido_warning_asset = resource_path('recursos/bg_nome_repetido_warning.png')
img_bg_nome_repetido_warning_asset = PhotoImage(file=path_img_bg_nome_repetido_warning_asset, master=root)

path_img_bg_nome_repetido_sala_warning_asset = resource_path('recursos/bg_nome_repetido_sala_warning.png')
img_bg_nome_repetido_sala_warning_asset = PhotoImage(file=path_img_bg_nome_repetido_sala_warning_asset, master=root)

path_img_botao_Ok_asset = resource_path('recursos/botao_Ok.png')
img_botao_Ok_asset = PhotoImage(file=path_img_botao_Ok_asset, master=root)

def fecha_APLICACAO(Toplevel):
    Toplevel.destroy()      
    Toplevel.quit()
    root. destroy()
    os._exit(1) 

def fecha_janela_TOPLEVEL(Toplevel):
    Toplevel.destroy()

def retorna_Config_Nuvem(Toplevel):
    Toplevel.destroy()

def janela_Erro_Nome_Repetido_Nuvem():
    newWindow = Toplevel(root)
    newWindow.title("**Espaco de Tuplas: Erro!")
    icone_asset_url = resource_path('recursos/icone.ico')    
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("334x178")

    bg_label = Label(newWindow,image = img_bg_nome_repetido_warning_asset, width=334, height=178)
    bg_label.place(x=0, y=0)

    ok_button = Button(newWindow, image=img_botao_Ok_asset,command=lambda:fecha_janela_TOPLEVEL(newWindow))
    ok_button.place(x=107, y=127)

def janela_Erro_Nome_Repetido_Conteiner():
    newWindow = Toplevel(root)
    newWindow.title("**Espaco de Tuplas: Erro!")
    icone_asset_url = resource_path('recursos/icone.ico')    
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("334x178")

    bg_label = Label(newWindow,image = img_bg_nome_repetido_sala_warning_asset, width=334, height=178)
    bg_label.place(x=0, y=0)

    ok_button = Button(newWindow, image=img_botao_Ok_asset,command=lambda:fecha_janela_TOPLEVEL(newWindow))
    ok_button.place(x=107, y=127)

def janela_Inicial():
    newWindow = Toplevel(root)
    newWindow.title("Ambientes Multinuvens")
    icone_asset_url = resource_path('recursos/icone.ico')    
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("324x301")

    newWindow.protocol("WM_DELETE_WINDOW", lambda:fecha_APLICACAO(newWindow))

    bg_label = Label(newWindow,image = img_bg_Gera_Usuario_asset, width=324, height=301)
    bg_label.place(x=0, y=0)

    gif_bg_asset_url = resource_path('recursos/gifs/chat_bubble_GIF.gif') 
    lbl_with_my_gif = AnimatedGif(newWindow, gif_bg_asset_url,0.30)
    lbl_with_my_gif.config(bg='#70ad47')
    lbl_with_my_gif.place(x=135, y=40)
    lbl_with_my_gif.start()

    cria_usuario_button = Button(newWindow, image=img_botao_gerar_Usuario_asset,command=lambda:janela_Config_Nuvem(0,""))
    cria_usuario_button.place(x=84, y=213)

def janela_Config_Nuvem(flag_nome_nuvem, nome_nuvem_anterior):   
    newWindow = Toplevel(root)
    newWindow.title("Ambientes Multinuvens: Nuvem")
    icone_asset_url = resource_path('recursos/icone.ico')    
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("457x422")

    bg_label = Label(newWindow,image = img_bg_configurar_Usuario_asset, width=453, height=417)
    bg_label.place(x=0, y=0)

    text_area = ScrolledText(newWindow,wrap = WORD, width = 35,height = 4,font = ("Callibri",8))
    text_area.place(x=200, y=120)
    text_area.focus()

    nome_usuario_text_input = Entry(newWindow)
    nome_usuario_text_input.place(x=33, y=127,width = 155,height = 25)

    text_area_Hosts = Entry(newWindow)
    text_area_Hosts.place(x=100, y=200, width = 285,height = 25)

    text_area_VM = Entry(newWindow)
    text_area_VM.place(x=100, y=250, width = 285,height = 25)

    text_area_P = Entry(newWindow)
    text_area_P.place(x=135, y=290, width = 265,height = 25)

    sala_de_ENTRADA_text_input = Entry(newWindow)
    sala_de_ENTRADA_text_input.place(x=35, y=359,width = 325,height = 25)

    entrar_button = Button(newWindow, image=img_botao_Entrar_asset,command=lambda:janela_checa_Validade_Dados(newWindow, str(nome_usuario_text_input.get()), str(text_area_Hosts.get()), str(text_area_VM.get()), str(text_area_P.get()), str(sala_de_ENTRADA_text_input.get())))
    entrar_button.place(x=259, y=37)

    if flag_nome_nuvem == 1:
        nome_usuario_text_input.insert(0, nome_nuvem_anterior + " <-- último nome usado para nuvem...") 

    listaConteinersAbertas(text_area)



def janela_checa_Validade_Dados(newWindow_close, nome_nuvem, nomeHost, nomeVm, nomeProcess, nome_container_chat):
    global tse, lista_registro_nuvens
    nuvens = listaNuvens(tse)
    containers = listarConteiners(tse)
    
    if(nome_nuvem != ""):
        # Verificamos se o nome do usuário é único em relação aos das outras Tuplas
        if (nome_nuvem in nuvens):
            janela_Erro_Nome_Repetido_Nuvem()
        else:
            if(nome_container_chat!=""):
                # Verificamos se o nome da container criada é único em relação aos das outras Tuplas
                if (nome_container_chat in containers):
                    # Cria usuário e entra na container especificada
                    criaNuvem(tse, nome_nuvem, nomeHost, nomeVm, nomeProcess)
                    entraConteiner(tse, nome_nuvem, nome_container_chat)
                    # Fecha a janela de configurações e entra na container desejada
                    fecha_janela_TOPLEVEL(newWindow_close)
                    lista_temp = [nome_nuvem,0]
                    lista_registro_nuvens.append(lista_temp)
                    janela_Chat_Geral_Nuvem(nome_nuvem,nome_container_chat)
                else:
                    # Criamos o usuário e colocamos ele na tupla de Usuários em Geral
                    criaNuvem(tse, nome_nuvem, nomeHost, nomeVm, nomeProcess)
                    # Criamos a container e a colocamos na tupla de containers em Geral
                    criaConteiner(tse, nome_container_chat)
                    entraConteiner(tse, nome_nuvem, nome_container_chat)
                    # Fecha a janela de configurações e entra na container desejada (Na Thread que vai abrir a janela de Chat dela no caso, é um pouo travado rsrsrs)
                    fecha_janela_TOPLEVEL(newWindow_close)
                    lista_temp = [nome_nuvem,0]
                    lista_registro_nuvens.append(lista_temp)
                    janela_Chat_Geral_Nuvem(nome_nuvem,nome_container_chat)
            else:
                janela_Erro_Nome_Repetido_Conteiner()
    else:
        janela_Erro_Nome_Repetido_Nuvem()

#Janela que exibe os usuários presentes na container e permite ao usuário 'remetente' escolher o usuário 'destinatário' de suas mensagens no Chat
def janela_Lobby_Nuvem(conversa_chat,containerAtual):
    global tse
    
    newWindow = Toplevel(root)
    newWindow.title("Ambientes Multinuvens")
    icone_asset_url = resource_path('recursos/icone.ico')    
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("371x362")

    bg_label = Label(newWindow,image = img_bg_usuario_lobby_asset, width=371, height=362)
    bg_label.place(x=0, y=0)

    text_area = ScrolledText(newWindow,wrap = WORD, width = 39,height = 6.5,font = ("Callibri",9))
    text_area.place(x=36, y=140)
    text_area.focus()

    listaIntegrantes(text_area,containerAtual)

    escolhe_conversa_text_input = Entry(newWindow)
    escolhe_conversa_text_input.place(x=36, y=295,width = 296,height = 25)

    config_conversa_button = Button(newWindow, image=img_botao_Conversar_asset,command=lambda:muda_conversa_chat(conversa_chat,str(escolhe_conversa_text_input.get())))
    config_conversa_button.place(x=19, y=24)

# Aqui mudamos a variável 'conversa_chat' que define para quem as mensagens do usuário vão ser visto na container
def muda_conversa_chat(conversa_chat,novo_destinatario):
    if novo_destinatario != '':
        conversa_chat['ID'] = novo_destinatario
        #print("Modo do chat: " + conversa_chat)

# Interface principal da container de chat das Nuvens
def janela_Chat_Geral_Nuvem(nome_nuvem,nome_container_chat):
    global tse

   
    conversa_chat = {'ID': "Todos"} # Aqui vai indicar com quem o usuário vai mandar msg's! sala
    #Se o valor for 'Todos' e mandará msg's para todos na sala, se nçao ele manda para alguém em específico na sala apenas!
    
    newWindow = Toplevel(root)
    newWindow.title("Ambientes Multinuvens: Nuvem")
    icone_asset_url = resource_path('recursos/icone.ico')
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("371x469")

    newWindow.protocol("WM_DELETE_WINDOW", lambda:janela_retorna_Configuracoes_Nuvem(newWindow,1,nome_nuvem,nome_container_chat))

    bg_label = Label(newWindow,image = img_bg_usuario_Chat_asset, width=371, height=469)
    bg_label.place(x=0, y=0)

    gif_bg_asset_url = resource_path('recursos/gifs/chat_bubble_GIF.gif') 
    lbl_with_my_gif = AnimatedGif(newWindow, gif_bg_asset_url,0.30)
    lbl_with_my_gif.config(bg='#70ad47')
    lbl_with_my_gif.place(x=86, y=24)
    lbl_with_my_gif.start()

    #Abaixo é o campo do título do nome do usuário:
    bg_label_nome_cliente = Label(newWindow, text = nome_nuvem,font = ("Callibri",18, 'bold'))
    bg_label_nome_cliente.config(bg='#70ad47')
    bg_label_nome_cliente.place(x=161, y=48)

    text_area = ScrolledText(newWindow,wrap = WORD, width = 39,height = 14,font = ("Callibri",9))
    text_area.place(x=37, y=144)
    text_area.focus()

    text_area.insert(tk.INSERT,"[Chat Geral:] Conteiner '" + nome_container_chat + "' //\n\n", 'msg_inicial')
    text_area.insert(tk.INSERT,"<Você entrou> Bem vindo ao Chat! ~\n...\n\n", 'msg_inicial')

    text_area.tag_config('msg_inicial', foreground='red')
    text_area.tag_config('msg_inicial', foreground='red')

    msg_text_input = Entry(newWindow)
    msg_text_input.place(x=122, y=403,width = 205,height = 26)

    chat_privado_button = Button(newWindow, image=img_botao_Conversar_privado_asset,command=lambda:janela_Lobby_Nuvem(conversa_chat,nome_container_chat))
    chat_privado_button.place(x=292, y=103)

    envia_msg_button = Button(newWindow, image=img_botao_mandar_msg_asset,command=lambda:envia_mensagem(str(msg_text_input.get()),nome_nuvem,nome_container_chat,conversa_chat['ID']))
    envia_msg_button.place(x=42, y=388)

    # Porque usar a função ".after" em vez de Threads? (Explicação para esse método no seguinte link: https://stackoverflow.com/questions/58275699/tkinter-mainloop-after-and-threading-confusion-with-time-intensive-code)
    newWindow.after(1,lambda:recebe_mensagens(newWindow,text_area,nome_nuvem,nome_container_chat)) # <-- Nao precisa de Threads pois a função '.after' fará esse papel aqui sem gerar muitos travamentos na aplicação, isso, somente para o Tkinter em Python 3!

# Função que faz o usuário 'retornar' a interface de 'Configuração do Usuário' quando sai da container de chat
def janela_retorna_Configuracoes_Nuvem(newWindow_close,flag_nome_nuvem,nome_nuvem_atual, nome_container_atual):
    global tse,lista_registro_nuvens

    # Abaixo removemos o elemento da lista de registro
    for i in range(len(lista_registro_nuvens)):
        if lista_registro_nuvens[i][0] == nome_nuvem_atual:
            lista_registro_nuvens.pop(i)
            
    saiConteiner(tse, nome_nuvem_atual, nome_container_atual)
    deletaNuvem(tse, nome_nuvem_atual)
    fecha_janela_TOPLEVEL(newWindow_close)                             
    janela_Config_Nuvem(flag_nome_nuvem,nome_nuvem_atual)

# Envia a mensagem do usuário para as outras Tuplas de usuários na container                                  
def envia_mensagem(entry_widget,nome_nuvem,nome_container_chat,destinatario):
    global tse, lista_registro_nuvens
    msg = entry_widget
    if(msg != ""):
        mandaMensagem(tse, nome_container_chat, nome_nuvem, destinatario, msg)
        for i in range(len(lista_registro_nuvens)): 
            lista_registro_nuvens[i][1] = 1 # <-- 'Setamos' a flag de todos os usuários na lista que armazena seus nomes e suas flags para o valor de '1'!

# Envia a mensagem do usuário para as outras Tuplas de usuários na container ('Loop' que checa por novas mensagens enviadas)
def recebe_mensagens(newWindow_input,ScrolledText,nome_nuvem,containerAtual):
    global tse,lista_registro_nuvens    
    msg_recebida = recebeMensagem(tse, containerAtual)

    for i in lista_registro_nuvens:
        if i[0] == nome_nuvem:
            if i[1] == 1: # <--  verifica se o usuário em específico está com sua flag como '1', se tiver, o usuário atualizará as msgs do seu chat pois há novas msgs!
                if(msg_recebida[0][0] == "Todos"):
                    ScrolledText.insert(tk.INSERT,msg_recebida[0][1]+"\n")
                    print(nome_nuvem+" recebeu a msg!")
                    i[1] = 0
                elif(msg_recebida[0][0] == nome_nuvem):
                    ScrolledText.insert(tk.INSERT,msg_recebida[0][1]+"\n", 'msg_privada')
                    ScrolledText.tag_config('msg_privada', background='#efe5b0',foreground='red')
                    i[1] = 0
            else:
                pass

    newWindow_input.after(1,lambda:recebe_mensagens(newWindow_input,ScrolledText,nome_nuvem,containerAtual))

# Faz a atualização da lista de integrantes numa container em específico dentre as TUPLAS
def listaIntegrantes(ScrolledText,containerAtual):
    global tse
    ScrolledText.delete('1.0', END)
    ScrolledText.insert(tk.INSERT,"[ ! ]: NUVENS PRESENTES NO CONTAINER: ...\n")
    lista = listarIntegrantes(tse, containerAtual)
    ScrolledText.insert(tk.INSERT,str(lista)+"\n")
    # Link que ajudou nesse trecho: https://stackoverflow.com/questions/15769246/pythonic-way-to-print-list-items
    print(*lista, sep='\n')
    ScrolledText.insert(tk.INSERT,"\n\n ...\n") 

# Faz a atualização da lista de Conteiner dentre as TUPLAS de Conteiner criadas
def listaConteinersAbertas(ScrolledText):
    global tse
    atualiza_Conteiner = listarConteiners(tse)

    if(len(atualiza_Conteiner) == 0): # Checa se nenhuma sala foi criada ainda...
        ScrolledText.delete('1.0', END)
        ScrolledText.insert(tk.INSERT,"**NENHUMA CONTAINER FOI CRIADA AINDA! ...\n")                             
        ScrolledText.insert(tk.INSERT,"\n\n ...\n")
    else:
        ScrolledText.delete('1.0', END)
        ScrolledText.insert(tk.INSERT,"[ ! ]: AS SEGUINTES CONTAINERS ESTÃO DISPONÍVEIS: ...\n")
        lista = listarConteiners(tse)
        ScrolledText.insert(tk.INSERT,str(lista)+"\n")
        
        print(*lista, sep='\n')
        ScrolledText.insert(tk.INSERT,"\n\n ...\n")

if __name__ == "__main__":
    tse = linsimpy.TupleSpaceEnvironment()

    nuvens = []
    conteiner = []
    tse.out(("NUVENS", tuple(nuvens)))
    tse.out(("CONTAINERS", tuple(conteiner)))

    janela_Inicial()
    root.mainloop()
