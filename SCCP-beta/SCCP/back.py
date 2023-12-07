import cv2                                      #camera
import mediapipe as mp                          #mediapipe
import numpy as np
from time import sleep                          #espera
from threading import Thread
from queue import Queue
import time
#notificar
from winotify import Notification
#envio
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float, select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import pymysql

geral = {}
#geral['sinalVerif'] = str        sinal on off thread verificação (run, pausa, fim)
#geral['sinalLog'] = bool         sinal on off thread log
geral['anterior'] = 'default'
geral['atual'] = 'default'
geral['countM'] = geral['countE'] = geral['countC'] = 0     #Contador mapeamento, erro, e correto

#--------------------------------------------------------------         Funções setup
def setup(user, tempoTrab, camera):
    global geral
    geral['usuario'] = user
    geral['camera'] = camera
    geral['tempoTrab'] = tempoTrab

def iniciar():
    global geral
    t1 = Thread(target=tempo, args=[geral['tempoTrab'], geral['camera']])
    t1.start()
    notificacao = Notification(app_id='Sistema de classificação e correção postural', title='Executando..', msg='Prepare-se, sua postura será analisada..')
    notificacao.show()

def pausar():
    global geral
    try:
        if geral['sinalVerif']!='pausa':
            geral['sinalVerif'] = 'pausa'
            notificacao = Notification(app_id='Sistema de classificação e correção postural', title='Pausa', msg='Pausa iniciada.\nTome um ar, descanse um pouco, realize alguns dos exercicios recomendados.\nRetorne em 10 minutos.')
            notificacao.show()
    except:
        pass

def finalizar():
    global geral
    try:
        if geral['sinalVerif'] != 'fim':
            geral['sinalVerif'] = 'fim'
            notificacao = Notification(app_id='Sistema de classificação e correção postural', title='Fim de execução', msg='Processos finalizando.')
            notificacao.show()
    except:
        pass
    
#--------------------------------------------------------------         domínio da thread t1 (tempo)
def tempo(tempoTrab ,camera):
    #Setup
    global geral
    geral['sinalVerif'] = 'run'                 #Seta sinal de verificação para rodar
    geral['anterior'] = 'default'
    geral['atual'] = 'default'
    geral['countM'] = geral['countE'] = geral['countC'] = 0     #Contador mapeamento, erro, e correto

    verif = Thread(target=verificar, args= [camera])
    verif.start()                               #inicia thread de verificação
    verif.join(timeout=geral['tempoTrab'])      #Espera tempo de serviço acabar ou alguem desligar a thread colocando geral['sinalVerif'] = 'fim' ou = 'pausa'
    if verif.is_alive():                        #se a thread estiver funcionando ainda
        #Notificação, hora de realizar uma pausa
        print("hora de pausar")
        notificacao = Notification(app_id='Sistema de classsificação e correção postural', title='Recomendação', msg='Hora de fazer uma pausa')
        notificacao.show()
        geral['sinalVerif'] = 'pausa'           #Envia sinal de desligar thread de verificação
    
#--------------------------------------------------------------         domínio thread log
queueRelatorios = Queue()

