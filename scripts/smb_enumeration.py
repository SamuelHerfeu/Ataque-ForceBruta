#!/usr/bin/env python3

import subprocess
import sys
import os

def enumerate_smb(target_ip):
    """
    Script para enumeração SMB educacional
    """
    print(f"[+] Iniciando enumeração SMB para {target_ip}")
    
    # Enumeração básica com enum4linux
    try:
        print(f"[+] Executando enum4linux...")
        result = subprocess.run(['enum4linux', target_ip], 
                              capture_output=True, text=True, timeout=300)
        print(result.stdout)
        
        # Salvar resultados
        with open(f'results/smb_enum_{target_ip}.txt', 'w') as f:
            f.write(result.stdout)
            
    except subprocess.TimeoutExpired:
        print("[-] Enumeração expirou")
    except Exception as e:
        print(f"[-] Erro na enumeração: {e}")

def test_smb_access(target_ip, username, password):
    """
    Testar acesso SMB com credenciais
    """
    print(f"[+] Testando acesso SMB com {username}:{password}")
    
    try:
        # Listar compartilhamentos
        cmd = f'smbclient -L //{target_ip} -U {username}%{password}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if "NT_STATUS_ACCESS_DENIED" not in result.stderr:
            print(f"[+] Acesso bem-sucedido!")
            print(result.stdout)
            return True
        else:
            print("[-] Acesso negado")
            return False
            
    except Exception as e:
        print(f"[-] Erro: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 smb_enumeration.py <target_ip>")
        sys.exit(1)
    
    target = sys.argv[1]
    enumerate_smb(target)
