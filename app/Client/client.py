import threading
import socket

HOST = 'localhost'
PORT = 80

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))

    except:
        return print('\n Falha na conexão! \n')

    userName = input('Nome do cliente: ')
    client.send(userName.encode('utf-8'))

    print('\n  -> CONECTADO!!')

    thread1 = threading.Thread(target=receiveMessage, args=[client])
    thread2 = threading.Thread(target=sendMessage, args=[client, userName])

    thread1.start()
    thread2.start()

def receiveMessage(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg + '\n')
        except:
            print('\n Não foi possível permanecer conectado ao servidor! \n')
            print('Pressione <Enter> para continuar... \n')
            client.close()
            break

def sendMessage(client, userName):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{userName}> {msg}'.encode('utf-8'))
        except:
            return

main()
