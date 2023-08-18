import socket
import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (socket.gethostname(), 12345)
server_socket.bind(server_address)
server_socket.listen(1)

print('Server is listening on', server_address)

while True:
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%H:%M %d.%m.%Y')
    print(f'{formatted_datetime} | (                     ) | Waiting for a connection...')
    client_socket, client_address = server_socket.accept()

    try:
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%H:%M %d.%m.%Y')
        print(f"{formatted_datetime} | {client_address} | Connected")
        while True:
            data = client_socket.recv(1024)
            if data:
                data = data.decode('utf-8')
                datas = data.split('.')
                cmd = datas[0]

                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime('%H:%M %d.%m.%Y')
                try:
                    if datas[2]=="upd":
                        pass
                    else:
                        print(f'{formatted_datetime} | {client_address} | {data}')
                except IndexError:
                    print(f'{formatted_datetime} | {client_address} | {data}')


                if cmd == 'login':
                    username = datas[1]
                    password = datas[2]
                    fpath = f"db/users/{username}.txt"
                    try:
                        with open(fpath) as file:
                            corpass = file.read().strip()
                        if corpass == password:
                            client_socket.send('1'.encode('utf-8'))
                        else:
                            client_socket.send('2'.encode('utf-8'))
                    except FileNotFoundError:
                        client_socket.send('0'.encode('utf-8'))

                elif cmd == "balance":
                    username = datas[1]
                    fpath = f'db/balance/{username}.txt'
                    with open(fpath) as file:
                        bala = file.read().strip()
                    client_socket.send(bala.encode('utf-8'))

                elif cmd == "transfer":
                    froms = datas[1]
                    amount = datas[2]
                    amount = int(amount)
                    to = datas[3]
                    frompath = f'db/balance/{froms}.txt'
                    topath = f'db/balance/{to}.txt'

                    try:
                        with open(frompath) as file:
                            curin = file.read().strip()
                        curin = int(curin)
                        newbal = curin - amount
                        newbal = str(newbal)
                        with open(frompath, 'w') as file:
                            file.write(newbal)
                    except FileNotFoundError:
                        client_socket.send('From Account Not Found'.encode('utf-8'))

                    try:
                        with open(topath) as file:
                            curin = file.read().strip()
                        curin = int(curin)
                        newbal = curin + amount
                        newbal = str(newbal)
                        with open(topath, 'w') as file:
                            file.write(newbal)
                    except FileNotFoundError:
                        with open(frompath) as file:
                            curin = file.read().strip()
                        curin = int(curin)
                        newbal = curin + amount
                        newbal = str(newbal)
                        with open(frompath, 'w') as file:
                            file.write(newbal)
                        client_socket.send('To Account Not Found'.encode('utf-8'))

                    client_socket.send('Transfer Successful'.encode('utf-8'))
            else:
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime('%H:%M %d.%m.%Y')
                print(f"{formatted_datetime} | {client_address} | Disconnected")
                break
    finally:
        client_socket.close()