#Thread log pega elemento da queue de registros, classifica postura, gera registro e notificações
def gerarRegistro():#relatorio):
    global geral

    while geral['sinalLog'] or (not queueRelatorios.empty()):
        if not queueRelatorios.empty():
            relatorio = queueRelatorios.get()
            #print(relatorio)
                            
            if relatorio['mapping']:                            #se conseguiu mapear
                #classifica postura
                if relatorio['posição cabeça'] and relatorio['queixo pescoço'] and relatorio['braço tronco E'] and relatorio['braço tronco D'] and relatorio['cotovelo E'] and relatorio['cotovelo D']:
                    postura = 'correta'
                else:
                    postura = 'errada'
                
                #se postura está correta e antes não estava
                if (postura=='correta') and (geral['atual'] != 'correta'):
                    geral['countC']+=1
                    #10 medições corretas seguidas notifica ok
                    if geral['countC'] == 10:
                        geral['countM']=0
                        geral['countE']=0
                        #Notificar tudo ok
                        notificacao = Notification(app_id='Sistema de classsificação e correção postural', 
                                                   title='Classificação postural: Adequada', 
                                                   msg='Continue assim.')
                        notificacao.show()
                        #muda estado para correta
                        geral['atual'] = 'correta'
                else:
                    geral['countE']+=1
                    if (geral['countE'] == 20) and (geral['atual']!='errada'):
                        geral['countM']=0
                        geral['countC']=0
                        corrigir = 'Ajuste:\n'
                        #notifica partes erradas
                        if relatorio['posição cabeça']!=True:   #posição da cabeça
                            corrigir+='posição da cabeça, '
                        if relatorio['queixo pescoço']!=True:   #angulo cabeça
                            corrigir+='angulação da cabeça, '
                        if relatorio['braço tronco E']!=True:   #posição do braço esquerdo
                            corrigir+='braço esquerdo, '
                        if relatorio['braço tronco D']!=True:   #posição do braço direito
                            corrigir+='braço direito, '
                        if relatorio['cotovelo E']!=True:       #angulo do cotovelo esquerdo
                            corrigir+='cotovelo esquerdo, '
                        if relatorio['cotovelo D']!=True:       #angulo do cotovelo direito
                            corrigir+='cotovelo direito, '

                        notificacao = Notification(app_id='Sistema de classsificação e correção postural', 
                                                   title='Postura classsificada como errada', 
                                                   msg=corrigir)
                        if corrigir != 'Ajuste:\n':
                            notificacao.show()
                            geral['atual'] = 'errada'
                        else:
                            geral['countE']-=1
                    elif ((geral['countE'] == 30) or (geral['countE'] == 40)) and (geral['atual']=='errada'):
                        corrigir = 'Ajuste:\n'
                        #notifica partes erradas
                        if relatorio['posição cabeça']!=True:   #posição da cabeça
                            corrigir+='posição da cabeça, '
                        if relatorio['queixo pescoço']!=True:   #angulo cabeça
                            corrigir+='angulação da cabeça, '
                        if relatorio['braço tronco E']!=True:   #posição do braço esquerdo
                            corrigir+='braço esquerdo, '
                        if relatorio['braço tronco D']!=True:   #posição do braço direito
                            corrigir+='braço direito, '
                        if relatorio['cotovelo E']!=True:       #angulo do cotovelo esquerdo
                            corrigir+='cotovelo esquerdo, '
                        if relatorio['cotovelo D']!=True:       #angulo do cotovelo direito
                            corrigir+='cotovelo direito, '

                        notificacao = Notification(app_id='Sistema de classsificação e correção postural', 
                                                   title='Postura classsificada como errada', 
                                                   msg=corrigir)
                        if corrigir != 'Ajuste:\n':
                            notificacao.show()
                        else:
                            geral['countE']-=1
            else:
                geral['countM']+=1
                if geral['countM'] == 10:
                    geral['countE']=0
                    geral['countC']=0
                    #notifica problema na detecção de pontos
                    notificacao = Notification(app_id='Sistema de classsificação e correção postural', 
                                                   title='Problema ne detecção', 
                                                   msg='Não conseguimos indentificar você, se posicione na frente da câmera')
                    notificacao.show()
                if geral['countM'] == 30:
                    geral['atual'] = 'indetectavel'

            if geral['anterior']!=geral['atual']:
                geral['anterior']=geral['atual']
                #chama envio de log envio do log
                enviarLog(relatorio['inicio'], geral['atual'])       #estados: (indetectavel, errada, correta)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Instance_BD"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    inicio: Mapped[float] = mapped_column(Float)           
    estado: Mapped[str] = mapped_column(String(50)) 
    
    def _repr_(self) -> str:
        return f"User(id={self.id!r}, nome={self.nome!r}, inicio={self.inicio!r}, estado={self.estado})"

