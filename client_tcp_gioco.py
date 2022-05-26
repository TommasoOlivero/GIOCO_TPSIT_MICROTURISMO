#Client TCP : gioco Micro Turismo
__author__='Coppola Carmine Mattia & Olivero Tommaso'

#importazione librerie necessarie
import socket
import threading
import queue
import sys
import serial
import time

q = queue.Queue()

#classe thread per la lettura dei dati ricevuti da microbit
class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
      
    def terminate(self):
        self.running = False
        
    def run(self):
        port = "COM33"
        s = serial.Serial(port)             #porta seriale del microbit
        s.baudrate = 115200
        while self.running:
            data = s.readline().decode()    #lettura dati dalla porta seriale
            acc = data.split(",")
            q.put(data)                     #inserimento dei dati nella coda
            #print(acc[0])
            #print(acc[1])
            #print(acc[2])
        
def main():
    rm = Read_Microbit()                                    #thread per la continua ricezione dei dati
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creazione del socket TCP
    rm.start()                                              #inizio ricezione dei dati da micro bit
    s.connect(("192.168.10.168", 8000))                      #connessione al server centrale 
    while True:
        dati = str(q.get())                                 #conversione in stringa i dati
        print(dati)      
        s.sendall(dati.encode())                            #invio dati al server

if __name__ == "__main__":
    main()