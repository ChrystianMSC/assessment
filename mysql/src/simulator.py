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
    try:
        dataType, protocol, utcTime, status, identifier = generateRandomData()

        # Verifique se os dados são válidos antes de criar o pacote
        if not (1 <= dataType <= 2) or not (66 <= protocol <= 68):
            raise ValueError("Tipo de dados ou protocolo inválido")

        packet = f">DATA{dataType},{protocol},{utcTime},{status};ID={identifier}<"
        print("\nEnviando dado:")
        print("\n" + packet)
        socket.sendto(packet.encode('utf-8'), (udpIp, udpPort))
    except ValueError as e:
        print(f"Erro ao gerar dados: {e}")
        # Aqui você pode adicionar qualquer lógica adicional ou tratamento necessário.


def simulator(udpIp, udpPort):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Simulador iniciado, dados serão enviados a cada 5 segundos. \nCtrl + C para encerrar o simulador")

    try:
        while True:
            sendDataToServer(clientSocket, udpIp, udpPort)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulador interrompido.")
    finally:
        closeSimulator(clientSocket)
        
def closeSimulator(clientSocket):
    clientSocket.close()

if __name__ == "__main__":
    udpIp = "127.0.0.1"
    udpPort = 12345

    simulator(udpIp, udpPort)