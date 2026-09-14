import strawberry
import sqlite3

from banco import BANCO

# temos metricas para buscar o historico (ate 5 min, ver banco.py),
# mediaCpu(segundos) e mediaRam(segundos) para calcular medias,
# mediaDisco(segundos) para o disco, e estatisticasCpu(segundos) para
# media/maximo/minimo da CPU em um unico campo (evita ter que fazer
# 3 consultas separadas)

@strawberry.type
class Metrica:
    id: int
    horario: str
    cpu: float
    ram: float
    disco: float


@strawberry.type
class EstatisticasCpu:
    media: float
    maximo: float
    minimo: float
    amostras: int


def obter_metricas():
    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, horario, cpu, ram, disco
        FROM metricas
        ORDER BY id DESC
    """)

    resultados = cursor.fetchall()

    conexao.close()

    metricas = []

    for resultado in resultados:
        metrica = Metrica(
            id=resultado[0],
            horario=resultado[1],
            cpu=resultado[2],
            ram=resultado[3],
            disco=resultado[4]
        )

        metricas.append(metrica)

    return metricas


@strawberry.type
class Query:

    @strawberry.field
    def metricas(self) -> list[Metrica]:
        return obter_metricas()

    @strawberry.field
    def media_cpu(self, segundos: int) -> float:

        conexao = sqlite3.connect(BANCO)

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT AVG(cpu)
            FROM metricas
            WHERE datetime(horario) >= datetime('now','localtime', ?)
        """, (f"-{segundos} seconds",))

        resultado = cursor.fetchone()

        conexao.close()

        if resultado[0] is None:
            return 0

        return round(resultado[0], 2)

    @strawberry.field
    def media_ram(self, segundos: int) -> float:

        conexao = sqlite3.connect(BANCO)

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT AVG(ram)
            FROM metricas
            WHERE datetime(horario) >= datetime('now','localtime', ?)
        """, (f"-{segundos} seconds",))

        resultado = cursor.fetchone()

        conexao.close()

        if resultado[0] is None:
            return 0

        return round(resultado[0], 2)

    @strawberry.field
    def media_disco(self, segundos: int) -> float:

        conexao = sqlite3.connect(BANCO)

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT AVG(disco)
            FROM metricas
            WHERE datetime(horario) >= datetime('now','localtime', ?)
        """, (f"-{segundos} seconds",))

        resultado = cursor.fetchone()

        conexao.close()

        if resultado[0] is None:
            return 0

        return round(resultado[0], 2)

    @strawberry.field
    def estatisticas_cpu(self, segundos: int) -> EstatisticasCpu:

        conexao = sqlite3.connect(BANCO)

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT AVG(cpu), MAX(cpu), MIN(cpu), COUNT(*)
            FROM metricas
            WHERE datetime(horario) >= datetime('now','localtime', ?)
        """, (f"-{segundos} seconds",))

        resultado = cursor.fetchone()

        conexao.close()

        if resultado[3] == 0:
            return EstatisticasCpu(media=0, maximo=0, minimo=0, amostras=0)

        return EstatisticasCpu(
            media=round(resultado[0], 2),
            maximo=round(resultado[1], 2),
            minimo=round(resultado[2], 2),
            amostras=resultado[3]
        )


schema = strawberry.Schema(query=Query)