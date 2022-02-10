import subprocess
import tkinter as tk
from tkinter import  PhotoImage


class Wi_Fi():
    def __init__(self) -> None:
        self.root  = tk.Tk()
        self.root.title("Leo")
        self.root.geometry("800x500")
        self.root.resizable(False,False)
        self.bg = PhotoImage(file='Click.png')
        self.canvas1 = tk.Canvas(self.root)
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_image( 0, 0, image = self.bg, anchor = "nw")
        self.canvas1.create_text( 200, 100, text = "I remember all your Wi-Fi passwords !",font="UTF-8")
        self.lb = tk.Listbox(self.canvas1,width=40,height=25)
        

        self.button1 = tk.Button(background='yellow',
                                 text='Finde Wi-Fi',
                                 anchor='nw',
                                 command=self.f)


        self.button2 = tk.Button(width=10,
                                 text='Quit',
                                 background='red',
                                 command=self.root.destroy)

        self.button1 = self.canvas1.create_window(0, 0, 
                                       anchor = "nw",
                                       window = self.button1)

        self.button2 = self.canvas1.create_window(720, 0, 
                                       anchor = "nw",
                                       window = self.button2)

        self.lb.grid(padx=10,pady=150)

    def find_wi_fi(self):
        data_lst = {}
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    data_lst[i] = results[0]
                except IndexError:
                    print ("{:<30}|  {:<}".format(i, ""))
            except subprocess.CalledProcessError:
                print ("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
        
        return data_lst        

    def f(self):
        value = 1
        res = self.find_wi_fi()
        for k,v in res.items():
            self.lb.insert(value, f"{k} --| {v}")
            value = value + 1


if __name__ == "__main__":
    run = Wi_Fi()
    tk.mainloop()