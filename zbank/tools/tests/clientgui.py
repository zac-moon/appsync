import tkinter as tk
import socket

root = tk.Tk()
root.title('ZBANK LINK - LOGIN')
root.geometry('800x600')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.71', 12345)
client_socket.connect(server_address)

def main(username):
    def balance(type):
        if type == 'upd':
            client_socket.send(f'balance.{username}.upd'.encode('utf-8'))
        else:
            client_socket.send(f'balance.{username}'.encode('utf-8'))
            
        balance = client_socket.recv(1024).decode('utf-8')
        return balance

    def transfer():
        print('transfer')
        transferwin = tk.Toplevel(client)
        transferwin.title("ZBANK LINK- TRANSFER")
        transferwin.geometry('400x400')

        traTitle = tk.Label(transferwin, text='Transfer Money')
        toLabel = tk.Label(transferwin, text='Enter Account Username to transfer to: ')
        toEntry = tk.Entry(transferwin)
        amountLabel = tk.Label(transferwin, text='Amount to transfer :')
        amountEntry = tk.Entry(transferwin) 

        def trTransfer():
            print('transfer')
            to = toEntry.get()
            amount = amountEntry.get()

            client_socket.send(f'transfer.{username}.{amount}.{to}'.encode('utf-8'))
            conf = client_socket.recv(1024)
            conf = conf.decode('utf-8')
            print(conf)
            if conf == "Transfer Successful":
                confLabel.config(text="Transfer Successful")
                transferwin.destroy() 
            elif conf == "To Account Not Found":
                confLabel.config(text='To Account Not Found')
            else:
                confLabel.config(text='An Error Occured- That\'s all We Know. :(')

        confLabel = tk.Label(transferwin, text="")
        transferbutton = tk.Button(transferwin, text="Transfer Funds", command=trTransfer)  # Changed transferbuttton to transferbutton
        
        traTitle.pack()
        toLabel.pack()
        toEntry.pack()
        amountLabel.pack()
        amountEntry.pack()  
        transferbutton.pack()  

    def update_balance():
        balance_label.config(text=f"BALANCE : £{balance('upd')}")
        client.after(200, update_balance)
        print('bal')

    client = tk.Toplevel(root)
    client.title(f'ZBANK LINK - {username}')
    client.geometry('800x600')

    client_title = tk.Label(client, text=f"ZBANK LINK - {username}")
    balance_label = tk.Label(client, text=f"BALANCE : £{balance('start')}", font=('Arial', 90))
    transfer_btn = tk.Button(client, text="TRANSFER", command=transfer)

    client_title.pack()
    balance_label.pack()
    transfer_btn.pack()

    balance('start')
    update_balance()

def login():
    username = username_entry.get()
    password = password_entry.get()
    client_socket.send(f'login.{username}.{password}'.encode('utf-8'))
    resp = client_socket.recv(1024).decode('utf-8')
    if resp == "1":
        print('Correct Details')
        main(username)
    elif resp == "0":
        print('Account Not Found')
    else:
        print('Password Incorrect')

main_title = tk.Label(root, text="ZBANK LINK - LOGIN", font=('Arial', 40))
username_label = tk.Label(root, text='Username:')
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")
login_btn = tk.Button(root, text="Login", command=login)

main_title.pack()
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
login_btn.pack()
root.mainloop()

client_socket.close()