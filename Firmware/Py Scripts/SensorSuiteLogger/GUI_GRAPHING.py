try:
    from Tkinter import *
except:
    from tkinter import *
from SensorSuiteAPI import *
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InteractiveGraph():
    def __init__(self, Mesh, MFrame, title, mote, Data):
        for widget in MFrame.winfo_children():
            widget.destroy()
        # ADD TIME SLIDER
        self.FFrame = Frame(MFrame)
        self.MainMesh = Mesh
        self.Data = Data
        FFrame2 = Frame(MFrame)
        self.FFrame.pack()
        FFrame2.pack(side=BOTTOM, expand=1, fill=X, )
        self.Mnum = mote
        self.SPH = 6
        # FILL TIMESTAMP GAPS
        realTime = self.MainMesh.Motes[self.Mnum].timestamp
        filledTime = []
        filledData = []
        sampleIntervalS = (3600)/self.SPH
        for i in range(len(realTime)):
            if i == 0:
                filledTime.append(realTime[i])
            if abs(realTime[i] - filledTime[-1]) > sampleIntervalS:
                while abs(filledTime[-1] - realTime[i]) > sampleIntervalS:
                    filledTime.append(filledTime[-1] + sampleIntervalS)
                    filledData.append(0)
            else:
                filledTime.append(realTime[i])
                filledData.append(self.Data[i])
        filledTime.pop(0)
        print 'new data = ' + str(len(filledData)) + ' new time = ' + str(len(filledTime))
        self.Data =  filledData
        self.timestamps = [datetime.utcfromtimestamp(d) for d in filledTime]
        self.dateStamps = [utctodate(d)[0:utctodate(d).find(':')] for d in filledTime]


        self.span = self.SPH * 3
        self.offsetSpan = int(self.span * 0.4)
        self.sections = len(self.timestamps)/self.offsetSpan - self.span/self.offsetSpan
        print self.sections
        self.time_slide = Scale(FFrame2, from_=0, to=self.sections, orient = HORIZONTAL)
        self.time_slide.pack(fill=X, expand=1)
        self.time_slide.set(self.sections)
        # ADD DATE DROP DOWN MENU
        self.clicked = StringVar()
        options = self.MainMesh.Motes[self.Mnum].dates
        self.clicked.set(options[-1])
        self.oldOption = self.clicked.get()
        drop = OptionMenu(FFrame2, self.clicked, *options)
        drop.pack(side=RIGHT)

        # ADD SPAN CHOOSE BUTTONS
        L_Span_T = Label(FFrame2, text = "Span: ").pack(side=LEFT)
        B_Span_dec = Button(FFrame2, text = '<', padx = 0,command = lambda : self.ChangeSpan('down') ).pack(side=LEFT)
        self.L_Span = Label(FFrame2, text = str(self.span/6) + 'hrs', relief = SUNKEN, padx= 10, bg='White')
        self.L_Span.pack(side=LEFT)
        B_Span_inc = Button(FFrame2, text = '>', padx = 0, command = lambda : self.ChangeSpan('up')).pack(side=LEFT)



        L_numSamples = Label(FFrame2, text = "  Number of Samples: " + str(len(self.timestamps))).pack(side=LEFT)



        print self.dateStamps

        y = self.Data[0:self.span]
        t = self.timestamps[0 :self.span]

        self.FFigure = plt.figure(figsize=(9,5), dpi = 80)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%H:%M'))
        self.FFigure.add_subplot(111).plot(t,y)
        chart = FigureCanvasTkAgg(self.FFigure, self.FFrame)
        chart.get_tk_widget().grid(row=0,column=0)
        plt.grid()
        plt.gcf().autofmt_xdate()

        self.oldpoint = 0
        self.updateDate()
        self.title = title
        self.labels = ['Dates','Samples']
        self.updateGraph(0)

    def ChangeSpan(self,amount):
        SPH = self.SPH
        if amount=='up':
            if self.span == (SPH * 3):      self.span = SPH * 5
            elif self.span == (SPH * 5):    self.span = SPH * 9
            elif self.span == (SPH * 9):    self.span = SPH * 12
            elif self.span == (SPH * 12):   self.span = SPH * 16
            elif self.span == (SPH * 16):   self.span = SPH * 24
            elif self.span == (SPH * 24):   self.span = SPH * 36
            elif self.span == (SPH * 36):   self.span = SPH * 48
            elif self.span == (SPH * 48):   self.span = SPH * 72
            elif self.span == (SPH * 72):   self.span = SPH * 168
            elif self.span == (SPH * 168):   self.span = SPH * 168
        else:
            if self.span == (SPH * 3):      self.pan = SPH * 3
            elif self.span == (SPH * 5):    self.span = SPH * 3
            elif self.span == (SPH * 9):    self.span = SPH * 5
            elif self.span == (SPH * 12):   self.span = SPH * 9
            elif self.span == (SPH * 16):   self.span = SPH * 12
            elif self.span == (SPH * 24):   self.span = SPH * 16
            elif self.span == (SPH * 36):   self.span = SPH * 24
            elif self.span == (SPH * 48):   self.span = SPH * 36
            elif self.span == (SPH * 72):   self.span = SPH * 48
            elif self.span == (SPH * 168):   self.span = SPH * 72
        self.offsetSpan = int(self.span*0.4)
        self.sections = len(self.timestamps)/self.offsetSpan - self.span/self.offsetSpan
        self.time_slide['to'] = self.sections
        self.L_Span['text'] = str(self.span/6) + 'hrs'
        self.updateGraph(self.time_slide.get())

    def updateGUI(self):
        if self.clicked.get()!=self.oldOption:
            self.updateDate()
            self.oldOption = self.clicked.get()
        else: self.oldOption = self.clicked.get()

        newpoint = self.time_slide.get()
        if self.oldpoint != newpoint:
            self.updateGraph(newpoint)
            self.oldpoint = newpoint
        else: self.oldpoint = newpoint

    def updateDate(self):
        dateInd = []
        for i in range(len(self.dateStamps)):
            if self.dateStamps[i] == self.clicked.get(): dateInd.append(i)
        newoption = (dateInd[-1])/self.offsetSpan - 1
        self.time_slide.set(newoption)
        print newoption

    def updateGraph(self, timeSlide):
        newStart = timeSlide*self.offsetSpan
        newFinal = newStart + self.span +1
        print 'newRange == ' + str(newStart) + '--' + str(newFinal)
        y = self.Data[newStart:newFinal]
        t = self.timestamps[newStart:newFinal]
        self.FFigure.clear()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%H:%M'))
        self.FFigure.add_subplot(111).plot(t, y)
        plt.title(self.title)
        plt.xlabel(self.labels[0])
        plt.ylabel(self.labels[1])
        chart = FigureCanvasTkAgg(self.FFigure, self.FFrame)
        chart.get_tk_widget().grid(row=0, column=0)
        plt.gcf().autofmt_xdate()
        plt.grid()

