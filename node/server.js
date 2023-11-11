const dgram = require('dgram');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();
const { DateTime } = require('luxon');

class UDPServer {
    constructor(udpIp, udpPort) {
        this.udpIp = udpIp;
        this.udpPort = udpPort;
        this.serverSocket = dgram.createSocket('udp4');
        this.initializeDatabase();

        console.log("Servidor iniciado, dados serão recebidos. \nCtrl + C para encerrar o servidor");

        this.serverSocket.on('message', (msg, rinfo) => {
            const packet = msg.toString('utf-8');
            const parsedData = this.parseData(packet);

            if (parsedData) {
                this.storeDataInDatabase(parsedData);
                this.storeDataInJson(parsedData);
                console.log(parsedData);
            }
        });

        this.serverSocket.on('error', (err) => {
            console.error(`Erro no servidor: ${err}`);
        });

        this.serverSocket.bind(udpPort, udpIp);
    }

    initializeDatabase() {
        this.db = new sqlite3.Database('db/database.db', (err) => {
            if (err) {
                console.error(`Erro ao conectar ao banco de dados: ${err.message}`);
            } else {
                console.log('Conectado ao banco de dados SQLite');
                this.db.run(`
                    CREATE TABLE IF NOT EXISTS devStatus (
                        type INTEGER,
                        protocolo INTEGER,
                        utc DATETIME,
                        status INTEGER,
                        id TEXT
                    )
                `);
            }
        });
    }

    parseData(packet) {
        try {
            const cleanPacket = packet.replace(/[><]/g, '');
            const parts = cleanPacket.split(',');

            const typeVal = parseInt(parts[0].replace("DATA", ""));
            const protocoloVal = parseInt(parts[1]);
            const utcVal = DateTime.fromFormat(parts[2], 'yyMMddHHmmss').toFormat('yyyy-MM-dd HH:mm:ss');
            const statusVal = parseInt(parts[3].split(';')[0]);
            const idVal = parts[3].split('=')[1];

            const parsedData = {
                type: typeVal,
                protocolo: protocoloVal,
                utc: utcVal,
                status: statusVal,
                id: idVal
            };

            return parsedData;
        } catch (e) {
            console.error(`Erro ao analisar o pacote: ${e}`);
            return null;
        }
    }

    storeDataInDatabase(parsedData) {
        const { type, protocolo, utc, status, id } = parsedData;
        this.db.run(`
            INSERT INTO devStatus (type, protocolo, utc, status, id)
            VALUES (?, ?, ?, ?, ?)
        `, [type, protocolo, utc, status, id], (err) => {
            if (err) {
                console.error(`Erro ao armazenar dados no banco de dados: ${err.message}`);
            }
        });
    }

    storeDataInJson(parsedData) {
        try {
            const filePath = 'json/parsedData.json';
            let existingJson = [];

            if (fs.existsSync(filePath)) {
                existingJson = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
            }

            existingJson.push(parsedData);

            fs.writeFileSync(filePath, JSON.stringify(existingJson, null, 4));
        } catch (e) {
            console.error(`Erro ao armazenar dados no arquivo JSON: ${e}`);
        }
    }

    closeConnections() {
        this.serverSocket.close();
        this.db.close((err) => {
            if (err) {
                console.error(`Erro ao fechar conexão com o banco de dados: ${err.message}`);
            } else {
                console.log('Conexões fechadas.');
            }
        });
    }
}

const udpIp = '127.0.0.1';
const udpPort = 12345;

const udpServer = new UDPServer(udpIp, udpPort);

process.on('SIGINT', () => {
    console.log('O servidor foi encerrado');
    udpServer.closeConnections();
    process.exit();
});