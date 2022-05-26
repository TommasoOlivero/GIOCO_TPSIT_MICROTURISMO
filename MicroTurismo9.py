# Progetto TPSIT con Thread e Socket
# Autoti: Coppola Carmine Mattia e Olivero Tommaso
# Micro Turismo
__author__ = 'Carmine Mattia Coppola & Oliva Assonnata'

# importazione librerie
from random import Random
import pygame,sys
from pygame.locals import *
import socket
import serial, time
import threading, queue
import math
import socket

# code per la gestione dei dati
q = queue.Queue()
q2 = queue.Queue()

# Inizializzazione di pygame e creazione delle variabili globali
pygame.init()
accel=0
global button_a1
button_a1=False
global button_a2
button_a2=False
global button_b1
button_b1=False
global button_b2
button_b2=False

# Classe Thread per la lettura dei dati dal secondo micorbit
class Receiver(threading.Thread):
    def __init__(self):
        # costruttore del thread
        threading.Thread.__init__(self)
        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("192.168.10.168", 8000))
        self.s.listen()
        self.connection, self.address=self.s.accept()
        self.running = True

    # Funzione usata per la lettura dei dati
    def run(self):
        while self.running:
            dati=""
            dati=self.connection.recv(4096)
            dati=dati.decode()
            dati_split=dati.split(",")
            dati_split=dati_split[0]
            dati_split=float(dati_split)
            q2.put(dati_split)
            global button_a2
            global button_b2
            if "ATrue" in dati:
                button_a2=True
            else:
                button_a2=False
            if "BTrue" in dati:
                button_b2=True
            else:
                button_b2=False

    # Funzione per la terminazione del Lavoro del Thread
    def terminate(self):
        self.running = False

# Funzione per la lettura delle matrici delle mappe dai file
def leggiMatrice(nomeFile):
    f=open(nomeFile,"r")
    mat=[]
    righe=f.readlines()
    for riga in righe:
        r=[int(n) for n in riga[:-1]]
        mat.append(r)
    return mat, len(riga)-1, len(righe)

#Restituisce la prima coordinata disponibile
def getCoordinataDisponibile(campo):
    x,y=0,0
    while campo[y][x]!= 1:
        x=Random.randint[0,len(campo[0])]
        y=Random.randint[0,len(campo)]
    return x,y

def updateAcc(num):
    global accel
    accel=num

# Classe Thread per la lettura dei dati del microbit del server
class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    # Funzione per la lettura dei dati da MicroBit
    def run(self):
        #serial config
        port = "COM14"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode() 
            acc = data.split(",")
            q.put(float(acc[0]))
            global button_a1
            global button_b1
            if "ATrue" in acc[1]:
                button_a1=True
            else:
                button_a1=False
            if "BTrue" in acc[2]:
                button_b1=True
            else:
                button_b1=False
            #time.sleep(0.01)

