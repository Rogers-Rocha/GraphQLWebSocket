import asyncio

from fastapi import WebSocket

# O websocket vai gerenciar apenas os clientes. Assim, se tiver 2 clientes, cada cliente nao vai criar seu proprio coletor

clientes = []


async def enviar_metrica(metrica):

    clientes_copia = clientes.copy()

    for cliente in clientes_copia:

        try:
            await cliente.send_json(metrica)

        except Exception:

            if cliente in clientes:
                clientes.remove(cliente)


async def conectar_cliente(websocket: WebSocket):

    await websocket.accept()

    clientes.append(websocket)


def desconectar_cliente(websocket: WebSocket):

    if websocket in clientes:
        clientes.remove(websocket)