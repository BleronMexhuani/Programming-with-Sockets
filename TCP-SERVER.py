import socket
import sys
import datetime
import random
from _thread import *


host = 'localhost'
port = 13000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serverSocket.bind((host, port))
except socket.error:
    print("Startimi i serverit deshtoi!")
    sys.exit()
print("Serveri ka startuar ne hostin "+host+" me port "+str(port))

serverSocket.listen(5)
print("Serveri eshte i gatshem te pranoje kerkesa...\n\n")

def ipaddr(adresa):
    return adresa[0]

def portnr(adresa):
    return adresa[1]

def count(text):
    string2=text.upper()                              
    zanore=0        
    bashktingllore=0                                           
    for char in string2:                                   
        if char in 'AEIOUY':                               
            zanore += 1
        elif (char.isalpha()) == True:
            bashktingllore += 1                                    
    return str("\" " + text+"\""+" ka " + str(zanore) + " zanore dhe " + str(bashktingllore) + " bashketingellore") 

def reverse(text):
    return text[::-1].strip() 

def palindrome(text):
    string1 = text.replace(" ","") 
    if(string1[::1]==string1[::-1]):
      return True
    else:
      return False    

def time():
    now = datetime.datetime.now()
    return "Data dhe koha tani: " + now.strftime("%d.%m.%Y , %I:%M:%S %p")

def game():
    answer = set()
    i = 0
    while i < 5:
        r = random.randint(1,35)
        if r not in answer:
            i += 1
            answer.add(r)
    return str(sorted(answer)).replace('[', '(').replace(']', ')')


def konverto(opsioni, vlera):
    if opsioni=="cmToFeet":
        rezultati=vlera / 30.4

    elif opsioni=="FeetToCm":
        rezultati=vlera * 30.4 

    elif opsioni=="kmToMiles":
        rezultati = vlera / 1.6

    elif opsioni=="MileToKm":
        rezultati = vlera * 1.6
    else:
        rezultati="Zgjedhni njeren nga opcionet"
    return str(round(rezultati, 2))

def gcf(nr1,nr2):
    while nr2 != 0:
        (nr1, nr2) = (nr2, nr1 % nr2)
    return nr1

#metodat extra
def decToBinary(number):
    binaryNum=[0]*number
    i=0
    answer=[]
    while(number>0):
        binaryNum[i]=number%2
        number=int(number/2)
        i+=1
    for j in range(i-1,-1,-1):
         answer.append(binaryNum[j])
    return str(answer)


def client_thread(conn,address):
    try:
        while True:
            methodByte = conn.recv(128)
            method = methodByte.decode("utf-8")

            select=str(method).split(" ")
            teksti = ""
            i = len(select)
            for fjala in range (1,i):
                teksti += select[fjala]
                if(fjala!=i):
                    teksti +=" "

            if not method:
                break
            if  (select[0]=="IPADDRESS"):
                answer = "IP adresa e Klientit eshte: " + ipaddr(address)
            elif (select[0]=="PORT"):
                answer = "Klienti eshte duke perdorur portin " + str(portnr(address))
            elif (select[0]=="COUNT"):
                if not teksti.strip():
                    answer = "Shkruani ndonje fjal apo fjali!"
                else:
                    answer = (count(teksti))
            elif(select[0]=="REVERSE"):                                                      
                if not teksti.strip():
                    answer="Shkruani ndonje fjal apo fjali!"
                else:
                    answer="Fjalia e kthyer mbrapsht:"+reverse(teksti)                
            elif(select[0]=="PALINDROME"):
                if not teksti.strip():
                    answer="Shkruani ndonje fjal apo fjali!"
                else:
                    answer=str(palindrome(teksti))
            elif (select[0]=="TIME"):
                    answer = time()
            elif (select[0]=="GAME"):
                    answer = game()
            elif(select[0]=="CONVERT"):
                try:
                    numri=float(select[2]) 
                    answer="Vlera e konvertuar eshte: "+str(konverto(select[1], numri))               
                except Exception:
                    answer="Argument jo valid!"
            elif(select[0]=="GCF"):
                try:
                    numri1=int(select[1])
                    numri2=int(select[2])
                    answer="Faktori me i madh i perbashket eshte: "+str(gcf(numri1,numri2))
                except Exception:
                    answer="Argument jo valid!"
            elif(select[0]=="DECTOBINARY"):
                try:
                    numri=int(select[1])
                    answer="Numri binar eshte : "+str(decToBinary(numri))
                except Exception:
                    answer="Argument jo valid"
            elif(select[0]=="lottery"):
                try:
                    number=int(select[2])
                    answer=(lottery(number))
                except Exception:
                    answer="Argumente gabim"
            else:
                answer = "Keni dhene nje komande jo valide!"
                print("Klienti ka dhene komande jo valide!")
            conn.sendall(str.encode(answer))
            print("Klientit " + "|" + address[0]+ "|" + " iu dergua pergjigja: " + "/" + str(answer) + "/")
        conn.close()
    except ConnectionResetError:
        print("\nKlienti humbi lidhjen me server!\n")
    except ConnectionAbortedError: 
        print("\nKlienti humbi lidhjen me server!\n")


while True:
    connection, address = serverSocket.accept()
    print("""Serveri u lidh me klientin """ + address[0] + " me port "+ str(address[1]) +"\n")
    start_new_thread(client_thread, (connection,address,))

serverSocket.close()
