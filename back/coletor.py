import psutil
from datetime import datetime

from banco import salvar_metrica


def coletar_metrica():
    cpu = psutil.cpu_percent(interval=1) # pega a porcentagem do CPU

    ram = psutil.virtual_memory().percent # pega a porcentagem da RAM

    disco = psutil.disk_usage("/").percent # pega a porcentagem do Disco

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Então o python transfoma tudo em informações com JSON
    metrica = {
        "horario": horario,
        "cpu": cpu,
        "ram": ram,
        "disco": disco
    }

    salvar_metrica(
        horario,
        cpu,
        ram,
        disco
    )

    return metrica