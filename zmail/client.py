import socket

def main():
    host = 'localhost'
    port = 12346

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        while True:
            message = input("Enter a message: ")
            client.send(message.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(response)
    except KeyboardInterrupt:
        print("Client closing.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
