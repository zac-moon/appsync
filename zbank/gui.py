import tkinter as tk
import socket
from ttkthemes import ThemedStyle
from tkinter import font

root = tk.Tk()
root.title('ZBANK LINK - LOGIN')
root.geometry('800x600')

style = ThemedStyle(root)
style.set_theme("radiance")
francoisOne = font.Font(family="tools/Francois_One/FrancoisOne-Regular.ttf", size=12)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.71', 12345)
client_socket.connect(server_address)

def main(username):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
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

        traTitle = tk.Label(transferwin, text='Transfer Money', font=(francoisOne, 16))
        toLabel = tk.Label(transferwin, text='Enter Account Username to transfer to: ', font=(francoisOne, 16))
        toEntry = tk.Entry(transferwin, font=(francoisOne, 16))
        amountLabel = tk.Label(transferwin, text='Amount to transfer :', font=(francoisOne, 16))
        amountEntry = tk.Entry(transferwin, font=(francoisOne, 16)) 

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

        confLabel = tk.Label(transferwin, text="", font=(francoisOne, 16))
        transferbutton = tk.Button(transferwin, text="Transfer Funds", command=trTransfer, font=(francoisOne, 16)) 

        traTitle.pack()
        toLabel.pack()
        toEntry.pack()
        amountLabel.pack()
        amountEntry.pack()  
        transferbutton.pack()  
        confLabel.pack()
    
    def update_balance(rast):
        balance_label.config(text=f"£{balance('upd')}")
        client.after(200, update_balance, rast + 1)
        print('bal', rast)

    def logout():
        client_socket.send(f'logout.{username}'.encode('utf-8'))
        client.destroy()

    client = tk.Toplevel()
    client.title(f'ZBANK LINK - {username}')
    client.geometry('800x600')

    balance_label = tk.Label(client, text=f"£{balance('start')}", font=(francoisOne, 90))
    transfer_btn = tk.Button(client, text="Transfer", command=transfer, height=6,width=10, font=(francoisOne, 16))
    logout_btn = tk.Button(client, text="Log Out", command=logout,height=6,width=10, font=(francoisOne, 16))

    balance_label.pack()
    transfer_btn.pack()
    logout_btn.pack()

    balance('start')
    update_balance(0)

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


main_title = tk.Label(root, text="ZBANK LINK - LOGIN", font=(francoisOne,40))
username_label = tk.Label(root, text='Username:', font=(francoisOne, 16))
username_entry = tk.Entry(root, font=(francoisOne, 16))
password_label = tk.Label(root, text="Password:", font=(francoisOne, 16))
password_entry = tk.Entry(root, show="*", font=(francoisOne, 16))
login_btn = tk.Button(root, text="Login", command=login, font=(francoisOne, 16))

main_title.pack()
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
login_btn.pack()
root.mainloop()

client_socket.close()