# Classe Thread per la gestione dell'oggetto razzo
class Razzo(threading.Thread):
    def __init__(self,campo,speed, center,scala,display):
        threading.Thread.__init__(self)
        self.display=display
        self.scala=scala
        self.rotazione=speed
        self.campo=campo
        self.running=True
        self.x,self.y=center[0],center[1]
        self.DEFAULT_IMAGE_SIZE = (30, 50)
        self.imgDefault=pygame.image.load("./images/Razzo.png").convert_alpha()
        self.imgDefault=pygame.transform.scale(self.imgDefault,self.DEFAULT_IMAGE_SIZE)
        self.img = pygame.image.load("./images/Razzo.png").convert_alpha()
        self.imgrect = self.img.get_rect()
        self.imgrect.center=(self.x,self.y)

    def terminate(self):
        self.running=False

    # Funzione per l'animazione dell'esplosione
    def explode(self, x, y):
        dim_exp=80
        exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8 = pygame.image.load("./images/exp1.png"), pygame.image.load("./images/exp2.png"), pygame.image.load("./images/exp3.png"), pygame.image.load(
        "./images/exp4.png"), pygame.image.load("./images/exp5.png"), pygame.image.load("./images/exp6.png"), pygame.image.load("./images/exp7.png"), pygame.image.load("./images/exp8.png")
        exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8 = pygame.transform.scale(exp1, (dim_exp, dim_exp)), pygame.transform.scale(exp2, (dim_exp, dim_exp)), pygame.transform.scale(exp3, (dim_exp, dim_exp)), pygame.transform.scale(
        exp4, (dim_exp, dim_exp)), pygame.transform.scale(exp5, (dim_exp, dim_exp)), pygame.transform.scale(exp6, (dim_exp, dim_exp)), pygame.transform.scale(exp7, (dim_exp, dim_exp)), pygame.transform.scale(exp8, (dim_exp, dim_exp))
        exp1_rect, exp2_rect, exp3_rect, exp4_rect, exp5_rect, exp6_rect, exp7_rect, exp8_rect = exp1.get_rect(
        ), exp2.get_rect(), exp3.get_rect(), exp4.get_rect(), exp5.get_rect(), exp6.get_rect(), exp7.get_rect(), exp8.get_rect()
        self.display.blit(exp1, (x, y),  exp1_rect)

        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp2, (x, y),  exp2_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp3, (x, y),  exp3_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp4, (x, y),  exp4_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp5, (x, y),  exp5_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp6, (x, y),  exp6_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp7, (x, y),  exp7_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp8, (x, y),  exp8_rect)
        time.sleep(0.02)
        pygame.display.update()

    # Funzione che restituisce in base alla rotazione del microbit il valore di rotazione dell'auto
    def getAngoloRotazione(self):
        x,y=self.rotazione[0],self.rotazione[1]
        if y==0:
            if x > 0:
                ang=-90
            else:
                ang=90
        elif x== 0:
            if y > 0:
                ang=180
            else:
                ang=0
        else:
            ang=math.atan(abs(x)/abs(y))
            ang=math.degrees(ang)
            if x>= 0 and y <= 0:
                ang=-ang
            if x>= 0 and y >= 0:
                ang=-90-(90-ang)
            if x<= 0 and y >= 0:
                ang=90+(90-ang)
        return ang

    # Funzione per la gestione della traiettoria del Razzo
    def move(self):
        self.img=pygame.transform.rotate(self.imgDefault,self.getAngoloRotazione())
        self.x,self.y=self.imgrect.center[0],self.imgrect.center[1]
        self.imgrect=self.img.get_rect()
        self.imgrect.center=(self.x, self.y)
        self.imgrect=self.imgrect.move(self.rotazione)
        if self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)] != 1 and self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)] != 2 and self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)] != 3:
            self.explode(self.imgrect.centerx,self.imgrect.centery)
            self.running=False
        self.display.blit(self.img, self.imgrect)

    # Funzione per permettere il corretto e continuo lavoro della macchina
    def run(self):
        while self.running:
            self.move()
            time.sleep(0.08)
    
