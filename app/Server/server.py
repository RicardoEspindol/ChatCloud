import threading
import socket
import os

clients = []
HOST = ''
PORT = 80
DATA_DIR = "data"  # Pasta para armazenar os arquivos de dados

def main():
    setup_data_dir()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        server.listen()

    except:
        print('\n Não foi possível iniciar o servidor! \n')
        return

    while True:
        client, addr = server.accept()
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def setup_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def messagesTreatment(client):
    userName = client.recv(1024).decode('utf-8')
    user_data_file = os.path.join(DATA_DIR, f"{userName}.txt")

    # Carrega o histórico de mensagens do arquivo
    send_history(client, user_data_file)

    while True:
        try:
            msg = client.recv(2048)
            if not msg:
                break

            save_message(userName, msg.decode('utf-8'), user_data_file)
            broadcast(msg, client)

        except:
            deleteClient(client)
            break

def save_message(userName, msg, file_path):
    with open(file_path, 'a') as file:
        file.write(f'<{userName}> {msg}\n')

def send_history(client, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            history = file.read()
            client.send(history.encode('utf-8'))

def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)

def deleteClient(client):
    clients.remove(client)

main()
