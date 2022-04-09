import tkinter as tk
from tkinter import ttk
import ctypes
import fileinput
import sys
import validators
from tkinter import messagebox
import os
from tkinter.messagebox import showinfo
from PIL import ImageTk
import re



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))



def DeleteWhiteLines(fname):
    with open(fname, 'r+') as fd:
        lines = fd.readlines()
        fd.seek(0)
        fd.writelines(line for line in lines if line.strip())
        fd.truncate()

def getWebsites():
    websites = []
    # Using readlines()
    file1 = open(host_path, 'r')
    Lines = file1.readlines()
    
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        if line.startswith('127.0.0.1'):
            line = line.replace('127.0.0.1', "").replace(" ", "").rstrip()
            websites.append(line)
    return websites

def addToBlockedWebsites():
    website_address = e1.get()

    with open (host_path , 'r+') as host_file:
        file_content = host_file.read()
        if (not validators.url(website_address)) and (not is_valid_ip(website_address)):
            label = tk.Label(advancedWindow, text = website_address + ' is not valid.' , font = 'Lato 12 bold')
            label.place(x=280, y=170)
            label.after(1000, label.destroy)
        
        if file_content.find(website_address) != -1:
            label = tk.Label(advancedWindow, text = 'Already Blocked' , font = 'Lato 12 bold', fg="red", bg="#132824")
            label.place(x=280, y=170)
            label.after(1000, label.destroy)
            e1.delete(0, tk.END)

        if validators.url(website_address) or is_valid_ip(website_address) and website_address not in file_content :
            host_file.seek(0)
            data = host_file.read(100)
            if len(data) > 0 :
                host_file.write("\n")
            
            host_file.write(ip_address + " " + website_address.strip())
            
            label = tk.Label(advancedWindow, text = "Blocked", font = 'Lato 12 bold', fg="red", bg="#132824")
            label.place(x=310, y=170)
            label.after(1000, label.destroy)
            tree.insert('', tk.END, values=website_address)
            e1.delete(0, tk.END)
    DeleteWhiteLines(host_path)

def addToUnblockedWebsites():
    website_address = tree.item(tree.selection())['values'][0]
    global treeWebsites

    def replacement(file, previousw, nextw):
        global treeWebsites
        with fileinput.input(file, inplace=True) as file:
            for line in file:
                if(website_address == line):
                    selected_item = tree.selection()[0]
                    tree.delete(selected_item)
                label = tk.Label(advancedWindow, text = "Unblocked", font = 'Lato 12 bold',fg="green", bg="#132824")
                label.place(x=310, y=170)
                label.after(1000, label.destroy)
                new_line = line.replace(previousw, nextw)
                print(new_line, end='')
        treeWebsites = getWebsites()
        for i in tree.get_children():
           tree.delete(i)
        for website in treeWebsites:
            tree.insert('', tk.END, values=website) 
        fileinput.close()

    with open (host_path , 'r+') as host_file:
        file_content = host_file.read()
    for website in sorted(website_address):
        
        if not website in file_content:
            label = tk.Label(advancedWindow, text = 'Already Unblocked' , font = 'Lato 12 bold', fg="green", bg="#132824")
            label.place(x=250, y=200)
            label.after(1000, label.destroy)


    
    replacement(host_path, "127.0.0.1 " + website_address, "")  
            


def GetValue(event):
    e1.delete(0, tk.END)
    row_id = tree.selection()[0]
    select = tree.set(row_id)
    e1.insert(0,select['website_ip'])


