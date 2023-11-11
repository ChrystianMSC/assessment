# assessment
[![My Skills](https://skillicons.dev/icons?i=py,nodejs)](https://skillicons.dev)

O projeto foi realizado em duas linguagens diferentes, Python e Node.js Cada um dentro de suas respectivas pastas.

Utilizando o pytest foram escritos testes, tanto para o simulador quanto o servidor em python.

- Primeiramente clone este repositório.

```
git clone https://github.com/ChrystianMSC/assessment
cd assessment
```

- Certifique-se de ter o sqlite instalado

```
sudo apt-get install sqlite3
```
No windows instalar o python já vem como o sqlite

Instruções mais especificas de execução serão dadas a seguir.

## Execução

### Node.js

Para executar o simulador e o servidor em Node.js o seguinte deve ser feito:

- Certifique-se de ter o Node.js instalado https://nodejs.org/en/

- Com o repositório abeto na raiz do projeto navegue para a pasta *node*

```
cd node
```

- Execute o comando *npm* para instalar as dependencias necessárias.

``` 
npm install 
```

- Quando todas dependencias forem instaladas, em um terminal execute o servidor.

```
node server.js
```

Se algum erro ocorre na hora de executar o servidor, provavelmente será problama de dependencia, apague o arquivo package-lock.json e execute novamente o comando.

- Agora em outro terminal execute o simulador

```
node simulator.js
```

Agora acompanhe os envios de dados do simulador para o servidor, eles começaram a ser enviados depois de 5 segundos.


## Ctrl + C para finalizar o servidor e/ou o simulador

---



### Python

- Com o repositório abeto na raiz do projeto navegue para a pasta *python*

```
cd python
```

- Com o sqlite instalado só precisamos instalar a biblioteca pytest para que os testes possam ser executado

```
pip install pytest
```

Algumas vezes no linux o python deve ser executado com python3.
Alem disso para instalar o pytest no linux o seguinte deve ser feito:

```
sudo apt install python3-pytest
```

E ele deveser executado com ```pytest-3```

- Agora execute tanto o servidor quando o simulador (em terminais diferentes) da seguinte forma:

```
python server.py
```
```
python simulator.py
```

Agora acompanhe os envios de dados do simulador para o servidor.

### Testes

Para executar os testes, no diretorio do projeto python execute os seguintes comandos:
```
pytest testServer.py
```
```
pytest testSimulator.py
```


## Ctrl + C para finalizar o servidor e/ou o simulador
---