def enviarLog(inicioLog, estadoLog):
    global geral
    log = {}
    log["user"] =  geral['usuario']
    log["inicio"] = inicioLog
    log["estado"] = estadoLog                                      #(indetectavel, errada, correta, pausa, fim)
    #print(log)
    engine = create_engine("mysql+pymysql://admin:Laranacompany#2728)&$%#%@in-stance.clzez51mwuu2.us-east-1.rds.amazonaws.com/Instance_BD")
    User.metadata.create_all(engine)
    with Session(engine) as session:
        Laranacompany = User(
            nome=geral['usuario'],
            inicio= inicioLog,
            estado= estadoLog
        )
        session.add_all([Laranacompany])
        session.commit()
    return

    #relatorio = {
    #           "user": Usuário
    #           "inicio" = time.time()
    #           "Estado": Estado    ('indetectavel', 'errada', 'correta', 'pausa', 'fim')
    # }

#--------------------------------------------------------------         domínio thread de verificação

def verificar(camera):
    global geral
    geral['anterior'] = 'default'
    geral['sinalLog'] = 1                                       #deixa avisado para theadlog que pode funcionar
    threadlog = Thread(target=gerarRegistro)                    #ajusta threadlog
    threadlog.start()                                           #inicia threadlog

    mp_drawing = mp.solutions.drawing_utils                     #guarda desenho
    mp_pose = mp.solutions.pose                                 #Usando modelo de estimar pose
    cap = cv2.VideoCapture(camera)                              #iniciar camera, 0 representa o numero da webcam 0
    #ajuste da estimativa de confiança do modelo de pose(imagem mt boa pode usar conf mais alta)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        #iniciar rotina de captura
        while geral['sinalVerif'] == 'run':                     #Se a flag de verificar estiver ok faz captura, se não para
            rotina_captura(cap, pose, mp_drawing, mp_pose)
            if (cv2.waitKey(10) & 0xFF) == ord('q'):            #se clicar q fecha
                #break
                geral['sinalVerif'] = 'fim'
            sleep(1)
    geral['sinalLog'] = False                                   #avisa threadlog pra encerrar
    threadlog.join()                                            #espera threadlog terminar
    enviarLog(time.time(), geral['sinalVerif'])                 #Envia log de pausa ou fim

    #fim de captura
    cap.release()                                               #fecha webcam
    cv2.destroyAllWindows()                                     #fecha janelas

def rotina_captura(cap, pose, mp_drawing, mp_pose):
    if cap.isOpened():                                          #Verifica se camera está aberta
        ret, frame = cap.read()                                 #guarda a leitura em variaveis
        inicio = time.time()                                    #guarda segundo em que foi retirada a captura

        #Recolore imagem em rgb para mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False          
        results = pose.process(image)                           #Usa modelo na imagem e guarda result
        #Recolore em BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        try:                                                    #Extrair coordenadas dos pontos (landmarks)
            #Array de landmarks: x, y, z e visibilidade de cada ponto, visibilidade 0 a 1
            pontos = results.pose_landmarks.landmark
            relatorio = verif_postura(mp_pose, pontos)          #verifica a postura e recebe dicionario relatorio
        except:
            relatorio = {'mapping': False}                      #Mapeamento mal sussedido
            pass                                                #iformar erro na detecção
        relatorio['inicio'] = inicio                            #guarda o segundo em que foi retirada captura no relatorio
        #gerarRegistro(relatorio)                                #relatorio passado para geração de registro
        queueRelatorios.put(relatorio)                          #guardar relatorio em queue
        
        #Desenha pontos e linhas de conexão na imagem
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Mediapipe Feed', image)                     #Mostra imagem