if __name__ == '__main__':
    dir = sys.path[0] + "/DataOrganization/"

    # load in mesh network
    MainMesh = MeshNetwork(dir)
    MainMesh.loadMesh()
    # initialize GUI
    root = Tk()
    graphPanel = InteractiveGraph(MainMesh,root,0, MainMesh.Motes[0].wind)

    root.after(33, graphPanel.updateGUI)
    root.mainloop()
# root.title("babe survey")

# # import media
# Crying_man = PhotoImage(file = "tenor.gif") # import image
#
# def babeConfirmer():
#     replyButton = "confirmed!!" + " and wow age is " + age.get()
#     LB_confrirmGril= Label(root, text=replyButton ).grid(row = 2, column = 0, columnspan= 3)
#     LP_Cryman = Label(root, image=Crying_man, pady=10).grid(row = 3, column = 0, columnspan= 3)
#     global Count
#     Count += 1
#
# # intro text
# myLabel = Label (root, text = "Hello ").grid(row = 0, column = 0)
# L_Grilask = Label (root, text = "You are ?").grid(row = 1, column = 0)
#
# # button
# B_confirm = Button(root, text = "Confirm baby", padx=20, pady=10, borderwidth=5, command= babeConfirmer).grid(row = 1, column = 1, columnspan= 2)
#
# #input box
# L_askAge = Label (root, text = "Age:").grid(row = 0, column = 1, sticky= E)
# age = Entry(root, width=20, borderwidth=2) #seperate button call and grip placement so you can call button object in other places
# age.grid(row = 0, column = 2)
#
# # dynamic text
# L_confirmCount = Label (root, text = "confirmed " + str(Count) + " times", relief="sunken").grid(row = 4, column = 0, columnspan= 5, sticky= W+E)

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


