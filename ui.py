from cgitb import text
from ctypes import alignment
from tkinter import *
from tkinter.ttk import Progressbar
import functions as func
from py2neo import Graph
import conf
from dataclasses import dataclass
from threading import Thread
from PIL import ImageTk, Image
import os


@dataclass
class GlobalVariables:
    #database
    database_uri : str
    username : str
    password : str
    graph : Graph
    
    #ui
    root_window : Tk




def connectDbAndReturnGraph(uri, username, password):
    return Graph(uri, auth=(username, password))


def createLoginFrame():
    
    def inner_prendiCredenziali():
        return (insert_uri.get() ,insert_username.get(), insert_pass.get())

    def loginAndChangeFrame():
        try:
            credenziali = inner_prendiCredenziali()
            graph = connectDbAndReturnGraph(credenziali[0], credenziali[1], credenziali[2])
            global_var.database_uri = credenziali[0]
            global_var.username = credenziali[1]
            global_var.password = credenziali[2]
            global_var.graph = graph
            label_error.pack_forget()
            frame_login.pack_forget()
            frame_menu.pack()

        except:
            label_error.pack()
        return 

    frame_login = Frame(global_var.root_window, bg = "white")
    label_error = Label(frame_login, text="Login Error", font='Arial 25', background="white", foreground="red")

    img = Image.open('covid.jpg')
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(frame_login, image=img, background='white')
    panel.image = img
    panel.pack()

    label_uri = Label(frame_login, text="Insert the uri of the db:", font='Arial 15', foreground="green", background="white", pady=20)
    label_uri.pack()
    insert_uri = Entry(frame_login, font="Arial 20")
    insert_uri.insert(0, conf.uri)
    insert_uri.pack(pady=5)
    label_insert_username = Label(frame_login, text="Insert your username:", font='Arial 15', foreground="green", background="white", pady=20)
    label_insert_username.pack()
    insert_username = Entry(frame_login, font="Arial 20")
    insert_username.insert(0, conf.username)
    insert_username.pack(pady=5)
    label_insert_pass = Label(frame_login, text="Insert your password:", font='Arial 15', foreground="green", background="white", pady=20)
    label_insert_pass.pack()
    insert_pass = Entry(frame_login, font="Arial 20", show="*")
    insert_pass.pack(pady=5)

    button_login = Button(frame_login, text="Login", command=loginAndChangeFrame, pady=15, padx=55)
    button_login.pack()

    button_quit = Button(frame_login, text="Quit", background= 'yellow', command=quit, pady=15, padx=58)
    button_quit.pack()

    return frame_login


def createRootWindow():
    root = Tk()
    root.title("COVID DATABASE")
    root.geometry("800x800")
    root.configure(background="white")
    titolo = Label(root, text="SMBUD DELIVERY 1: NEO4J",font="Arial 30" ,background="white")
    titolo.pack()
    sottotitolo = Label(root, text="Giuseppe Urso, Simone Reale, Hazem Shalby, Marco Somaschini, Andrea Vitobello", font="Times 15" ,background="white", foreground="green")
    sottotitolo.pack()
    return root



def managePopulationFrame():

    def goToMenu():
        frame_manage_pop.pack_forget()
        frame_menu.pack()
        return

    def create():
        t = Thread(target=func.createPopulation, args=(global_var.graph, scale_pop.get() - 1, progress_bar))
        t.start()
        return

    def delete():
        func.deletePopulation(global_var.graph)

    frame_manage_pop = Frame(global_var.root_window, bg = "white")
    label_program = Label(frame_manage_pop, text="Manage population", font="Arial 25", background="white", pady=40)
    label_program.pack()
    label_2 = Label(frame_manage_pop, text="Choose the number of people to be created:", font="Arial 15", background="white", pady=5)
    label_2.pack()
    scale_pop = Scale(frame_manage_pop, from_=15, to=1500, orient="horizontal", background="white", length=300, cursor="plus", font="Arial 15")
    scale_pop.set(500)
    scale_pop.pack(pady=20)
    button_create_pop = Button(frame_manage_pop, text="Create population",command=create , pady=15, padx=15,)
    button_create_pop.pack()
    button_delete_pop = Button(frame_manage_pop, text="Kill everyone", command=delete , background="red", pady=25, padx=29, cursor="pirate")
    button_delete_pop.pack()
    progress_bar = Progressbar(frame_manage_pop, orient=HORIZONTAL, mode='determinate', length=300, )
    go_to_menu = Button(frame_manage_pop, text="Go to Menu", command=goToMenu,  pady=25, padx=32, activebackground="red")
    go_to_menu.pack()
    return frame_manage_pop




