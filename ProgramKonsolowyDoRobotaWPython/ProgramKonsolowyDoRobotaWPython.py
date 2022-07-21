import threading
import DobotDllType as dType
import socket
import math
import os
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
print(" Program do obs³ugi bezprzewodowej robota Dobot Magician wyposa¿onego w g³owicê laserow¹\n")
print(" Przed pierwszym uruchomieniem ustaw g³owicê lasera w odpowiednim\n miejscu uwzglêdniaj¹æ, ¿e maksmylna d³ugoœæ graweru wynosi 100mm\n")
print(" Witaj, program ten ma na celu odbraæ frazê, skonwertowaæ odebrany ci¹g znaków na \n odpowiednie ruchy ramienia robota i wypaliæ za pomoc¹ lasera.\n")
print(" UWAGA! Do poprawnego dzia³ania skryptu udz¹dzenie nadaj¹ce(smartfon)\n MUSI znajdowaæ siê w TEJ SAMEJ sieci lokalnej\n Mi³ego grawerowania :)\n")
print(" Wpisz ten adres w aplikacji na smartfonie: " + get_ip())
HOST = get_ip()
PORT = 7800
s = socket.socket()
print('\n Otwarcie gniazda')
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print(' Uruchomienie nieudane: ' .format(err))
s.listen(2)
print(" Oczekiwanie na dane...")
conn, addr = s.accept()
print(" Uda³o siê po³¹czyæ z: ",addr,"\n")
message = conn.recv(1024).decode()
str = message
h = (str[-1:])
print(" Twój grawer to: " + str[:-1])
if (h == "M"):
    print(" Wybra³eœ mniejsz¹ czcionkê")
else:
    print(" Wybra³eœ wieksz¹ czcionkê")
