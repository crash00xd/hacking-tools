#!/bin/bash

# Verifica se o endereço IP do alvo foi fornecido  
if [ -z "$1" ]; then  
    echo "Uso: ./port_scan.sh <endereco_ip>"  
    exit 1  
fi

# Verifica se o nmap está instalado  
if ! command -v nmap &> /dev/null; then  
    echo "O nmap não está instalado. Instalando o nmap..."  
    sudo apt update  
    sudo apt install nmap -y

    # Verifica se a instalação foi bem-sucedida  
    if [ $? -ne 0 ]; then  
        echo "ERRO AO INSTALAR O NMAP" >&2  
        exit 1  
    fi  
fi

# Inicia a varredura de portas  
echo "Escaneando todas as portas..."

nmap -p- -T4 -Pn "$1"

# -p-: escaneia todas as portas  
# -T4: nível de intensidade razoável  
# -Pn: ignora a descoberta de hosts
# exit 1: posso usar ele pra tratar de erros diversos e fechar a execucao do programa
# $?: variavel que contem a saida do comando anterior
# -ne: condicao "nao igual"
# >&2: exibe a mensagem de erro no canal padrao (no caso, a tela)
