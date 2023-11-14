import socket
from unittest.mock import Mock, patch
import pytest
from simulator import sendDataToServer, simulator, closeSimulator
from unittest.mock import patch

@pytest.fixture
def mock_socket():
    return Mock(spec=socket.socket)

def test_sendDataToServer(mock_socket):
    udpIp = "127.0.0.1"
    udpPort = 12345

    with patch("simulator.generateRandomData", return_value=(1, 66, "210101010101", 0, "ABC")):
        sendDataToServer(mock_socket, udpIp, udpPort)

    # Verifique se o método sendto foi chamado com os argumentos corretos
    mock_socket.sendto.assert_called_once_with(b">DATA1,66,210101010101,0;ID=ABC<", (udpIp, udpPort))

def test_closeSimulator(mock_socket):
    closeSimulator(mock_socket)
    # Verifique se o método close foi chamado
    mock_socket.close.assert_called_once()

def test_simulator_with_exception(mock_socket):
    udpIp = "127.0.0.1"
    udpPort = 12345

    # Simule uma exceção durante o envio de dados
    with patch("simulator.sendDataToServer", side_effect=Exception("Test exception")):
        with pytest.raises(Exception, match="Test exception"):
            simulator(udpIp, udpPort)
