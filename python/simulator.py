import socket
import random
import time

def generateRandomData():
    dataType = random.choice([1, 2])
    protocol = random.choice([66, 67, 68])
    utcTime = time.strftime("%y%m%d%H%M%S", time.gmtime())
    status = random.choice([0, 1])
    identifier = ''.join(random.choice('0123456789ABCDEF') for _ in range(3))

    return dataType, protocol, utcTime, status, identifier

def sendDataToServer(socket, udpIp, udpPort):
    dataType, protocol, utcTime, status, identifier = generateRandomData()

    packet = f">DATA{dataType},{protocol},{utcTime},{status};ID={identifier}<"
    print("\nEnviando dado:")
    print("\n" + packet)
    socket.sendto(packet.encode('utf-8'), (udpIp, udpPort))

def simulator(udpIp, udpPort):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Simulador iniciado, dados serão enviados a cada 3 segundos. \nCtrl + C para encerrar o simulador")
    time.sleep(3)

    try:
        while True:
            sendDataToServer(clientSocket, udpIp, udpPort)
            time.sleep(3)
    except KeyboardInterrupt:
        print("Simulador interrompido.")
    finally:
        clientSocket.close()

if __name__ == "__main__":
    udpIp = "127.0.0.1"
    udpPort = 12345

    simulator(udpIp, udpPort)