# Classe Thread per la gestione dell'oggetto macchina
class Car(threading.Thread):
    def __init__(self, campo, display,scala, codice, coda, immagine,button_a,button_b,partenza):
        threading.Thread.__init__(self)
        self.coda=coda
        self.button_a=button_a
        self.button_b=button_b
        self.codice= codice
        self.running=True
        self.scala=scala
        self.display=display
        self.acc= 0
        self.giri=0
        self.campo=campo
        self.DEFAULT_IMAGE_SIZE = (40, 90)
        self.imgDefault=pygame.image.load(immagine).convert_alpha()
        self.imgDefault=pygame.transform.scale(self.imgDefault,self.DEFAULT_IMAGE_SIZE)
        self.img = pygame.image.load(immagine).convert_alpha()
        
        self.imgrect = self.img.get_rect()
        self.angoloVecchio=0
        self.imgrect.center=(partenza[0],partenza[1])
        self.rotazione=[1,0]
        self.speed=0
        self.maxSpeed=15

    def terminate(self):
        self.running = False
    
    # Funzione che restituisce in base alla rotazione del microbit il valore di rotazione dell'immagine dell'auto
    def getAngoloRotazione(self):
        x,y=self.rotazione[0],self.rotazione[1]
        if y==0:
            if x > 0:
                ang=-90
            else:
                ang=90
        elif x== 0:
            if y > 0:
                ang=180
            else:
                ang=0
        else:
            ang=math.atan(abs(x)/abs(y))
            ang=math.degrees(ang)
            if x>= 0 and y <= 0:
                ang=-ang
            if x>= 0 and y >= 0:
                ang=-90-(90-ang)
            if x<= 0 and y >= 0:
                ang=90+(90-ang)
        return ang

    # Funzione per la rotazione della macchina su pygame
    def rotate(self,angolo):
        self.img=pygame.transform.rotate(self.imgDefault,self.angoloVecchio)
        angolo/=2
        cordx=self.imgrect.centerx
        cordy=self.imgrect.centery
        self.imgrect=self.img.get_rect()
        self.imgrect.center=(cordx,cordy)

        if self.rotazione[0] >= 0 and self.rotazione[1]<=0:
            self.rotazione[0]+=angolo
            self.rotazione[1]+=angolo
            self.angoloVecchio=self.getAngoloRotazione()

        elif self.rotazione[0]>= 0 and self.rotazione[1]>= 0:
            self.rotazione[0]-=angolo
            self.rotazione[1]+=angolo
            self.angoloVecchio=self.getAngoloRotazione()

        elif self.rotazione[0] <= 0 and self.rotazione[1] >= 0:
            self.rotazione[0]-=angolo
            self.rotazione[1]-=angolo
            self.angoloVecchio=self.getAngoloRotazione()

        elif self.rotazione[0] <= 0 and self.rotazione[1] <= 0:
            self.rotazione[0]+=angolo
            self.rotazione[1]-=angolo
            self.angoloVecchio=self.getAngoloRotazione()
            
        if self.rotazione[0]> 1:
            self.rotazione[0]=1
        if self.rotazione[0]< -1:
            self.rotazione[0]=-1
        if self.rotazione[1]> 1:
            self.rotazione[1]=1
        if self.rotazione[1]< -1:
            self.rotazione[1]=-1
    
    # Funzione per l'animazione di esplosione su pygame
    def explode(self, x, y):
        dim_exp=80
        exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8 = pygame.image.load("./images/exp1.png"), pygame.image.load("./images/exp2.png"), pygame.image.load("./images/exp3.png"), pygame.image.load(
        "./images/exp4.png"), pygame.image.load("./images/exp5.png"), pygame.image.load("./images/exp6.png"), pygame.image.load("./images/exp7.png"), pygame.image.load("./images/exp8.png")
        exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8 = pygame.transform.scale(exp1, (dim_exp, dim_exp)), pygame.transform.scale(exp2, (dim_exp, dim_exp)), pygame.transform.scale(exp3, (dim_exp, dim_exp)), pygame.transform.scale(
        exp4, (dim_exp, dim_exp)), pygame.transform.scale(exp5, (dim_exp, dim_exp)), pygame.transform.scale(exp6, (dim_exp, dim_exp)), pygame.transform.scale(exp7, (dim_exp, dim_exp)), pygame.transform.scale(exp8, (dim_exp, dim_exp))
        exp1_rect, exp2_rect, exp3_rect, exp4_rect, exp5_rect, exp6_rect, exp7_rect, exp8_rect = exp1.get_rect(
        ), exp2.get_rect(), exp3.get_rect(), exp4.get_rect(), exp5.get_rect(), exp6.get_rect(), exp7.get_rect(), exp8.get_rect()
        self.display.blit(exp1, (x, y),  exp1_rect)

        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp2, (x, y),  exp2_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp3, (x, y),  exp3_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp4, (x, y),  exp4_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp5, (x, y),  exp5_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp6, (x, y),  exp6_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp7, (x, y),  exp7_rect)
        time.sleep(0.02)
        pygame.display.update()
        self.display.blit(exp8, (x, y),  exp8_rect)
        time.sleep(0.02)
        pygame.display.update()

    # Funzione per il calcolo di respawn dopo uno schianto e stampa della macchina nel punto calcolato
    def respawn(self):
        spawnPossibili={True: -40,False :40}
        center=[self.imgrect.center[0],self.imgrect.center[1]]
        while self.campo[int(center[1]/self.scala)][int(center[0]/self.scala)]!= 1:
            if int((center[0]-30)/self.scala) < len(self.campo[0]):
                center[0]+=spawnPossibili[self.campo[int(center[1]/self.scala)][int((center[0]-20)/self.scala)]== 1]
            if int((center[1]-30)/self.scala) < len(self.campo):
                center[1]+=spawnPossibili[self.campo[int((center[1]-20)/self.scala)][int(center[0]/self.scala)]== 1]
        self.imgrect.center=center

    # Funzione per la gestione dello spostamento della macchina e degli eventi legati all'uso dei bottoni
    def move(self):
        if not(self.coda.empty()):
            self.acc=self.coda.get()
            self.acc=self.acc/2000
            if self.button_a:
                self.speed+=1
                if self.speed > self.maxSpeed:
                    self.speed=self.maxSpeed
            else:
                self.speed-=1
                if self.speed < 0:
                    self.speed=0
            if self.button_b:
                r=Razzo(self.campo,(self.rotazione[0]*40,self.rotazione[1]*40),self.imgrect.center,self.scala,self.display)
                r.start()
        
        self.rotate(self.acc)

        #self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)]=1
        self.imgrect=self.imgrect.move(self.rotazione[0]*self.speed,self.rotazione[1]*self.speed)
        if self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)] == 0:
            self.explode(self.imgrect.centerx,self.imgrect.centery)
            self.respawn()
            time.sleep(0.2)
            self.display.blit(self.img, self.imgrect)
            time.sleep(0.4)
        if self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)] == 2:
            self.giri+=1
            if(self.giri%2== 0):
                self.giri-=1
        if self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)] == 3:
            self.giri+=1
            if(self.giri%2==1):
                self.giri-=1
        self.campo[int(self.imgrect.centery/self.scala)][int(self.imgrect.centerx/self.scala)]=self.codice
        self.display.blit(self.img, self.imgrect)

    def run(self):
        while self.running:
            self.move()
            time.sleep(0.08)


