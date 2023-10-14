import requests
import argparse
from base64 import b64encode
import time
from colorama import init, Fore

init(autoreset=True)

def authenticate(username, token):
    HEADERS = {"Authorization": "Basic " + b64encode(f"{username}:{token}".encode('utf-8')).decode('utf-8')}
    res = requests.get("https://api.github.com/user", headers=HEADERS)
    if res.status_code != 200:
        print(Fore.RED + "Falha na autenticação! Verifique o Personal Access Token e o nome de usuário.")
        exit(1)
    else:
        print(Fore.GREEN + "Autenticação bem-sucedida!")
    return HEADERS

def get_random_users(username, token, num_users=10):
    HEADERS = authenticate(username, token)
    sesh = requests.session()
    sesh.headers.update(HEADERS)
    last_page = 1

    try:
        with open("last_page.txt", "r") as f:
            last_page = int(f.read())
    except FileNotFoundError:
        pass

    new_users = []

    fn = open("word-list.txt", "a")

    print(Fore.GREEN + "Gerando usuários aleatórios...")

    for i in range(last_page, last_page + num_users):
        res = sesh.get(f"https://api.github.com/users?since={i}").json()
        for user in res:
            new_users.append(user['login'])
            print(Fore.CYAN + f"~# Gerando usuário: {user['login']}")
            fn.write(user['login'] + "\n")

    f = open("last_page.txt", "w+")
    f.write(str(last_page + num_users))
    f.close()
    fn.close()

    return new_users

def follow_users(username, token):
    HEADERS = authenticate(username, token)
    sesh = requests.session()
    sesh.headers.update(HEADERS)

    with open("word-list.txt", "r") as file_in:
        new_users = [line.strip() for line in file_in]

    print(Fore.GREEN + "Iniciando a seguir os usuários gerados...")

    for user in new_users:
        time.sleep(2)
        res = sesh.put(f"https://api.github.com/user/following/{user}")
        if res.status_code != 204:
            print(Fore.RED + f"~# {user} Usuário inexistente.")
        else:
            print(Fore.GREEN + f"~# {user} Seguido com sucesso")

if __name__ == "__main__":
    username = input("Insira seu nome de usuário do GitHub: ")
    token = input("Insira seu Personal Access Token do GitHub: ")
    num_users = int(input("Quantos usuários você deseja gerar na word-list.txt? "))

    new_users = get_random_users(username, token, num_users)
    follow_users(username, token)
