try:
    from Tkinter import *
except:
    from tkinter import *
# Global Vars
Count = 0

# initialize GUI
root = Tk();
root.title("babe survey")

# import media
Crying_man = PhotoImage(file = "tenor.gif") # import image

def babeConfirmer():
    replyButton = "confirmed!!" + " and wow age is " + age.get()
    LB_confrirmGril= Label(root, text=replyButton ).grid(row = 2, column = 0, columnspan= 3)
    LP_Cryman = Label(root, image=Crying_man, pady=10).grid(row = 3, column = 0, columnspan= 3)
    global Count
    Count += 1

# intro text
myLabel = Label (root, text = "Hello ").grid(row = 0, column = 0)
L_Grilask = Label (root, text = "You are ?").grid(row = 1, column = 0)

# button
B_confirm = Button(root, text = "Confirm baby", padx=20, pady=10, borderwidth=5, command= babeConfirmer).grid(row = 1, column = 1, columnspan= 2)

#input box
L_askAge = Label (root, text = "Age:").grid(row = 0, column = 1, sticky= E)
age = Entry(root, width=20, borderwidth=2) #seperate button call and grip placement so you can call button object in other places
age.grid(row = 0, column = 2)

# dynamic text
L_confirmCount = Label (root, text = "confirmed " + str(Count) + " times", relief="sunken").grid(row = 4, column = 0, columnspan= 5, sticky= W+E)

# Lab_moteTable = Label (Frame_Motes, text = "MOTE ID", relief=SUNKEN)   .grid(row=0, column=0)
# Lab_moteTable = Label (Frame_Motes, text = "USER ID", relief=SUNKEN)   .grid(row=0, column=1)
# Lab_moteTable = Label (Frame_Motes, text = "Temp(C)", relief=SUNKEN)   .grid(row=0, column=2)
# Lab_moteTable = Label (Frame_Motes, text = "Humid(RH)", relief=SUNKEN) .grid(row=0, column=3)
# Lab_moteTable = Label (Frame_Motes, text = "LUX", relief=SUNKEN)       .grid(row=0, column=4)

# # create scroll bar
# MoteScroll = Scrollbar(Frame_Motes)
#
#
# # create treeview Tavle
# Tre_MoteTable = ttk.Treeview(Frame_Motes,yscrollcommand=MoteScroll.set)
# tabs  = ("Status", "Temp", "Humid", "Lux", "O2", "CO2", "Accel", "Wind", "Rain")
# units = ("",        "(C)", "(RH)", "", "(%)","(ppm)", "",   "(M/s)", ".")
# Tre_MoteTable['columns'] = tabs
#
# MoteScroll.config(command = Tre_MoteTable.yview)
#
# # Define columns
# TabWidths = (90,50,50,50,50,50,50,50,50)
# Tre_MoteTable.column("#0", width= 110, minwidth= 50, anchor=W)
# for n in range(len(tabs)-1):
#     Tre_MoteTable.column(tabs[n], width= TabWidths[n], minwidth= TabWidths[n], anchor=CENTER)
# Tre_MoteTable.column(tabs[8], width= TabWidths[8], minwidth= TabWidths[8], anchor=E)
#
# # Define Heading
# Tre_MoteTable.heading("#0", text="Mote(MAC)")
# for n in range(len(tabs)):
#     print n
#     Tre_MoteTable.heading(tabs[n], text=tabs[n] + units[n])
#
# #insert Info
# SpoofMacs = ('60-d0-35', '60-d1-41', '60-d0-40', '60-45-dl', '60-d0-11', '60-d0-35', '60-d1-41', '60-d0-40', '60-45-dl', '60-d0-11', '60-d0-52',
#             '60-d0-35', '60-d1-41', '60-d0-40', '60-45-dl', '60-d0-11', '60-d0-52', '60-d0-35', '60-d1-41', '60-d0-40', '60-45-dl', '60-d0-11', '60-d0-52')
# for n in range(len(SpoofMacs)):
#  Tre_MoteTable.insert(parent='', index='end', iid = n, text = 'Mote-'+SpoofMacs[n], values=("OPERATIONAL", 0, 0, 0, 0, 0, 0, 0, 0))


root.mainloop()