#função para calcular angulo entre pontos 3d
def angulo(a,b,c):
    a = np.array(a) # ponta 1
    b = np.array(b) # Meio
    c = np.array(c) # ponta 2
    V1 = np.array([a[0]-b[0], a[1]-b[1], a[2]-b[2]])            #obtenho vetor que começa em b e termina em a
    V2 = np.array([c[0]-b[0], c[1]-b[1], c[2]-b[2]])            #obtenho vetor que começa em b e termina em c
    MV1 = (V1[0]**2+V1[1]**2+V1[2]**2)**(0.5)                   #módulo do vetor 1
    MV2 = (V2[0]**2+V2[1]**2+V2[2]**2)**(0.5)                   #módulo do vetor 2
    radians = np.arccos((V1[0]*V2[0]+V1[1]*V2[1]+V1[2]*V2[2])/(MV1*MV2))   #Obtendo o angulo em radiandos entre os dois vetores
    angle = np.abs(radians*180.0/np.pi)                         #angulo em graus
    return angle
  
#verifica postura, se angulos estão corretos 
def verif_postura(mp_pose, pontos):
    #Definindo pontos de análise
    ombroE=[pontos[11].x, pontos[11].y, pontos[11].z]           #ombro esquerdo 11
    ombroD=[pontos[12].x, pontos[12].y, pontos[12].z]           #ombro direito 12
    mediaOmbros = [(pontos[12].x + pontos[11].x)/2, (pontos[12].y + pontos[11].y)/2, (pontos[12].z + pontos[11].z)/2]
    cotoveloE=[pontos[13].x, pontos[13].y, pontos[13].z]        #cotovelo esquerdo 13
    cotoveloD=[pontos[14].x, pontos[14].y, pontos[14].z]        #cotovelo direito 14
    pulsoE=[pontos[15].x, pontos[15].y, pontos[15].z]           #pulso esquerdo 15
    pulsoD=[pontos[16].x, pontos[16].y, pontos[16].z]           #pulso direito 16
    quadrilE=[pontos[23].x, pontos[23].y, pontos[23].z]         #quadris esquerdo 23
    quadrilD=[pontos[24].x, pontos[24].y, pontos[24].z]         #quadris direito 24
    mediaQuadris=[(pontos[24].x + pontos[23].x)/2, (pontos[24].y + pontos[23].y)/2, (pontos[24].z + pontos[23].z)/2]
    nariz =[pontos[0].x, pontos[0].y, pontos[0].z]              #Nariz 0
    #Media orelhas (centro da cabeça), esquerda 7, direita 8
    mediaOrelhas = [(pontos[8].x + pontos[7].x)/2, (pontos[8].y + pontos[7].y)/2, (pontos[8].z + pontos[7].z)/2]

    #verificando angulos
    margem = 5                                                  #+5 e - 5 de margem de erro do midiapipe
    relatorio={}                                                #dicionario de true e false para verificações

    #prostração da cabeça 
    ang = angulo(mediaOrelhas, mediaOmbros, mediaQuadris)
    #print('prostração da cabeça ',ang)
    relatorio['posição cabeça']= (ang <= 180 - 5 + margem and ang >= 180-20-margem)    
    #Angulo pescoço-queixo 80 a 100 graus (90 +- 10)
    ang = angulo(mediaOmbros, mediaOrelhas, nariz) -33#-31
    #print('queixo pescoço ',ang)
    relatorio['queixo pescoço']= (ang <= 100 and ang >= 80) 
    #Angulo braço-tronco 20-30  
    ang = angulo(quadrilE, ombroE, cotoveloE)                   #esquerdo
    relatorio['braço tronco E']= (ang <= 30+margem and ang >= 20-margem)                    
    ang = angulo(quadrilD, ombroD, cotoveloD)                   #direito
    relatorio['braço tronco D']= (ang <= 30+margem and ang >= 20-margem)
    #Angulo cotovelo 90-100
    ang = angulo(ombroE, cotoveloE, pulsoE) -27                 #esquerdo
    #print('cotovelo E', ang)
    relatorio['cotovelo E']= (ang <= 100+margem and ang >= 90-margem)
    ang = angulo(ombroD, cotoveloD, pulsoD) -27+10              #direito
    #print('cotovelo D', ang)
    relatorio['cotovelo D']= (ang <= 100+margem and ang >= 90-margem)
    relatorio['mapping'] = True                                 #mapeamento bem sussedido

    return relatorio