def UnBlocker():

        unwebsite_lists = UnWebsites.get(1.0,tk.END).strip().replace(" ", "")
        UnWebsite = set(unwebsite_lists.split(","))

        def replacement(file, previousw, nextw):
            with fileinput.input(file, inplace=True) as file:
                for line in file:
                    new_line = line.replace(previousw, nextw)
                    print(new_line, end='')
            fileinput.close()


        with open (host_path , 'r+') as host_file:
            file_content = host_file.read()
        for website in sorted(UnWebsite):
            
            if not website in file_content:
                label = tk.Label(root, text = 'Already Unblocked' , font = 'Lato 12 bold', fg="green", bg="#132824")
                label.place(x=250, y=200)
                label.after(1000, label.destroy)
                unwebsite_lists = UnWebsites.delete('1.0', tk.END)
                pass
            else:
                label = tk.Label(root, text = "Unblocked", font = 'Lato 12 bold',fg="green", bg="#132824")
                label.place(x=250, y=200)
                label.after(1000, label.destroy)
                replacement(host_path, "127.0.0.1 " + website, "")  
                unwebsite_lists = UnWebsites.delete('1.0', tk.END)


def Blocker():
        tk.Label(root, text="")
        website_lists = Websites.get(1.0,tk.END).strip().replace(" ", "").replace(";", ",")
        Website = set(website_lists.split(","))
        DeleteWhiteLines(host_path)
        with open (host_path , 'r+') as host_file:
            file_content = host_file.read()
            
            for website in sorted(Website):
                if (not validators.url(website)) and (not is_valid_ip(website)):
                    label = tk.Label(root, text = website + ' is not valid.' , font = 'Lato 12 bold')
                    label.place(x=250, y=200)
                    label.after(1000, label.destroy)
                    break
                
                if website in file_content:
                    label = tk.Label(root, text = 'Already Blocked' , font = 'Lato 12 bold', fg="red", bg="#132824")
                    label.place(x=250, y=200)
                    label.after(1000, label.destroy)
                    website_lists = Websites.delete('1.0', tk.END)
                    pass
                if validators.url(website) or is_valid_ip(website) and website not in file_content :
                    host_file.seek(0)
                    data = host_file.read(100)
                    if len(data) > 0 :
                        host_file.write("\n")
                    
                    host_file.write(ip_address + " " + website.strip())
                    
                    label = tk.Label(root, text = "Blocked", font = 'Lato 12 bold', fg="red", bg="#132824")
                    label.place(x=250, y=200)
                    label.after(1000, label.destroy)
                    website_lists = Websites.delete('1.0', tk.END)
        DeleteWhiteLines(host_path)

def Restore():
    label = tk.Label(root, text = "Restored✔", font = 'Lato 12 bold', fg="dodgerblue")
    label.place(x=250, y=200)
    label.after(1000, label.destroy)
    with open (host_path , 'r+') as host_file:
        host_file.seek(0)                        
        host_file.truncate()
        host_file.write(
            "# Copyright (c) 1993-2006 Microsoft Corp.\n"+
            "#\n"+
            "# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.\n"+
            "#\n"+
            "# This file contains the mappings of IP addresses to host names. Each\n"+
            "# entry should be kept on an individual line. The IP address should\n"+
            "# be placed in the first column followed by the corresponding host name.\n" +
            "# The IP address and the host name should be separated by at least one # space.\n"+
            "# space.\n"+
            "#\n"+
            "# Additionally, comments (such as these) may be inserted on individual\n"+
            "# lines or following the machine name denoted by a '#' symbol.\n"+
            "#\n"+
            "# For example:\n"+
            "#\n"+
            "#      102.54.94.97     rhino.acme.com          # source server\n"+
            "#       38.25.63.10     x.acme.com              # x client host\n"+
            "# localhost name resolution is handle within DNS itself.\n"+
            "#       127.0.0.1       localhost\n"+
            "#       ::1             localhost")

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class Error(tk.Toplevel):
    def __init__(self, message, window):
        tk.Toplevel.__init__(self)
        tk.Label(self, text=message).grid(row=0, column=0)
        x = window.winfo_x()
        y = window.winfo_y()
        self.geometry("+%d+%d" % (x + 200, y + 100))
        
        tk.Button(self, command=combine_funcs(window.destroy, self.destroy), text="OK").grid(row=1, column=0)
        self.lift()  
        self.grab_set()  
        

