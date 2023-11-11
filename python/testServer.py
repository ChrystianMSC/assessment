import pytest
import os
import socket
from datetime import datetime
import sqlite3
from server import UDPServer
import json
import time

# Fixture para criar uma instância temporária da classe UDPServer para testes
@pytest.fixture
def udp_server_instance():
    udp_server = UDPServer("127.0.0.1", 12345)
    yield udp_server
    udp_server.closeConnections()  # Certifique-se de encerrar o servidor após cada teste

# Testa a inicialização correta do UDPServer
def test_udp_server_initialization(udp_server_instance):
    assert isinstance(udp_server_instance, UDPServer)

# Testa a inicialização correta do banco de dados
def test_database_initialization(udp_server_instance):
    udp_server_instance.initializeDatabase()

    # Verifica se a tabela 'devStatus' existe no banco de dados
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='devStatus';")
        result = cursor.fetchone()
        assert result is not None

# Testa se os dados são analisados corretamente
def test_data_parsing():
    udp_server = UDPServer("127.0.0.1", 12345)
    packet = "<DATA1,2,210101123456,3;id=abc>"
    parsed_data = udp_server.parseData(packet)
    expected_data = {
        "type": 1,
        "protocolo": 2,
        "utc": "2021-01-01 12:34:56",
        "status": 3,
        "id": "abc"
    }
    assert parsed_data == expected_data

# Testa se os dados são armazenados corretamente no banco de dados
def test_store_data_in_database(udp_server_instance):
    parsed_data = {
        "type": 1,
        "protocolo": 2,
        "utc": "2021-01-01 12:34:56",
        "status": 3,
        "id": "abc"
    }
    udp_server_instance.storeDataInDatabase(parsed_data)

    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devStatus;")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == parsed_data["type"]
        assert result[1] == parsed_data["protocolo"]
        assert result[2] == parsed_data["utc"]
        assert result[3] == parsed_data["status"]
        assert result[4] == parsed_data["id"]

# Testa se os dados são armazenados corretamente no arquivo JSON
def test_store_data_in_json(udp_server_instance):
    parsed_data = {
        "type": 1,
        "protocolo": 2,
        "utc": "2021-01-01 12:34:56",
        "status": 3,
        "id": "abc"
    }
    udp_server_instance.storeDataInJson(parsed_data)

    with open('json/parsedData.json', 'r') as json_file:
        existing_json = json.load(json_file)
        if len(existing_json) == 1:
            assert existing_json[0] == parsed_data
        else:
            assert existing_json[len(existing_json) - 1] == parsed_data