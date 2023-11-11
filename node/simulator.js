const dgram = require('dgram');
const moment = require('moment');

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function generateRandomData() {
    const dataType = getRandomIntInclusive(1, 2);
    const protocol = getRandomIntInclusive(66, 68);
    const utcTime = moment().utc().format("YYMMDDHHmmss");
    const status = getRandomIntInclusive(0, 1);
    const identifier = Math.random().toString(16).substr(2, 3).toUpperCase();

    return { dataType, protocol, utcTime, status, identifier };
}

function sendDataToServer(socket, udpIp, udpPort) {
    const { dataType, protocol, utcTime, status, identifier } = generateRandomData();

    const packet = `>DATA${dataType},${protocol},${utcTime},${status};ID=${identifier}<`;
    console.log('\nEnviando dado:\n', packet);

    socket.send(Buffer.from(packet), udpPort, udpIp, (err) => {
        if (err) {
            console.error('Erro ao enviar o pacote:', err);
        }
    });
}

function simulator(udpIp, udpPort) {
    const clientSocket = dgram.createSocket('udp4');
    console.log('Simulador iniciado, dados serão enviados a cada 5 segundos. \nCtrl + C para encerrar o simulador');
    setTimeout(() => {
        const interval = setInterval(() => {
            sendDataToServer(clientSocket, udpIp, udpPort);
        }, 5000);

        process.on('SIGINT', () => {
            clearInterval(interval);
            console.log('Simulador interrompido.');
            clientSocket.close();
            process.exit();
        });
    }, 3000);
}

const udpIp = '127.0.0.1';
const udpPort = 12345;

simulator(udpIp, udpPort);