def showerror(string, window):
    Error(string, window)
  
global helpCounterWindow
helpCounterWindow = 1 
 
def createHelpWindow():
    global helpCounterWindow
    
    if helpCounterWindow < 2:
        helpWindow = tk.Toplevel(root)
        helpWindow.resizable(False, False)
        helpWindow.geometry('500x300')
        helpWindow.title('Website Blocker | Help')
        #helpWindow.attributes('-topmost', 'true')
        root.eval(f'tk::PlaceWindow {str(helpWindow)} center')
        maindir = os.getcwd()
        

        image = ImageTk.PhotoImage(file = f'{maindir}\mainBg.png')
        label = tk.Label(helpWindow, image=image, compound='center')
        label.pack(fill='both', expand=True)
        label.image = image
        tk.Label(helpWindow, text='Help', compound='center', font ='Lato 20 bold',  foreground="white", background="#222").place(x=220 ,y=10)



        tk.Label(helpWindow, text ='Block Website : enter the website proceeding with "http(s)" or IP. \nEx.: https://website.com \nIf you want to add multiple links separate them with ",".' , font ='Lato 10 bold', foreground="white", background="#222", compound="center").place(x=60 ,y=68)
        tk.Label(helpWindow, text ='Unblock Website : the same like in "Block Website"' , font ='Lato 10 bold', foreground="white", background="#222", compound="center").place(x=60 ,y=126)
        tk.Label(helpWindow, text ="Restore to default : removes all blocked websites" , font ='Lato 10 bold', foreground="white", background="#222", compound="center").place(x=60 ,y=146)
        helpCounterWindow+=1
    else:
        messagebox.showinfo("Error", "Hey! You've already opened a new window!")
    
    def on_closing():
        global helpCounterWindow
        showerror('Do you want to quit?', helpWindow)
        helpCounterWindow = 1
    helpWindow.protocol("WM_DELETE_WINDOW", on_closing)




global advancedCounterWindow
advancedCounterWindow = 1 
global treeWebsites
 
