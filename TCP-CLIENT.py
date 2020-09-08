import socket

serverName = ""
serverPort = 0

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conn = True
while conn:
    conn = False
    try:
        serverName = input("Host: ")
        serverPort = int(input("Port: "))
        clientSocket.connect((serverName, serverPort))       
    except Exception as e:
        conn = True
        input("Lidhja me server u pamundesua,provoni perseri(ENTER)")

print("""===============================================================
Jeni lidhur ne serverin me host ""","|",serverName,"|"," ne portin ",serverPort)

try:
    print("""================================================================
Shkruani me shkronja te medha komanden qe doni ta perdorni:               
\ IPADDRESS                                      
\ PORT                        
\ COUNT <HAPSIRE> <tekst>      
\ REVERSE <HAPSIRE> <tekst>                                                
\ PALINDROME <HAPSIRE> <tekst>                   
\ TIME                         
\ GAME
\ GCF <HAPSIRE> <NR1> <HAPSIRE> <NR2>   
\ CONVERT <HAPSIRE> Opcioni<cmToFeet,FeetToCm,kmToMiles,MileToKm> <HAPSIRE> <NR>
\DECTOBINARY <HAPSIRE> <NR>
\ CHANGE (Per te ndryshuar lidhjen me server)     
Shkruaj \"EXIT\" per te ndaluar programi!\n """)  
    while True:              
        method = input("KOMANDA \\ ")
        if method.upper() == "EXIT":
            break
        elif method == '':
            print("Shkruani njeren nga komandat me siper!")   
        elif method == "CHANGE":
            print("================================================================")
            try:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverName1 = input("Host: ")
                serverPort1 = int(input("Port: "))
                clientSocket.connect((serverName1, serverPort1)) 
            except socket.error as msg:
                print("Socket creation error: "+str(msg))
            print("""===================================\nJeni lidhur ne serverin me host ""","|",serverName1,"|"," ne portin ",serverPort1,"\n")   
        else:
            clientSocket.sendall(str.encode(method))
            serverAnswerByte = clientSocket.recv(128)
            serverAnswer = serverAnswerByte.decode("utf-8")
            print(serverAnswer)
            print("Vazhdoni me kerkese tjeter ose shkruaj EXIT per dalje.")           
except TimeoutError:
        print("Serveri morri shume kohe per tu pergjigjur andaj lidhja u mbyll!")

clientSocket.close()
