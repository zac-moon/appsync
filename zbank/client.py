import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('192.168.1.71', 12345)
client_socket.connect(server_address)
login = False

try:
    while True:
        for i in range(1, 64):
            print('')
        print('\n\nZBANK LINK LOGIN')
        print("Enter Details to login: ")
        username = input("Enter Username (or 'exit' to quit): ").strip()
        if username == "exit":
            break
        password = input('Enter Password: ').strip()
        client_socket.send(f'login.{username}.{password}'.encode('utf-8'))
        resp = client_socket.recv(1024).decode('utf-8')
        if resp == "1":
            print("Correct Details - Logged In\n\n")
            print('ENTER 0 TO LOGOUT \nENTER 1 FOR BALANCE \nENTER 2 FOR TRANSFER')
            login = True
            while login:
                mode = input('Enter code: ')
                if mode == '0':
                    login = False
                    client_socket.send(f'logout.{username}'.encode('utf-8'))
                    break
                elif mode == '1':
                    client_socket.send(f'balance.{username}'.encode('utf-8'))
                    bal = client_socket.recv(1024).decode('utf-8')
                    print(f'Balance: {bal}')
                elif mode == '2':
                    amount = input('Enter amount to transfer (0 to exit): ').strip()
                    to = input('Enter account username to transfer to (0 to cancel): ').strip()
                    client_socket.send(f'transfer.{username}.{amount}.{to}'.encode('utf-8'))
                    conf = client_socket.recv(1024).decode('utf-8')
                    print(conf)
        elif resp == '0':
            print('Account Not Found - Please Sign Up Instead')
        else:
            print("Incorrect Details. Please try again.")
finally:
    client_socket.close()