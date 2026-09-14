import asyncio
import os
import sys
from contextlib import asynccontextmanager

# Garante que este diretório (back/) esteja no sys.path, para que os imports
# abaixo (banco, coletor, graphql_api, websocket) funcionem não importa de
# onde o programa seja iniciado (ex.: `uvicorn main:app` dentro de back/,
# ou `uvicorn back.main:app` a partir da raiz do projeto).
DIRETORIO_BACK = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_BACK not in sys.path:
    sys.path.insert(0, DIRETORIO_BACK)

# Diretório do front, calculado de forma absoluta (não depende do
# diretório de onde o comando é executado).
DIRETORIO_FRONT = os.path.join(os.path.dirname(DIRETORIO_BACK), "front")

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from banco import criar_banco
from coletor import coletar_metrica
from graphql_api import schema
from websocket import conectar_cliente, desconectar_cliente, enviar_metrica

from strawberry.fastapi import GraphQLRouter


async def coletor_automatico():

    while True:

        # coletar_metrica() faz chamadas bloqueantes (psutil.cpu_percent
        # com interval=1, além de I/O de banco). Rodar em thread separada
        # evita travar o loop de eventos do asyncio, o que travaria
        # temporariamente todas as conexões WebSocket e requisições
        # GraphQL a cada coleta.
        metrica = await asyncio.to_thread(coletar_metrica)

        await enviar_metrica(metrica)

        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):

    criar_banco()

    tarefa = asyncio.create_task(coletor_automatico())

    yield

    tarefa.cancel()


app = FastAPI(lifespan=lifespan)


graphql_app = GraphQLRouter(schema)

app.include_router(
    graphql_app,
    prefix="/graphql"
)


app.mount(
    "/static",
    StaticFiles(directory=DIRETORIO_FRONT),
    name="static"
)


@app.get("/")
def pagina_inicial():

    return FileResponse(
        os.path.join(DIRETORIO_FRONT, "index.html")
    )


@app.websocket("/ws")
async def websocket(websocket: WebSocket):

    await conectar_cliente(websocket)

    try:

        while True:

            await asyncio.sleep(60)

    except Exception:

        desconectar_cliente(websocket)
