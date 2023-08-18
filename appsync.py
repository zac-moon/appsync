import tkinter as tk

root= tk.Tk()
root.title('AppSync')
root.geometry('800x600')


def bank():
    print('Bank')


mainTitle = tk.Label(root, text="App Sync")
zbankButton = tk.Button(root,text="ZBANK LINK ", height=60,width=120)

mainTitle.grid(row=0,column=0,rowspan=3)

root.mainloop()