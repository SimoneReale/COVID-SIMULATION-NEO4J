from cgitb import text
from tkinter import *
import functions as func
from py2neo import Graph
import conf
from dataclasses import dataclass


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


def createFrameLogin():
    
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
    label_error = Label(frame_login, text="Login Error", background="white", foreground="red", font="15", )
    label_uri = Label(frame_login, text="Insert the uri of the db:", background="white", pady=20)
    label_uri.pack()
    insert_uri = Entry(frame_login)
    insert_uri.insert(0, conf.uri)
    insert_uri.pack(pady=5)
    label_insert_username = Label(frame_login, text="Insert your username:", background="white", pady=20)
    label_insert_username.pack()
    insert_username = Entry(frame_login)
    insert_username.insert(0, conf.username)
    insert_username.pack(pady=5)
    label_insert_pass = Label(frame_login, text="Insert your password:", background="white", pady=20)
    label_insert_pass.pack()
    insert_pass = Entry(frame_login, show="*")
    insert_pass.pack(pady=5)

    button_login = Button(frame_login, text="Login", command=loginAndChangeFrame, pady=15, padx=15)
    button_login.pack()

    return frame_login


def createRootWindow():
    root = Tk()
    root.title("COVID DATABASE")
    root.geometry("700x700")
    root.configure(background="white")
    titolo = Label(root, text="SMBUD DELIVERY 1",font="Times 20" ,background="white")
    titolo.pack()
    return root



def createPopulationFrame():

    def goToMenu():
        frame_create_pop.pack_forget()
        frame_menu.pack()
        return

    def create():
        func.createPopulation(global_var.graph, scale_pop.get() - 1)
        return

    frame_create_pop = Frame(global_var.root_window, bg = "white")
    label_program = Label(frame_create_pop, text="Create population frame", font="25", background="white", pady=20)
    label_program.pack()
    scale_pop = Scale(frame_create_pop, from_=2, to=1000, orient="horizontal")
    scale_pop.set(200)
    scale_pop.pack()
    button_create_pop = Button(frame_create_pop, text="Create population",command=create , pady=15, padx=15)
    button_create_pop.pack()
    go_to_menu = Button(frame_create_pop, text="Go to Menu", command=goToMenu,  pady=25, padx=35)
    go_to_menu.pack()
    return frame_create_pop




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
    label_menu = Label(frame_menu, text="MENU", font="20", background="white", pady=20)
    label_menu.pack()

    button_frame_create_pop = Button(frame_menu, text="Go to create population", command=goToFrameCreatePop, pady=15, padx=25)
    button_frame_create_pop.pack()


    button_frame1 = Button(frame_menu, text="Go to frame 1", command=goToFrame1, pady=15, padx=25)
    button_frame1.pack()

    button_frame2 = Button(frame_menu, text="Go to frame 2", command=goToFrame2, pady=15, padx=25)
    button_frame2.pack()

    button_frame3 = Button(frame_menu, text="Go to frame 3", command=goToFrame3, pady=15, padx=25)
    button_frame3.pack()

    button_frame4 = Button(frame_menu, text="Go to frame 4", command=goToFrame4, pady=15, padx=25)
    button_frame4.pack()

    button_frame5 = Button(frame_menu, text="Go to frame 5", command=goToFrame5, pady=15, padx=25)
    button_frame5.pack()
    
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
    frame_login = createFrameLogin()
    frame_login.pack()
    
    frame_menu = createMenuFrame()
    frame_create_pop = createPopulationFrame()
    
    frame1 = createFrame1()
    frame2 = createFrame2()
    frame3 = createFrame3()
    frame4 = createFrame4()
    frame5 = createFrame5()

    global_var.root_window.mainloop()

