# GraphQLWebSocket
Trabalho o qual utiliza GrapfQL para consulta de dados do histórico e WebSocket para receber os dados em tempo real.

# Para executar o programa, use os seguintes comandos dentro do terminal do PowerShell:

cd back
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt

# assim voce tem que estar assim no caminho: GraphQLWebSocket\back>

py -m uvicorn main:app --reload

# isso vai rodar os pacotes e te dar uma url como: http://127.0.0.1:8000
# copie a URL que aparecer e cole no navegador.
# dentro da pasta back, terá o arquivo metricas.db onde ele continuará a ganhar novas linhas a cada 5 segundos.
# Para interromper o servidor, pressione CTRL + C no terminal.
