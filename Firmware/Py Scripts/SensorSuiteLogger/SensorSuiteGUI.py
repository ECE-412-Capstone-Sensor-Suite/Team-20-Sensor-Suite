try:
    from Tkinter import *
except:
    from tkinter import *
import ttk
from tkFont import Font
class MoteTable():
    def __init__(self, Parent, Headers, MoteRows):
        self.ParentFrame = Parent
        self.Cells = []
        self.Row = []
        self.headrow = []
        for header in Headers:
            self.headrow.append(Button(Parent, bg = 'light blue', text = header,relief = RAISED , borderwidth=3))

        for mote in MoteRows :
            Label_row = []
            for info in mote:
                if info == mote[0]:
                    Label_row.append(Button(self.ParentFrame, text=info, borderwidth=3, font= Font(size=110)))
                elif info == mote[1]:
                        if info=="OPERATIONAL":
                            Label_row.append(
                                Label(Parent, font=Font(size=8), bg='DarkOliveGreen1', text=info, relief=GROOVE,
                                      borderwidth=2))
                        else:
                            Label_row.append(
                                Label(Parent, font=Font(size=8), bg='salmon1', text=info, relief=GROOVE,
                                      borderwidth=2))


                else:
                    Label_row.append(Label(Parent, font= Font(size=8), bg = 'gainsboro', text=info, relief=SUNKEN, borderwidth=2))

            self.Cells.append(Label_row)


    def pack_in(self):
        Grid.rowconfigure(self.ParentFrame, 0, weight=1)
        self.LayRow(self.headrow, 0,0)
        for n in range(len(self.Cells)):
            Grid.rowconfigure(self.ParentFrame, n+1, weight=1)
            self.LayRow(self.Cells[n], n + 1, 0)

    def LayRow(self, Label_row, row_num, startCol):
        for n in range(len(Label_row)):
            Label_row[n].grid(row = row_num, column=startCol+n, sticky=NSEW)


dir = sys.path[0] + "/DataOrganization/"
# initialize GUI
root = Tk()
root.title("Sensor Suite Data Viewer")
#root.iconbitmap('')
root.geometry("1400x800")

Frame_Setup = LabelFrame(root, text = 'setup',      relief = GROOVE, padx=10, pady=10, borderwidth=4)
Frame_Motes = LabelFrame(root, text = 'Mote View',  relief = GROOVE, padx=5, pady=5, borderwidth=4)
Frame_History = LabelFrame(root, text = 'Graph',  relief = GROOVE, padx=5, pady=5, borderwidth=4)

Lab_Directory = Label (Frame_Setup,
                       text = "Directory:               {directory}".format( directory = dir[0:3] + " .... " + dir[-35:-1])
                       )
Lab_ChangeDir = Label(Frame_Setup, text = "Change Directory: ")
In_dir = Entry(Frame_Setup, width=50, borderwidth=2) #seperate button call and grip placement so you can call button object in other places

lab_numOfMotes = Label(Frame_Setup, text = "Number of Motes in network: ")
lab_DataSpan = Label(Frame_Setup, text = "DateSpan of collected Data: ")

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
    row = [str(n)+'C' + '-D'+str(n) + '-6' + str(n), "OPERATIONAL", n+9, 30, 0, 0, 0, 0, 0,0]
    Mote_Rows.append(row)
M_Table = MoteTable(SecondFrame, Headers,Mote_Rows)
M_Table.pack_in()

# Customize Cells
for cell in M_Table.headrow:
    cell['font'] = Font(size = 9)

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