def createMenuFrame():
    def goToFrameCreatePop():
        frame_menu.pack_forget()
        frame_create_pop.pack()
        return
    def goToFrame1():
        frame_menu.pack_forget()
        frame1.pack()
        return
    def goToFrame2():
        frame_menu.pack_forget()
        frame2.pack()
        return
    def goToFrame3():
        frame_menu.pack_forget()
        frame3.pack()
        return
    def goToFrame4():
        frame_menu.pack_forget()
        frame4.pack()
        return
    def goToFrame5():
        frame_menu.pack_forget()
        frame5.pack()
        return

    frame_menu = Frame(global_var.root_window, bg="white")
    label_menu = Label(frame_menu, text="MENU", font="Arial 30", background="white", pady=40)
    label_menu.pack()

    button_frame_create_pop = Button(frame_menu, text="Manage population", command=goToFrameCreatePop, pady=15, padx=45)
    button_frame_create_pop.pack()


    button_frame1 = Button(frame_menu, text="Go to frame 1", background="red", command=goToFrame1, pady=15, padx=25)
    button_frame1.pack()

    button_frame2 = Button(frame_menu, text="Go to frame 2", background="yellow", command=goToFrame2, pady=15, padx=25)
    button_frame2.pack()

    button_frame3 = Button(frame_menu, text="Go to frame 3", background="orange", command=goToFrame3, pady=15, padx=25)
    button_frame3.pack()

    button_frame4 = Button(frame_menu, text="Go to frame 4", background="green", command=goToFrame4, pady=15, padx=25)
    button_frame4.pack()

    button_frame5 = Button(frame_menu, text="Go to frame 5", background="pink", command=goToFrame5, pady=15, padx=25)
    button_frame5.pack()

    button_quit = Button(frame_menu, text="Quit", command=quit, pady=15, padx=85)
    button_quit.pack()
    
    return frame_menu










def createFrame1():
    def goToMenu():
        frame1.pack_forget()
        frame_menu.pack()
        return
    frame1 = Frame(global_var.root_window, bg="white")
    label_frame1 = Label(frame1, text="FRAME 1", font="20", background="white", pady=20)
    label_frame1.pack()
    go_to_menu = Button(frame1, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame1














def createFrame2():
    def goToMenu():
        frame2.pack_forget()
        frame_menu.pack()
        return
    frame2 = Frame(global_var.root_window, bg="white")
    label_frame2 = Label(frame2, text="FRAME 2", font="20", background="white", pady=20)
    label_frame2.pack()
    go_to_menu = Button(frame2, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame2














def createFrame3():
    def goToMenu():
        frame3.pack_forget()
        frame_menu.pack()
        return
    frame3 = Frame(global_var.root_window, bg="white")
    label_frame3 = Label(frame3, text="FRAME 3", font="20", background="white", pady=20)
    label_frame3.pack()
    go_to_menu = Button(frame3, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame3












def createFrame4():
    def goToMenu():
        frame4.pack_forget()
        frame_menu.pack()
        return
    frame4 = Frame(global_var.root_window, bg="white")
    label_frame4 = Label(frame4, text="FRAME 4", font="20", background="white", pady=20)
    label_frame4.pack()
    go_to_menu = Button(frame4, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame4














def createFrame5():
    def goToMenu():
        frame5.pack_forget()
        frame_menu.pack()
        return
    frame5 = Frame(global_var.root_window, bg="white")
    label_frame5 = Label(frame5, text="FRAME 5", font="20", background="white", pady=20)
    label_frame5.pack()
    go_to_menu = Button(frame5, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame5





if __name__ == "__main__":
    
    global_var = GlobalVariables("","","", any, createRootWindow())
    frame_login = createLoginFrame()
    frame_login.pack()
    
    frame_menu = createMenuFrame()
    frame_create_pop = managePopulationFrame()
    
    frame1 = createFrame1()
    frame2 = createFrame2()
    frame3 = createFrame3()
    frame4 = createFrame4()
    frame5 = createFrame5()

    global_var.root_window.mainloop()

