from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Treeview
from tkcalendar import Calendar

import functions
import functions as func
import py2neo
from py2neo import Graph
import conf
from dataclasses import dataclass
from threading import Thread
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter

import numpy as np


@dataclass
class GlobalVariables:
    #database
    database_uri : str
    db_username : str
    db_password : str
    db_graph : Graph

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
            global_var.db_username = credenziali[1]
            global_var.db_password = credenziali[2]
            global_var.db_graph = graph
            label_error.pack_forget()
            frame_login.pack_forget()
            frame_menu.pack()

        except:
            label_error.pack()
        return

    frame_login = Frame(global_var.root_window, bg = "white")
    label_error = Label(frame_login, text="Login Error", font='Arial 25', background="white", foreground="red")

    img = Image.open('images\\covid.jpg')
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
    #Remove this eventually
    insert_pass.insert(0, conf.password)
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
        t = Thread(target=func.createDataset, args=(global_var.db_graph, scale_pop.get() - 1, progress_bar, progress_bar_label, choice_infected.get()))
        t.start()
        return

    def delete():
        func.deleteDataset(global_var.db_graph)


    choice_infected = IntVar()

    frame_manage_pop = Frame(global_var.root_window, bg = "white")
    label_program = Label(frame_manage_pop, text="Manage population", font="Arial 25", background="white", pady=40)
    label_program.pack()
    label_2 = Label(frame_manage_pop, text="Choose the number of people to be created:", font="Arial 15", background="white", pady=5)
    label_2.pack()
    scale_pop = Scale(frame_manage_pop, from_=15, to=1500, orient="horizontal", background="white", length=400, cursor="plus", font="Arial 15")
    scale_pop.set(500)
    scale_pop.pack(pady=15)
    ChkBttn = Checkbutton(frame_manage_pop, variable=choice_infected, text="Start with some infected people", background="white")
    ChkBttn.pack(padx = 5, pady = 15)
    button_create_pop = Button(frame_manage_pop, text="Create population",command=create , pady=15, padx=15,)
    button_create_pop.pack()
    button_delete_pop = Button(frame_manage_pop, text="Kill everyone", command=delete , background="red", pady=25, padx=29, cursor="pirate")
    button_delete_pop.pack()
    progress_bar_label = Label(frame_manage_pop, text="Creating people and family relationships...", font="Arial 12", background="white", pady=40)
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
    def goToFrameSimulation():
        frame_menu.pack_forget()
        frameSimulation.pack()
        return
    def goToFrame2():
        frame_menu.pack_forget()
        frame2.pack()
        return
    def goToFrame22():
        frame_menu.pack_forget()
        frame22.pack()
        return
    def goToFrame3():
        frame_menu.pack_forget()
        frame3.pack()
        return
    def goToFrameAddContact():
        frame_menu.pack_forget()
        frameAddContact.pack()
        return
    def goToFrame4():
        frame_menu.pack_forget()
        frame4.pack()
        return
    def goToFrame5():
        frame_menu.pack_forget()
        frame5.pack()
        return
    def goToFrame9():
        frame_menu.pack_forget()
        frame9.pack()
        return
    def goToFrame10():
        frame_menu.pack_forget()
        frame10.pack()

    frame_menu = Frame(global_var.root_window, bg="white")
    label_menu = Label(frame_menu, text="MENU", font="Arial 30", background="white", pady=40)
    label_menu.pack()

    button_frame_create_pop = Button(frame_menu, text="Manage population", command=goToFrameCreatePop, pady=15, padx=45)
    button_frame_create_pop.pack()


    button_frame1 = Button(frame_menu, text="Go to graph number of infected per day", background="red", command=goToFrame1, pady=15, padx=25)
    button_frame1.pack()

    button_frameSimulation = Button(frame_menu, text="Simulate!", background="red", command=goToFrameSimulation, pady=15, padx=25)
    button_frameSimulation.pack()

    button_frame2 = Button(frame_menu, text="Add a Test", background="yellow", command=goToFrame2, pady=15, padx=25)
    button_frame2.pack()
    button_frame22 = Button(frame_menu, text="Place with most new case", background="yellow", command=goToFrame22, pady=15, padx=25)
    button_frame22.pack()

    button_frame3 = Button(frame_menu, text="Go to the possibly-infected people finder", background="orange", command=goToFrame3, pady=15, padx=25)
    button_frame3.pack()

    button_frameAddContact = Button(frame_menu, text="Add new contact", background="orange", command=goToFrameAddContact, pady=15, padx=25)
    button_frameAddContact.pack()

    button_frame4 = Button(frame_menu, text="Go to frame 4", background="green", command=goToFrame4, pady=15, padx=25)
    button_frame4.pack()

    button_frame5 = Button(frame_menu, text="Go to frame 5", background="pink", command=goToFrame5, pady=15, padx=25)
    button_frame5.pack()

    button_frame9 = Button(frame_menu, text="Go to frame 9", background="green", command=goToFrame9, pady=15, padx=25)
    button_frame9.pack()

    button_frame10 = Button(frame_menu, text="Go to frame 10", background="pink", command=goToFrame10, pady=15, padx=25)
    button_frame10.pack()

    button_quit = Button(frame_menu, text="Quit", command=quit, pady=15, padx=85)
    button_quit.pack()

    return frame_menu