def createAdvancedWindow():
    global advancedCounterWindow
    global treeWebsites
    if advancedCounterWindow < 2:
        global treeWebsites
        global advancedWindow
        advancedWindow = tk.Toplevel(root)
        advancedWindow.resizable(False, False)
        advancedWindow.geometry('700x500')
        advancedWindow.title('Website Blocker | Editor')
        #advancedWindow.attributes('-topmost', 'true')
        root.eval(f'tk::PlaceWindow {str(advancedWindow)} center')
        maindir = os.getcwd()
        



        mainBg = tk.PhotoImage(file = f'{maindir}\mainBg.png')
        lockImg = tk.PhotoImage(file = f'{maindir}\lock.png')
        unlockImg = tk.PhotoImage(file = f"{maindir}/unlock.png")
        label = tk.Label(advancedWindow, image=mainBg)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.pack()
        label.image = mainBg
        


        
        tk.Label(advancedWindow, text="Website(IP):",foreground="white", background="#222", font ='Lato 10 bold').place(x=10, y=10)
        
        
        global e1
        e1 = tk.Entry(advancedWindow)
        e1.place(x=120, y=10)
        





        columns = ['website_ip']
        global tree
        tree = ttk.Treeview(advancedWindow, columns=columns, show='headings')
        tree.column("website_ip", minwidth=0, width=600, stretch=tk.NO)
        tree.place(x=50, y=200)

        # define headings
        tree.heading('website_ip', text='Website(IP)')
        # generate sample data
        treeWebsites = getWebsites()

        # add data to the treeview
        for website in treeWebsites:
            tree.insert('', tk.END, values=website)


        


        #tree.bind('<<TreeviewSelect>>', addToUnblockedWebsites)
        tree.bind('<Double-Button-1>',GetValue)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(advancedWindow, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        
        bBtn = tk.Button(advancedWindow, text = 'Block',font = 'Lato 12 bold',image = lockImg, pady = 5, width = 30, background="#222", activebackground="#222", borderwidth=0, command = combine_funcs(addToBlockedWebsites))
        bBtn.place(x=275, y=5)
        bBtn.image = lockImg
        
        unblockBtn = tk.Button(advancedWindow, text = 'UnBlock',font = 'Lato 12 bold',image = unlockImg, pady = 5, width = 30, background="#222", activebackground="#222", borderwidth=0,  command = addToUnblockedWebsites)
        unblockBtn.place(x=660, y=200)
        unblockBtn.image = unlockImg



       

        advancedCounterWindow+=1
    else:
        messagebox.showinfo("Error", "Hey! You've already opened a new window!")
    
    def on_closing():
        global advancedCounterWindow
        showerror('Do you want to quit?', advancedWindow)
        advancedCounterWindow = 1
    advancedWindow.protocol("WM_DELETE_WINDOW", on_closing)



if is_admin():
    

    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    root.geometry('500x300')
    root.resizable(0,0)
    root.title("Website Blocker")
    root.configure(bg="#222")
    maindir = os.getcwd() #Put all the files including images next to WebsiteBlocker.exe so application can load them


    filename = tk.PhotoImage(file = f'{maindir}\mainBg.png')


    background_label = tk.Label(image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(root, text ='WEBSITE BLOCKER' , font ='Lato 20 bold',  foreground="white", background="#222").pack()


    host_path = os.getenv("SystemDrive") + '\Windows\System32\drivers\etc\hosts'
    ip_address = '127.0.0.1'


    tk.Label(root, text ='Block Website :' , font ='Lato 10 bold', foreground="white", background="#222").place(x=10 ,y=68)
    Websites = tk.Text(root,font = 'Lato 10',height='2', width = '40', wrap = tk.WORD, padx=5, pady=5)
    Websites.place(x= 140,y = 60)



    tk.Label(root, text ='Unblock Website :' , font ='Lato 10 bold', foreground="white", background="#222").place(x=10 ,y=132)
    UnWebsites = tk.Text(root,font = 'Lato 10',height='2', width = '40', wrap = tk.WORD, padx=5, pady=5)
    UnWebsites.place(x= 140,y = 120)



    

    img = tk.PhotoImage(file = f'{maindir}/lock.png')
    block = tk.Button(root, text = 'Block',font = 'Lato 12 bold',pady = 5,command = Blocker ,width = 30, image=img, background="#222", activebackground="#222", borderwidth=0)
    block.place(x = 450, y = 64)

    img2 = tk.PhotoImage(file = f'{maindir}/unlock.png')
    unlock = tk.Button(root, text = 'UnBlock',font = 'Lato 12 bold',pady = 5,command = UnBlocker ,width = 30, image=img2, background="#222", activebackground="#222", borderwidth=0)
    unlock.place(x = 450, y = 128)





    helpimg = tk.PhotoImage(file = f'{maindir}/help.png')
    HelpBtn = tk.Button(root, 
                text="Help",
                command=createHelpWindow, image=helpimg,background="#222", activebackground="#222", borderwidth=0).pack(side=tk.BOTTOM)

   
    tk.Label(root, text ='Restore to default :' , font ='Lato 10 bold', foreground="white", background="#222").place(x=10 ,y=200)
    restoreimg = tk.PhotoImage(file = f'{maindir}/restore.png')
    RestoreBtn = tk.Button(root,text="Restore",
                command=Restore, image=restoreimg,background="#222", activebackground="#222", borderwidth=0)
    RestoreBtn.place(x=140, y=200)



    advancedimg = tk.PhotoImage(file = f'{maindir}/advanced.png')
    AdvancedBtn = tk.Button(root,text="Editor",
                command=createAdvancedWindow, image=advancedimg,background="#222", activebackground="#222", borderwidth=0)
    AdvancedBtn.place(rely=1.0, relx=1.0, x=0, y=0, anchor="se")

    
    
    root.mainloop()


else:
    
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)


def main():
    is_admin()