def disegnaMappa(mappa, display, scala):#Utilizzabile per disegnare i bordi dei circuiti
    red= (255,   0,   0)
    for y,k in enumerate(mappa):
        for x,c in enumerate(k):
            if c == 1:
                pygame.draw.rect(display, red, (x*scala, y*scala, scala, scala))
    
#Funzione per la formatazione del testo
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

# Funzione per il controllo del menu iniziale
def menu_inziale(display, display_width, display_height):
    font = "Pixel Digivolve.otf"

    clock = pygame.time.Clock()
    FPS=30
    
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(50, 50, 50)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)

    menu=True
    global button_a1
    global button_b1
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        if button_a1 == True:
            return
        elif button_b1 == True:
            pygame.quit()
            quit()

        bgmenu = pygame.image.load("./images/Schermata_Menu.png")
        bgmenu = pygame.transform.scale(bgmenu, (display_width,display_height))
        bgmenu_rect = bgmenu.get_rect()
        display.blit(bgmenu, bgmenu_rect)
        title=text_format("Micro Turismo", font, 90, red)
        text_start=text_format("START (A)", font, 75, white)
        text_quit=text_format("QUIT (B)", font, 75, white)
 
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        display.blit(text_start, (display_width/2 - (start_rect[2]/2), 300))
        display.blit(text_quit, (display_width/2 - (quit_rect[2]/2), 400))
        pygame.display.update()
        clock.tick(FPS)

def main():
    
    file="MAPPA_1_CERCHIO.txt"
    rm=Read_Microbit()
    
    mappa,wide,height=leggiMatrice(file)
    print(len(mappa),len(mappa[0]))
    global button_a1
    global button_b1
    global button_a2
    global button_b2
    scala=10#Costante per dimensionare l'altezza e larghezza dello schermo
    display = pygame.display.set_mode((wide*scala, height*scala))
    background = pygame.image.load("./images/Schermata_Circuito.png").convert_alpha()
    vittoria1 = pygame.image.load("./images/winner_pg1.png").convert_alpha()
    vittoria2 = pygame.image.load("./images/winner_pg2.png").convert_alpha()
    loading = pygame.image.load("./images/Schermata_loading.png").convert_alpha()
    rm.start()
    menu_inziale(display,wide*scala,height*scala)
    global q
    q.queue.clear()
    rec= Receiver()
    pg1=Car(mappa, display, scala,11,q,"./images/PG2.png", button_a1, button_b1,(51*scala,7*scala))
    pg2=Car(mappa,display,scala,12,q2,"./images/PG1.png", button_a2, button_b2,(51*scala,18*scala))
    pg1.start()
    pg2.start()
    rec.start()
    

    while pg1.giri!= 2 and pg2.giri!= 2: # main game loop, vengono effettuati n giri(contaGiri-1/2)
        pg1.button_a=button_a1
        pg1.button_b=button_b1
        pg2.button_a=button_a2
        pg2.button_b=button_b2
        display.fill((0,0,0))
        display.blit(background, (0, 0))
        time.sleep(0.08)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.flip()
    
    rec.terminate()
    pg2.terminate()
    rm.terminate()
    pg1.terminate()
    pg2.join()
    rec.join()
    pg1.join()
    rm.join()
    if pg1.giri== 2:
        display.blit(vittoria1,(0,0))
    else:
        display.blit(vittoria2,(0,0))
    pygame.display.flip()
    time.sleep(3)
    
    """rm.terminate()
    rec.terminate()
    pg1.terminate()
    pg2.terminate()"""
    
    pygame.quit()
    quit()
        
if __name__=="__main__":
    main()