#frame reale
def createFrame1():
    def goToMenu():
        frame1.pack_forget()
        frame_menu.pack()
        return

    def graphNumbersOfInfectedPerDay():
        dictionary = func.createDictionaryNumberOfInfectedPerDay(global_var.db_graph)
        plt.bar(list(dictionary.keys()), dictionary.values(), color='g')
        plt.xticks(rotation=90)
        plt.ylabel('number of infected')
        plt.show()





    frame1 = Frame(global_var.root_window, bg="white")
    label_frame1 = Label(frame1, text="GRAPH THE NUMBER OF INFECTED PER DAY", font="20", background="white", pady=20)
    label_frame1.pack()
    graph_it = Button(frame1, text="Graph number of infected per day!", command=graphNumbersOfInfectedPerDay)
    graph_it.pack(pady=40, padx=40)
    go_to_menu = Button(frame1, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame1



#frame reale 2
def createFrameSimulation():
    def goToMenu():
        frameSimulation.pack_forget()
        frame_menu.pack(pady=30)
        return

    def simulate():
        t = Thread(target=func.simulatePandemic, args=(global_var.db_graph, scale_pop.get(), progress_bar, progress_bar_label, scale_inf.get()))
        t.start()
        return





    frameSimulation = Frame(global_var.root_window, bg="white")
    label_pop = Label(frameSimulation, text="INITIAL NUMBER OF PEOPLE", font="Arial 12", background="white", pady=5)
    label_pop.pack()
    scale_pop = Scale(frameSimulation, from_=15, to=500, orient="horizontal", background="white", length=400, cursor="plus", font="Arial 15")
    scale_pop.set(250)
    scale_pop.pack(pady=15)
    label_inf = Label(frameSimulation, text="INITIAL NUMBER OF INFECTED PEOPLE", font="Arial 12", background="white", pady=5)
    label_inf.pack()
    scale_inf = Scale(frameSimulation, from_=1, to=500, orient="horizontal", background="white", length=400, cursor="plus", font="Arial 15")
    scale_inf.set(30)
    scale_inf.pack(pady=15)
    simulate = Button(frameSimulation, text="Simulate!", command=simulate, pady=50, padx=50)
    simulate.pack(pady=40, padx=40)
    progress_bar_label = Label(frameSimulation, text="Creating people and family relationships...", font="Arial 12", background="white", pady=40)
    progress_bar = Progressbar(frameSimulation, orient=HORIZONTAL, mode='determinate', length=300, )
    go_to_menu = Button(frameSimulation, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frameSimulation









#frame shalby
def createFrame2():
    def goToMenu():
        frame2.pack_forget()
        frame_menu.pack()
        return
    def addCovidTest():
        result = (value_test_result.get()=="Positive")
        t = Thread(target=func.addCovidTest, args=(global_var.db_graph, insert_name.get(), insert_surname.get(), cal.get_date(), value_test_type.get(), result))
        t.start()
        return
    frame2 = Frame(global_var.root_window, bg="white")
    label_frame2 = Label(frame2, text="ADD A NEW COVID TEST", font="Arial 20", background="white", pady=10)
    label_frame2.pack()
    #name
    Label(frame2, text="Insert the name of patient:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    insert_name = Entry(frame2, font="Arial 20")
    insert_name.pack(pady=5)
    #surname
    Label(frame2, text="Insert the surname of patient:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    insert_surname = Entry(frame2, font="Arial 20")
    insert_surname.pack(pady=5)
    #test date
    Label(frame2, text="Insert test date:", font='Arial 15', foreground="green", background="white", pady=5).pack()
    cal= Calendar(frame2, date_pattern="yyyy-mm-dd")
    cal.pack(pady=5)
    #test type
    Label(frame2, text="Insert test type:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    options_list_type = ["MOLECULAR_TEST", "ANTIGEN_TEST", "ANTIBODY_TEST"]
    value_test_type = StringVar(frame2)
    value_test_type.set("Select an Option")
    test_type = OptionMenu(frame2, value_test_type, *options_list_type)
    test_type.pack(pady=5)
    #test result
    Label(frame2, text="Insert test Result:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    options_list_result = ["Positive", "Negative"]
    value_test_result = StringVar(frame2)
    value_test_result.set("Select an Option")
    test_type = OptionMenu(frame2, value_test_result, *options_list_result)
    test_type.pack(pady=5)
    #add button
    button_add_test = Button(frame2, text="Add Test", command=addCovidTest)
    button_add_test.pack()

    go_to_menu = Button(frame2, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame2

#frame shalby 2
def createFrame22():
    def goToMenu():
        frame22.pack_forget()
        frame_menu.pack()
        return

    def graphNumberOfInfectedPerPlace():
        [data, labels] = functions.getInfectedPerPlaceType(global_var.db_graph)

        # Wedge properties
        wp = {'linewidth': 1, 'edgecolor': "green"}

        # Creating autocpt arguments
        def func(pct, allvalues):
            absolute = int(pct / 100. * np.sum(allvalues))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)

        # Creating plot
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(data,
                                          autopct=lambda pct: func(pct, data),
                                          labels=labels,
                                          wedgeprops=wp,
                                          textprops=dict(color="magenta"))

        # Adding legend
        ax.legend(wedges, labels,
                  title="Places",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title("Customizing pie chart")

        # show plot
        plt.show()
    frame22 = Frame(global_var.root_window, bg="white")
    label_frame22= Label(frame22, text="NUMBER OF INFECTED PER PLACE", font="20", background="white", pady=20)
    label_frame22.pack()
    graph_it = Button(frame22, text="Graph number of infected per place type", command=graphNumberOfInfectedPerPlace)
    graph_it.pack(pady=40, padx=40)
    go_to_menu = Button(frame22, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()

    return frame22












#frame somaschini
def createFrame3():

    def goToMenu():
        frame3.pack_forget()
        tree.pack_forget()
        frame_menu.pack()
        return
    def findPeopleAtRisk():
        data  = func.findPeopleAtRisk(global_var.db_graph)
        tree.pack_forget()
        tree.pack()
        tree.heading(1, text="Name")
        tree.heading(2, text="Surname")
        tree.heading(3, text="Date of Contact")
        tree.heading(4, text="Place of Contact")

        tree.column(1, width = 100)
        tree.column(2, width = 100)
        tree.column(3, width = 100)
        tree.column(4, width = 100)

        for record in data:
            keys = list(record)
            tree.insert('', 'end', values = (record[keys[0]], record[keys[1]], record[keys[2]], record[keys[3]]))
        return

    frame3 = Frame(global_var.root_window, bg="white")
    label_frame3 = Label(frame3, text="Analysis of infection spread", font="20", background="white", pady=20)
    label_frame3.pack()
    tree = Treeview(frame3, columns = (1,2,3,4), height = 25, show = "headings")
    findPeopleAtRisk = Button(frame3, text="Find possible infected", command=findPeopleAtRisk)
    findPeopleAtRisk.pack()
    go_to_menu = Button(frame3, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame3


def createFrameAddContact():
    def goToMenu():
        frameAddContact.pack_forget()
        frame_menu.pack()
        return
    def addContact():
        try:
            log = func.addContact(
                global_var.db_graph,
                entries['First Name'].get(),
                entries['Last Name'].get(),
                entries['First Name of the other'].get(),
                entries['Last name of the other'].get(),
                entries['Date'].get(),
                entries['Place'].get()
            )
        except py2neo.errors.ClientError as Ex:
            log = "Invalid query parameters"
        label_output = Label(frameAddContact, text=log, font='Arial 14', background="white", foreground="black")
        label_output.pack()
        return

    frameAddContact = Frame(global_var.root_window, bg="white")
    label_frame3 = Label(frameAddContact, text="Add contact beetween people", font="20", background="white", pady=20)
    label_frame3.pack()

    entries = {
        "First Name":               Entry(frameAddContact),
        "Last Name":                Entry(frameAddContact),
        "First Name of the other":  Entry(frameAddContact),
        "Last name of the other":   Entry(frameAddContact),
        "Date":                     Entry(frameAddContact),
        "Place":                   Entry(frameAddContact)
    }
    for label, entry in entries.items():
        Label(frameAddContact, text = label).pack()
        entry.pack()

    add_contact = Button(frameAddContact, text="Add Contact", command=addContact)
    add_contact.pack()

    go_to_menu = Button(frameAddContact, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frameAddContact






#frame urso
def createFrame4():
    def goToMenu():
        frame4.pack_forget()
        frame_menu.pack()
        return

    def graphNumberOfInfectedPerVaccine():
        infectedPerVaccine = functions.getInfectedPerVaccineType(global_var.db_graph)
        plt.figure(figsize=(9, 9))
        plt.bar(list(infectedPerVaccine.keys()), infectedPerVaccine.values(), color='r')
        plt.xticks(rotation=90)
        plt.ylabel('Number of infected per vaccine type')
        plt.show()
        vaccinatedPerVaccine = functions.getNumberOfVaccinatedPerVaccine(global_var.db_graph)
        mostEffectiveVaccine, lowestRatio = functions.getMostEffectiveVaccine(infectedPerVaccine, vaccinatedPerVaccine)
        string = "The most effective vaccine is: " + mostEffectiveVaccine + " with a infected/total vaccinated ratio = " + str(lowestRatio)
        label2_frame4.configure(text=string)


    frame4 = Frame(global_var.root_window, bg="white")
    label_frame4 = Label(frame4, text="FRAME 4", font="20", background="white", pady=20)
    label_frame4.pack()
    graph_it = Button(frame4, text="Graph number of infected per vaccine type!", command=graphNumberOfInfectedPerVaccine)
    graph_it.pack(pady=40, padx=40)
    go_to_menu = Button(frame4, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    string = ""
    label2_frame4 = Label(frame4, text=string, font="20", background="white", pady=100)
    label2_frame4.pack()

    return frame4













#frame vitobello
def createFrame5():
    def goToMenu():
        frame5.pack_forget()
        frame_menu.pack()
        return

    def averageNumOfPeopleMetByType():
        metByType = functions.averageContactNumber(global_var.db_graph)
        left = [1,2,3]
        height = list(metByType.values())
        labels = list(metByType.keys())
        plt.figure(figsize=(7, 7))
        plt.bar(left, height, tick_label = labels, width=0.8, color=['red', 'blue', 'green'])
        for index in range(len(left)):
            plt.text(1+index, height[index], str(height[index]))
        plt.xticks(rotation=0)
        plt.ylabel('Number of people met by an infected person, by type of contact')
        plt.show()

    frame5 = Frame(global_var.root_window, bg="white")
    label_frame5 = Label(frame5, text="FRAME 5", font="20", background="white", pady=20)
    label_frame5.pack()
    graph_it = Button(frame5, text="Histogram: average number of people met by an infected one, by kind of contact", command=averageNumOfPeopleMetByType)
    graph_it.pack(pady=40, padx=40)
    go_to_menu = Button(frame5, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()

    return frame5


#frame urso
def createFrame9():
    def goToMenu():
        frame9.pack_forget()
        frame_menu.pack()
        return

    def infectFamilies():
        functions.commandInfectFamilies(global_var.db_graph)


    frame9 = Frame(global_var.root_window, bg="white")
    label_frame9 = Label(frame9, text="FRAME 9", font="20", background="white", pady=20)
    label_frame9.pack()
    graph_it = Button(frame9, text="Infect all families with at least one infected person!", command=infectFamilies)
    graph_it.pack(pady=40, padx=40)
    go_to_menu = Button(frame9, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    string = ""
    label2_frame9 = Label(frame9, text=string, font="20", background="white", pady=100)
    label2_frame9.pack()

    return frame9


#frame vitobello2
def createFrame10():
    def goToMenu():
        frame10.pack_forget()
        frame_menu.pack()
        return

    def getInput():
        name = e1.get().upper()
        surname = e2.get().upper()
        vaccine = e3.get().upper()[0:2]
        result = functions.commandAddNewDose(global_var.db_graph, name, surname, vaccine)
        string = "Command Result -> " + result
        label2_frame10.configure(text=string)

    frame10 = Frame(global_var.root_window, bg="white")
    label_frame10 = Label(frame10, text="FRAME 10", font="20", background="white", pady=20)
    label_frame10.pack()


    labelA1 = Label(frame10, text="First Name")
    labelA1.pack()
    e1 = Entry(frame10)
    e1.pack()

    labelA2 = Label(frame10, text="Last Name")
    labelA2.pack()
    e2 = Entry(frame10)
    e2.pack()

    labelA3 = Label(frame10, text="Vaccine Type\n(Pfizer, Moderna, Astrazeneca, Sputnik)")
    labelA3.pack()
    e3 = Entry(frame10)
    e3.pack()

    submit = Button(frame10, text="submit", command=getInput)
    submit.pack()

    go_to_menu = Button(frame10, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()

    string = ""
    label2_frame10 = Label(frame10, text=string, font="20", background="white", pady=100)
    label2_frame10.pack()


    return frame10



if __name__ == "__main__":

    global_var = GlobalVariables("","","", any, createRootWindow())
    frame_login = createLoginFrame()
    frame_login.pack()

    frame_menu = createMenuFrame()
    frame_create_pop = managePopulationFrame()

    frame1 = createFrame1()
    frameSimulation = createFrameSimulation()
    frame2 = createFrame2()
    frame22 = createFrame22()
    frame3 = createFrame3()
    frameAddContact = createFrameAddContact()
    frame4 = createFrame4()
    frame5 = createFrame5()
    frame9 = createFrame9()
    frame10 = createFrame10()

    global_var.root_window.mainloop()
