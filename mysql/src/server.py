import os
import socket
import json
from datetime import datetime
from dotenv import load_dotenv
from database import DBConnector

load_dotenv()

class UDPServer:
    def __init__(self, udp_ip, udp_port, db_connector):
        self.udpIp = udp_ip
        self.udpPort = udp_port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((udp_ip, udp_port))
        self.db_connector = db_connector

        print("Servidor iniciado, dados serão recebidos. \nCtrl + C para encerrar o servidor")

    def parseData(self, packet):
        try:
            cleanPacket = packet.strip("><")

            parts = cleanPacket.split(',')

            typeVal = int(parts[0].replace("DATA", ""))
            protocoloVal = int(parts[1])
            utcVal = datetime.strptime(parts[2], "%y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            statusVal = int(parts[3].split(';')[0])
            idVal = parts[3].split('=')[1]

            parsedData = {
                "type": typeVal,
                "protocolo": protocoloVal,
                "utc": utcVal,
                "status": statusVal,
                "id": idVal
            }

            return parsedData

        except Exception as e:
            print(f"Erro ao analisar o pacote: {e}")
            return None

    def receiveAndStoreData(self):
        while True:
            try:
                self.serverSocket.settimeout(1)

                data, addr = self.serverSocket.recvfrom(1024)
                packet = data.decode('utf-8')
                parsedData = self.parseData(packet)

                if parsedData:
                    self.db_connector.storeDataInDatabase(parsedData)
                    self.storeDataInJson(parsedData)
                    print(parsedData)

            except socket.timeout:
                pass

            except KeyboardInterrupt:
                print("O servidor foi encerrado")
                break

        self.closeConnections()

    def storeDataInJson(self, parsedData):
        try:
            if os.path.exists('../json/parsedData.json'):
                with open('../json/parsedData.json', 'r') as jsonFile:
                    existingJson = json.load(jsonFile)
            else:
                existingJson = []

            existingJson.append(parsedData)

            with open('../json/parsedData.json', 'w') as jsonFile:
                json.dump(existingJson, jsonFile, indent=4)

        except Exception as e:
            print(f"Erro ao armazenar dados no arquivo JSON: {e}")

    def closeConnections(self):
        self.serverSocket.close()
        self.db_connector.closeConnections()

if __name__ == "__main__":
    udpIp = "127.0.0.1"
    udpPort = 12345

    db_connector = DBConnector()
    udpServer = UDPServer(udpIp, udpPort, db_connector)
    udpServer.receiveAndStoreData()