conn.close()
print(" Zamkniêcie gnizda. Rozpoczynam proces grawerowania... ")
print()
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
#Za³aduj Bilbioteki Dll i Pobierz Objekty CDLL
api = dType.load() #za³adowanie API
state = dType.ConnectDobot(api, "", 115200)[0] #£¹czenie z Dobotem
print()
print("Status po³¹czenia: ",CON_STR[state])
if (state == dType.DobotConnect.DobotConnect_NoError):
    dType.SetQueuedCmdClear(api) #Czyszczenie Kolejki
    LI = dType.GetQueuedCmdCurrentIndex(api)[0]; #Zdefiniowanie licznika kolejki
    dType.SetCPParams(api,8,8,8,0,isQueued=1); LI+=1 #Ustawienia Parametrów Ruchu
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1); LI+=1 #Ustawienia Parametrów Ruchu
    print('start')
    pos = dType.GetPose(api) #Odczytanie aktualnej pozycji koñcówki manipulatora
    s = pos[0]
    w = pos[1]
    z = pos[2]
    rHead = pos[3]
    z = -32
    dType.SetPTPCmd(api, 2, x, y, z, rHead, isQueued=1); LI+=1 #Ruch robota typu PTP
    i = 0
    x_pocz = s;
    y_pocz = w;
    str1=str[:-1]
    liczba_znakow = len(str1)
    if(liczba_znakow >= 33): #Funkcja wyboru, zabezpiecza przed zbyt d³ugim ci¹giem znaków
        liczba_znakow = 32
    while i < liczba_znakow: #Funkcja zapêtlaj¹ca czeœæ kodu
        p = str1[i] #Przypisanie do zmiennej "p" aktualnie wypalanego znaku
        if(p=="A" and h=="M"): #Funkcja warunkowa dla pewnej grupy wyra¿eñ
            x1=s+9.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1 #Instrukcja wykonania ruchu typu CP
            x1=s+7.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.6; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.2; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.7; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 13;   
        elif(p=="A" and h=="D"):
            x1=s+18.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.3; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=22
        elif(p=="a" and h=="M"):
            x1=s+6.3; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.1; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.1; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.1; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.5; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="a" and h=="D"):
            x1=s+13.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+14.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+14.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.4; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.2; y1=w+13.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.5; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="¥" and h=="M"):
            x1=s+10.4; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.0; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+9.8; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+7.4; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.2; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.7; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 14;
        elif(p=="¥" and h=="D"):
            x1=s+20.8; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+20.1; y1=w-5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+19.6; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.1; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.5; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.8; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.5; y1=w-4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.4; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.5; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.8; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.9; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.7; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.7; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.1; y1=w-3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.8; y1=w-3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.9; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.4; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.9; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+20.5; y1=w-3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+20.7; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+20.8; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+20.8; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=24
        elif(p=="¹" and h=="M"):
            x1=s+8.2; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.8; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.6; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w-2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.1; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.5; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="¹" and h=="D"):
            x1=s+16.9; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+16.2; y1=w-5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+15.7; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.2; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w-4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w-0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+14.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+14.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+13.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w-0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w-3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w-3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.0; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.5; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w-3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.8; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.9; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.9; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.7; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.7; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=21
        elif(p=="B" and h=="M"):
            x1=s+7.5; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.4; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.2; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.2; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.1; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.1; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.1; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.9; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=12
        elif(p=="B" and h=="D"):
            x1=s+15.2; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.0; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.6; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+19.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+19.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.4; y1=w+19.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+16.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+15.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+14.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+11.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+10.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.8; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.2; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.2; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.7; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+15.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.5; y1=w+16.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+16.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+12.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.4; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.3; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.0; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="b" and h=="M"):
            x1=s+6.6; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.5; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.2; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.1; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.8; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="b" and h=="D"):
            x1=s+13.2; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.0; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.7; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.0; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+13.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.3; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.7; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="C" and h=="M"):
            x1=s+8.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.9; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.6; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="C" and h=="D"):
            x1=s+16.6; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+15.3; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.7; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+19.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+18.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.4; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+16.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+16.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+16.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+13.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.9; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.4; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="c" and h=="M"):
            x1=s+6.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1            
            s += 10
        elif(p=="c" and h=="D"):
            x1=s+12.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.8; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+14.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+14.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+14.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="Æ" and h=="M"):
            x1=s+8.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.6; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.4; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.6; y1=w+11.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.5; y1=w+11.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1          
            s += 12
        elif(p=="Æ" and h=="D"):
            x1=s+16.6; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+15.3; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.7; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+19.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+18.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.4; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+16.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+16.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+16.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+13.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.9; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.4; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.9; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.2; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+7.2; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="æ" and h=="M"):
            x1=s+6.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.4; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="æ" and h=="D"):
            x1=s+12.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.8; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+14.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+14.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+14.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.8; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.1; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.1; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="D" and h=="M"):
            x1=s+8.4; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.8; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+7.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.9; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="D" and h=="D"):
            x1=s+17.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+16.8; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+15.9; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.5; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+19.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+19.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+19.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+16.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.9; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.8; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+14.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+14.1; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+16.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=21
        elif(p=="d" and h=="M"):
            x1=s+6.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.3; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.3; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.3; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1                
            s += 10
        elif(p=="d" and h=="D"):
            x1=s+13.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.6; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="E" and h=="M"):
            x1=s+6.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s-0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1        
            s += 10
        elif(p=="E" and h=="D"):
            x1=s+13.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.3; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="e" and h=="M"):
            x1=s+6.8; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+1.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.3; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.5; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1              
            s += 11
        elif(p=="e" and h=="D"):
            x1=s+13.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.7; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.0; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.2; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.9; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.2; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="Ê" and h=="M"):
            x1=s+6.9; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.5; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.3; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w-2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11              
        elif(p=="Ê" and h=="D"):
            x1=s+14.1; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.4; y1=w-5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.9; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w-4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w-3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w-3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.2; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.8; y1=w-3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=18
        elif(p=="ê" and h=="M"):
            xx1=s+6.8; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+1.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.3; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w-2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w-0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w-0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.5; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="ê" and h=="D"):
            x1=s+13.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.7; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w-0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w-1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w-3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w-3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.4; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w-3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w-3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w-5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w-4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.0; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.2; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.9; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.2; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="F" and h=="M"):
            x1=s+6.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+1.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.3; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="F" and h=="D"):
            x1=s+13.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.9; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="f" and h=="M"):
            x1=s+4.8; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.7; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.5; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 9
        elif(p=="f" and h=="D"):
            x1=s+9.7; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.5; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.1; y1=w+18.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+18.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+18.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+17.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+15.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+15.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+19.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+20.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+21.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+21.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+20.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+20.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=14
        elif(p=="G" and h=="M"):
            x1=s+8.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.0; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 13
        elif(p=="G" and h=="D"):
            x1=s+17.9; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+16.3; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.3; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+14.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+19.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.9; y1=w+18.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.9; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.7; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.2; y1=w+15.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.5; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.6; y1=w+16.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.9; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+13.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.9; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=22
        elif(p=="g" and h=="M"):
            x1=s+6.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.3; y1=w-0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.7; y1=w-1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w-2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w-2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w-1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w-1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w-0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.3; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="g" and h=="D"):
            x1=s+13.2; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.7; y1=w-1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+11.5; y1=w-3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w-5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w-5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w-3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w-2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w-0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+13.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.7; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.7; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.7; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="H" and h=="M"):
            x1=s+7.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="H" and h=="D"):
            x1=s+15.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.9; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.5; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="h" and h=="M"):
            x1=s+6.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.0; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10              
        elif(p=="h" and h=="D"):
            x1=s+12.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.1; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.2; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="i" and h=="M"):
            x1=s+1.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.0; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+1.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.1; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 5
        elif(p=="i" and h=="D"):
            x1=s+3.3; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.5; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.5; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+3.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.7; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=7
        elif(p=="I" and h=="M"):
            x1=s+4.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.1; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 8
        elif(p=="I" and h=="D"):
            x1=s+7.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.0; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=12
        elif(p=="J" and h=="M"):
            x1=s+4.8; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.5; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.9; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 9
        elif(p=="J" and h=="D"):
            x1=s+9.6; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+8.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=14
        elif(p=="j" and h=="M"):
            x1=s+4.1; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.7; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.7; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+4.0; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.8; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.4; y1=w-2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w-1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w-1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w-1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 18
        elif(p=="j" and h=="D"):
            x1=s+8.1; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.3; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.3; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+7.9; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.5; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.6; y1=w-4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w-5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w-5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w-2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w-3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w-3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w-3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w-3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w-2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w-1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=12
        elif(p=="K" and h=="M"):
            x1=s+8.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.4; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="K" and h=="D"):
            x1=s+16.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+4.7; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.7; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="k" and h=="M"):
            x1=s+6.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="k" and h=="D"):
            x1=s+13.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+4.2; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="L" and h=="M"):
            x1=s+6.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="L" and h=="D"):
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="l" and h=="M"):
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.1; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="l" and h=="D"):
            x1=s+2.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.1; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="£" and h=="M"):
            x1=s+7.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.3; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="£" and h=="D"):
            x1=s+14.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+1.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+1.4; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-1.0; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-1.0; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=18
        elif(p=="³" and h=="M"):
            x1=s+3.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 8
        elif(p=="³" and h=="D"):
            x1=s+6.4; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+3.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.8; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.8; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+20.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+14.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=10
        elif(p=="M" and h=="M"):
            x1=s+9.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.6; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 13
        elif(p=="M" and h=="D"):
            x1=s+18.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+15.6; y1=w+17.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+17.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=22
        elif(p=="m" and h=="M"):
            x1=s+11.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.7; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+9.7; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 15
        elif(p=="m" and h=="D"):
            x1=s+22.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+19.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+19.6; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.6; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.5; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.4; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.1; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.8; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.3; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.7; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.6; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.6; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.5; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+14.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+14.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+14.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.9; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.3; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.6; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+20.9; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+21.8; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+22.1; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+22.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=26
        elif(p=="N" and h=="M"):
            x1=s+7.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="N" and h=="D"):
            x1=s+15.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.9; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.7; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="n" and h=="M"):
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.1; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="n" and h=="D"):
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.3; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="Ñ" and h=="M"):
            x1=s+7.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.1; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.2; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.2; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="Ñ" and h=="D"):
            x1=s+15.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.9; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.7; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.3; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.6; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.6; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="ñ" and h=="M"):
            x1=s+6.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.4; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.6; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="ñ" and h=="D"):
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.3; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.7; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.0; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.0; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="O" and h=="M"):
            x1=s+8.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.7; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+9.1; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+8.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.8; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.2; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="O" and h=="D"):
            x1=s+15.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+16.4; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+17.2; y1=w+14.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.7; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.2; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+20.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+15.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+14.6; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.4; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="o" and h=="M"):
            x1=s+7.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.8; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.1; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.6; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.2; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s+=11
        elif(p=="o" and h=="D"):
            x1=s+13.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.5; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+11.1; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.7; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.3; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="Ó" and h=="M"):
            x1=s+8.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.7; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+9.1; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+8.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.8; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.2; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.7; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.8; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.8; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="Ó" and h=="D"):
            x1=s+15.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+16.4; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+17.2; y1=w+14.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.7; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.2; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+20.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.3; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+15.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+14.6; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.4; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.3; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.6; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.6; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="ó" and h=="M"):
            x1=s+7.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.8; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.1; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.6; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.2; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.7; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="ó" and h=="D"):
            x1=s+13.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.5; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+11.1; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.7; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.3; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.3; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.6; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+4.6; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="P" and h=="M"):
            x1=s+6.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.4; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.2; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.0; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="P" and h=="D"):
            x1=s+13.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.4; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.0; y1=w+11.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+19.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+19.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+18.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+16.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+15.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.7; y1=w+13.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.4; y1=w+15.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+16.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+16.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+17.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+13.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+13.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="p" and h=="M"):
            x1=s+6.7; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.6; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.4; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.3; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.2; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.9; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="p" and h=="D"):
            x1=s+13.4; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.3; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.9; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.4; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+13.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+14.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.8; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.5; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.9; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+12.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="R" and h=="M"):
            x1=s+8.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.7; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.4; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.3; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.2; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="R" and h=="D"):
            x1=s+17.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.8; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+18.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.2; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+16.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+14.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+10.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.8; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.7; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.5; y1=w+15.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+16.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+17.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=21
        elif(p=="r" and h=="M"):
            x1=s+4.7; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.7; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.4; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 9
        elif(p=="r" and h=="D"):
            x1=s+9.6; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.5; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+8.9; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+10.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+14.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=14
        elif(p=="S" and h=="M"):
            x1=s+7.7; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.6; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.4; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="S" and h=="D"):
            x1=s+15.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+14.9; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.5; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+14.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+16.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+18.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+18.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+15.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w+15.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+16.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+16.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="s" and h=="M"):
            x1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.7; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.1; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="s" and h=="D"):
            x1=s+11.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.5; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+14.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+14.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+12.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=15
        elif(p=="Œ" and h=="M"):
            x1=s+7.9; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.8; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.6; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.9; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="Œ" and h=="D"):
            x1=s+15.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+14.9; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.5; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+14.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+16.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+18.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+18.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w+15.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w+15.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+16.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+16.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.1; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.4; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.4; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="œ" and h=="M"):
            xx1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.7; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.1; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+3.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.0; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="œ" and h=="D"):
            x1=s+11.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.5; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+14.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+14.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+14.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+12.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+9.3; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.7; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+3.7; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=15
        elif(p=="T" and h=="M"):
            x1=s+8.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.9; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="T" and h=="D"):
            x1=s+16.7; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.6; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.7; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.7; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="t" and h=="M"):
            x1=s+5.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 9
        elif(p=="t" and h=="D"):
            x1=s+10.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+8.5; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+19.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+19.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=14
        elif(p=="U" and h=="M"):
            x1=s+7.9; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.8; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.6; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="U" and h=="D"):
            x1=s+15.8; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.7; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+15.3; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.7; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.2; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="u" and h=="M"):
            x1=s+6.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.2; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="u" and h=="D"):
            x1=s+13.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.4; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="V" and h=="M"):
            x1=s+9.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 1
        elif(p=="V" and h=="D"):
            x1=s+17.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.6; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.7; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=21
        elif(p=="v" and h=="M"):
            x1=s+7.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="v" and h=="D"):
            x1=s+14.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="W" and h=="M"):
            x1=s+12.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+8.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 16
        elif(p=="W" and h=="D"):
            x1=s+24.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+19.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+16.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+16.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.1; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+22.3; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+24.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=28
        elif(p=="w" and h=="M"):
            x1=s+10.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 14
        elif(p=="w" and h=="D"):
            x1=s+20.3; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+16.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.2; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+20.3; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=24
        elif(p=="Q" and h=="M"):
            x1=s+9.8; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+9.4; y1=w-2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+9.0; y1=w-2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w-0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w-1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w-1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w-1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w-1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w-1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+8.2; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.9; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+7.3; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 14
        elif(p=="Q" and h=="D"):
            x1=s+19.5; y1=w-4.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+18.7; y1=w-5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+17.9; y1=w-5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.1; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.3; y1=w-5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w-4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w-3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w-2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+20.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.2; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.5; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.6; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.4; y1=w+14.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.9; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.6; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.8; y1=w-1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.3; y1=w-2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.1; y1=w-2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.7; y1=w-2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+17.3; y1=w-2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.0; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+18.8; y1=w-2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.1; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.5; y1=w-2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+19.5; y1=w-4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+16.3; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+15.8; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+14.6; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.5; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.3; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.3; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=24
        elif(p=="q" and h=="M"):
            x1=s+6.8; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.6; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.6; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.6; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.0; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="q" and h=="D"):
            x1=s+13.6; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+11.1; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+11.1; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+13.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+14.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.2; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.1; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+11.1; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.0; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+12.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+11.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="Y" and h=="M"):
            x1=s+8.4; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.9; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="Y" and h=="D"):
            x1=s+15.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+8.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="y" and h=="M"):
            xx1=s+7.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.4; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.0; y1=w-2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="y" and h=="D"):
            x1=s+14.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.6; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.9; y1=w-5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=18
        elif(p=="X" and h=="M"):
            x1=s+9.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+9.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 13
        elif(p=="X" and h=="D"):
            x1=s+16.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.0; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+16.9; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.9; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=21
        elif(p=="x" and h=="M"):
            x1=s+7.7; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+4.0; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="x" and h=="D"):
            x1=s+14.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+11.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+7.0; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=18
        elif(p=="Z" and h=="M"):
            x1=s+8.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.2; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="Z" and h=="D"):
            x1=s+16.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.2; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="z" and h=="M"):
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="z" and h=="D"):
            x1=s+12.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.2; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="" and h=="M"):
            x1=s+8.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+6.1; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.3; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.3; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="" and h=="D"):
            x1=s+16.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.2; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+12.0; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+8.3; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.3; y1=w+22.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.0; y1=w+27.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="Ÿ" and h=="M"):
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="Ÿ" and h=="D"):
            x1=s+12.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.2; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+9.8; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.2; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+4.2; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="¯" and h=="M"):
            x1=s+8.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.1; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+3.6; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+3.6; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 12
        elif(p=="¯" and h=="D"):
            x1=s+16.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.0; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.2; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+16.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+9.9; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.0; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+7.0; y1=w+25.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+25.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+22.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=20
        elif(p=="¿" and h=="M"):
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+3.9; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+2.5; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="¿" and h=="D"):
            x1=s+12.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.2; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+12.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+7.6; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.8; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+4.8; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=16
        elif(p=="0" and h=="M"):
            x1=s+7.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.5; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.6; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="0" and h=="D"):
            x1=s+14.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+14.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.9; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+19.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+20.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+19.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.1; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.1; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+11.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+11.7; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.8; y1=w+12.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+13.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+16.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+16.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+15.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+13.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="1" and h=="M"):
            x1=s+5.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.1; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="1" and h=="D"):
            x1=s+11.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+0.5; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+17.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+17.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+18.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+18.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+19.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=14
        elif(p=="2" and h=="M"):
            x1=s+6.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+0.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.0; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+1.4; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+6.8; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="2" and h=="D"):
            x1=s+13.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s-0.0; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s-0.0; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+13.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+14.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+16.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+17.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+19.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+18.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+14.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.0; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="3" and h=="M"):
            x1=s+5.9; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.2; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.4; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="3" and h=="D"):
            x1=s+11.7; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.3; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.8; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.2; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+3.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+0.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+11.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.5; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+15.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+15.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+16.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+16.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+17.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+19.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+19.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.7; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+19.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+19.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.6; y1=w+16.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+15.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.8; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=15
        elif(p=="4" and h=="M"):
            x1=s+7.6; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.1; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+4.8; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.8; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+0.9; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="4" and h=="D"):
            x1=s+15.8; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+12.8; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.8; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+15.8; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.2; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.2; y1=w+16.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+2.5; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=19
        elif(p=="5" and h=="M"):
            x1=s+6.7; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.4; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+6.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 10
        elif(p=="5" and h=="D"):
            x1=s+13.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.4; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.0; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.4; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.3; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.1; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+7.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+12.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+11.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.2; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.0; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+8.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="6" and h=="M"):
            x1=s+7.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.9; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.8; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.2; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.8; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.7; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+5.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+4.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+0.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="6" and h=="D"):
            x1=s+14.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.5; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+12.0; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.1; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+11.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+13.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+15.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+17.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+19.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.2; y1=w+20.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+20.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.1; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.9; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.2; y1=w+18.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+17.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+16.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+14.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+12.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+12.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.6; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.6; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.7; y1=w+10.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.4; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.8; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+14.0; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+11.2; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.9; y1=w+8.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.4; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.7; y1=w+9.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.0; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.6; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+10.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.5; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+1.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+2.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+2.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="7" and h=="M"):
            x1=s+7.1; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+2.6; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+1.1; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="7" and h=="D"):
            x1=s+13.8; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+4.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+1.8; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.8; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.8; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="8" and h=="M"):
            x1=s+7.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+6.9; y1=w+1.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.1; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+0.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.1; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.5; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.0; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+6.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.6; y1=w+4.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.1; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.5; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.4; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.0; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+6.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+6.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+5.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.5; y1=w+7.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.7; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.7; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.5; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.4; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+3.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+1.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+2.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11           
        elif(p=="8" and h=="D"):
            x1=s+13.9; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.3; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+11.8; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w-0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+3.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.3; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.0; y1=w+7.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+10.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.4; y1=w+13.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.7; y1=w+17.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+18.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+20.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+20.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+19.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+17.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.3; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+14.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.5; y1=w+12.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.5; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+10.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.7; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.9; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.6; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.9; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+10.7; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.4; y1=w+16.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+9.6; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+18.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+18.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w+16.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+15.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.0; y1=w+14.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+13.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.0; y1=w+13.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.1; y1=w+12.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.6; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.5; y1=w+11.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.3; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.5; y1=w+12.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+13.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.5; y1=w+14.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.7; y1=w+15.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.1; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.9; y1=w+6.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.5; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.4; y1=w+8.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+8.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+7.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+4.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+2.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+1.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.6; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+2.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.8; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.1; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p=="9" and h=="M"):
            x1=s+7.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+7.0; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+6.7; y1=w+3.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+2.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.8; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+0.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.8; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+1.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+1.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.3; y1=w+0.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.7; y1=w+1.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+1.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.3; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+4.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.0; y1=w+3.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.3; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+3.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+3.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.2; y1=w+4.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.6; y1=w+4.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.3; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.0; y1=w+6.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.2; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.0; y1=w+9.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+10.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.8; y1=w+9.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.4; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.7; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.9; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+5.7; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+5.6; y1=w+6.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1
            x1=s+5.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+8.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+8.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.2; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+9.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+9.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.5; y1=w+8.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+8.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+7.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.3; y1=w+6.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.4; y1=w+6.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+5.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.7; y1=w+5.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.1; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.8; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.6; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.1; y1=w+4.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.7; y1=w+4.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+5.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+5.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+5.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.7; y1=w+5.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+5.7; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.7; y1=w+5.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s += 11
        elif(p=="9" and h=="D"):
            x1=s+13.7; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+13.5; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+13.1; y1=w+6.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+4.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+2.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+1.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.2; y1=w+0.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.3; y1=w-0.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.2; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w-0.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w-0.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w-0.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.6; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.0; y1=w+2.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.7; y1=w+2.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.3; y1=w+1.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.0; y1=w+2.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+3.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.2; y1=w+5.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+8.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.6; y1=w+7.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.5; y1=w+7.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.4; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.1; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.9; y1=w+7.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.9; y1=w+7.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.9; y1=w+7.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.9; y1=w+8.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.9; y1=w+9.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+10.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.2; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s-0.4; y1=w+13.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+0.1; y1=w+16.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+1.5; y1=w+18.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+19.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+20.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.9; y1=w+20.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.1; y1=w+19.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.3; y1=w+19.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.3; y1=w+18.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+12.3; y1=w+17.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.1; y1=w+15.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.5; y1=w+13.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.7; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+13.7; y1=w+11.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            x1=s+11.0; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1
            x1=s+10.8; y1=w+13.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1  
            x1=s+10.5; y1=w+15.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.0; y1=w+16.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.4; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.7; y1=w+17.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.0; y1=w+17.9; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.3; y1=w+18.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.4; y1=w+18.2; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.6; y1=w+17.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.4; y1=w+17.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+15.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.2; y1=w+13.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.4; y1=w+12.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+2.6; y1=w+11.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.1; y1=w+10.8; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+3.8; y1=w+10.1; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+4.5; y1=w+9.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.2; y1=w+9.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+5.9; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+6.8; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+7.8; y1=w+9.4; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+8.9; y1=w+9.6; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+9.9; y1=w+10.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+10.5; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+10.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+10.9; y1=w+11.0; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+11.3; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            x1=s+11.0; y1=w+11.7; dType.SetCPLECmd(api,1,x1,y1,z,90,isQueued=1); LI+=1 
            dType.SetCPLECmd(api,1,x1,y1,z,0,isQueued=1); LI+=1; dType.SetWAITCmd(api, 2000, isQueued=1); LI+=1
            s +=17
        elif(p==" " and h=="M"):
            s += 15
        elif(p==" " and h=="D"):
            s += 20
        elif(s>(s+100) and h=="M"):
            s = x_pocz;
            w -= 15;
            x1=s; y1=w;
            dType.SetPTPCmd(api, 2, x1, y1, z, rHead, isQueued=1); LI+=1
        elif(s>(s+100) and h=="D"):
            s = x_pocz;
            w -= 30;
            x1=s; y1=w
            dType.SetPTPCmd(api, 2, x1, y1, z, rHead, isQueued=1);LI+=1
        i+=1
    #Start to Execute Command Queue
    #Wait for Executing Last Command 
    print(dType.GetQueuedCmdCurrentIndex(api)[0])
    print(LI)
    while (LI) > (dType.GetQueuedCmdCurrentIndex(api)[0]):
        dType.dSleep(100)
        print(dType.GetQueuedCmdCurrentIndex(api)[0])
    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)
#Disconnect Dobot
dType.DisconnectDobot(api)
input('Press ENTER to exit')