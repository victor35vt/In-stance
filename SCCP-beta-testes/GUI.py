#Importando arquivos
from back import *

#importando thread
from threading import Thread

#Notificação (curta, longa)(sonora, visual)
camera = 0
tempoTrab = 3000 #50 min pausa 10
User = "Nome"
#efinir usuario
defUsuario(User)

#botão iniciar (inicia verificações e contador para pausa)

t1 = Thread(target=tempo, args=[tempoTrab, camera])
t1.start()

#botão realizar pausa   Adianta momento da pausa
    #signalV = 0
    #Troca para a tela da cartilha com botão despausar

#botão finalizar execução


#botão ser notificado de pausar em x tempo




#possivel problema em comunicar as variáveis entre back e gui
#criar função que receba x como parametro e altere var glob
#essa função fique em back
