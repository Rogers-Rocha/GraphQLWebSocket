import sqlite3

# será criada uma tabela chamada metricas com:
# id, horario, cpu, ram e disco. Por exemplo:
#   1 | 2026-09-13 18:30:00 | 32.5 | 61.2 | 45.1
#   2 | 2026-09-13 18:30:05 | 40.1 | 62.0 | 45.2
#   3 | 2026-09-13 18:30:10 | 37.8 | 62.4 | 45.2

BANCO = "metricas.db"


def criar_banco():
    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metricas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horario TEXT NOT NULL,
            cpu REAL NOT NULL,
            ram REAL NOT NULL,
            disco REAL NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_metrica(horario, cpu, ram, disco):
    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO metricas (horario, cpu, ram, disco)
        VALUES (?, ?, ?, ?)
    """, (horario, cpu, ram, disco))

    # Remove registros com mais de 5 minutos. Janela de retencao deliberada,
    # justificada na secao 2 do relatorio.txt: mantem o banco pequeno e
    # coerente com o uso do sistema como monitoramento "ao vivo", e ja da
    # ~60 amostras (coleta a cada 5s) para as consultas GraphQL de media/
    # maximo/minimo.
    cursor.execute("""
        DELETE FROM metricas
        WHERE datetime(horario) < datetime('now', 'localtime', '-5 minutes')
    """)

    # Com o servidor parado, use esse comando abaixo para:
    # apagar todas as linhas do banco, mas mantem a tabela
    # cursor.execute("DELETE FROM metricas")

    conexao.commit()
    conexao.close()


def buscar_metricas():
    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, horario, cpu, ram, disco
        FROM metricas
        ORDER BY id DESC
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados