try:
    from Tkinter import *
except:
    from tkinter import *
import ttk
class MoteTable():
    def __init__(self, Parent, Headers, MoteRows):
        self.ParentFrame = Parent
        self.Table = []
        self.Row = []
        self.headrow = []

        self.headrow.append(Label(Parent, text='Graph', relief=GROOVE, borderwidth=2))
        for header in Headers:
            self.headrow.append(Label(Parent, text = header,relief = GROOVE, borderwidth=2))

        for mote in MoteRows :
            Label_row = []
            for info in mote:
                Label_row.append(Label(Parent, text=info, relief=GROOVE, borderwidth=2))

            self.Table.append(Label_row)


    def pack_in(self):
        Grid.rowconfigure(self.ParentFrame, 0, weight=1)
        self.LayRow(self.headrow, 0,0)
        for n in range(len(self.Table)):
            Grid.rowconfigure(self.ParentFrame, n+1, weight=1)
            self.LayRow(self.Table[n], n + 1,1)
            Button(self.ParentFrame, text='+', borderwidth=2, pady=0).grid(row = n+1, column=0)

    def LayRow(self, Label_row, row_num, startCol):
        for n in range(len(Label_row)):
            Label_row[n].grid(row = row_num, column=startCol+n, sticky=EW)


dir = sys.path[0] + "/DataOrganization/"
# initialize GUI
root = Tk()
root.title("Sensor Suite Data Viewer")
#root.iconbitmap('')
root.geometry("1200x800")

Frame_Setup = LabelFrame(root, text = 'setup',      relief = GROOVE, padx=10, pady=10, borderwidth=4)
Frame_Motes = LabelFrame(root, text = 'Mote View',  relief = GROOVE, padx=5, pady=5, borderwidth=4)
Frame_History = LabelFrame(root, text = 'Graph',  relief = GROOVE, padx=5, pady=5, borderwidth=4)

Lab_Directory = Label (Frame_Setup,
                       text = "Directory:               {directory}".format( directory = dir[0:3]+ " .... " + dir[-35:-1])
                       )
Lab_ChangeDir = Label(Frame_Setup, text = "Change Directory: ")
In_dir = Entry(Frame_Setup, width=50, borderwidth=2) #seperate button call and grip placement so you can call button object in other places

lab_numOfMotes = Label(Frame_Setup, text = "Number of Motes in network: ")
lab_DataSpan = Label(Frame_Setup, text = "DateSpan of collected Data: ")



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

# CREATE SCROLLABLE FRAME/CANVAS
MoteFrame = Frame(Frame_Motes, bg='Black')
MoteFrame.pack(fill=BOTH, expand = 1)
# Create Canvas
Mcanvas = Canvas(MoteFrame)
Mcanvas.pack(side=LEFT, fill=BOTH, expand=1)
# scrollbar
Mscrollbar = ttk.Scrollbar(MoteFrame, orient=VERTICAL, command=Mcanvas.yview)
Mscrollbar.pack(side=RIGHT, fill=Y)
# config canvas
Mcanvas.configure(yscrollcommand=Mscrollbar.set)
# bind config
Mcanvas.bind('<Configure>', lambda e: Mcanvas.configure(scrollregion=Mcanvas.bbox("all")))
SecondFrame = Frame(Mcanvas)
Mcanvas.create_window((0,0), window=SecondFrame, anchor=NW)
# for n in range(100):
#     Button(SecondFrame, text=str(n)).grid(row= n, column=0)
#     Label(SecondFrame, text='wow', relief=SUNKEN).grid(row= n, column=1)
# MOTE TABLE

Headers  = ("mote","Status", "Temp", "Humid", "Lux", "O2", "CO2", "Accel", "Wind", "Rain")
Mote_Rows = []
for n in range(100):
    row = ["Mote " + str(n), "OPERATIONAL", n+9, 30, 0, 0, 0, 0, 0,0]
    Mote_Rows.append(row)
M_Table = MoteTable(SecondFrame, Headers,Mote_Rows)
M_Table.pack_in()

# FRAME PACKING
Grid.rowconfigure(root, 0, weight=0)
Grid.rowconfigure(root, 1, weight=10)
Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=10)


Frame_Setup.grid(pady=6, padx=6, row = 0, column = 0, sticky=NSEW)
Frame_Motes.grid(pady=6, padx=6, row = 1, column = 0, sticky=NSEW)
Frame_History.grid(pady=6, padx=8, row = 0, rowspan=2,  column = 1, sticky=NSEW)

# LABEL PACKING
Lab_Directory.grid(row = 0, column = 0, columnspan= 2, sticky=W)
Lab_ChangeDir.grid(row = 1, column = 0, )
In_dir.grid(row = 1, column = 1)
lab_numOfMotes.grid(row = 2, column = 0, columnspan= 2, sticky=W)
lab_DataSpan.grid(row = 3, column = 0, columnspan= 2, sticky=W)


Grid.columnconfigure(Frame_Motes, 0, weight=10)
Grid.columnconfigure(Frame_Motes, 1, weight=10)
pady = 190
# Tre_MoteTable.grid(row=0,column=0, ipady=pady, sticky=NS)
# MoteScroll.grid(row=0,column=1, sticky=NS)

def updateGUI():
    #print 'update'
    #Tre_MoteTable.grid(ipady = TreeHeight)
    root.after(16, updateGUI)
#root.after(100,updateGUI)

root.mainloop()

