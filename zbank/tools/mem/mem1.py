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
    if amount == '':
        amount = '0'
    elif not all(char.isdigit() for char in amount):
        amount = '0'

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