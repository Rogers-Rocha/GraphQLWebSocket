const cpu = document.getElementById("cpu");
const ram = document.getElementById("ram");
const disco = document.getElementById("disco");

const horario = document.getElementById("horario");
const status = document.getElementById("status");

const resultado = document.getElementById("resultado");


const protocolo = window.location.protocol === "https:"
    ? "wss"
    : "ws";


const websocket = new WebSocket(
    `${protocolo}://${window.location.host}/ws`
);


websocket.onopen = function () {

    status.textContent =
        "WebSocket conectado";

};


websocket.onmessage = function (evento) {

    const dados = JSON.parse(evento.data);


    cpu.textContent =
        `${dados.cpu.toFixed(1)} %`;


    ram.textContent =
        `${dados.ram.toFixed(1)} %`;


    disco.textContent =
        `${dados.disco.toFixed(1)} %`;


    horario.textContent =
        `Última atualização: ${dados.horario}`;

};


websocket.onerror = function () {

    status.textContent =
        "Erro na conexão WebSocket";

};


websocket.onclose = function () {

    status.textContent =
        "WebSocket desconectado";

};


async function consultarMediaCpu() {

    const consulta = `
        query {
            mediaCpu(segundos: 30)
        }
    `;


    const resposta = await fetch(
        "/graphql",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: consulta
            })
        }
    );


    const dados = await resposta.json();


    resultado.textContent =
        `Média da CPU: ${dados.data.mediaCpu}%`;

}


async function consultarMediaDisco() {

    const consulta = `
        query {
            mediaDisco(segundos: 30)
        }
    `;


    const resposta = await fetch(
        "/graphql",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: consulta
            })
        }
    );


    const dados = await resposta.json();


    resultado.textContent =
        `Média do Disco: ${dados.data.mediaDisco}%`;

}


async function consultarEstatisticasCpu() {

    const consulta = `
        query {
            estatisticasCpu(segundos: 60) {
                media
                maximo
                minimo
                amostras
            }
        }
    `;


    const resposta = await fetch(
        "/graphql",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: consulta
            })
        }
    );


    const dados = await resposta.json();

    const estatisticas = dados.data.estatisticasCpu;


    resultado.textContent =
        `CPU (últimos 60s) - média: ${estatisticas.media}% | máx: ${estatisticas.maximo}% | mín: ${estatisticas.minimo}% | amostras: ${estatisticas.amostras}`;

}