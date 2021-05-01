# DV_Presentation Part base on python2.7
from __future__ import absolute_import
import Tkinter as tk
import cv2
import numpy as np


# Making a class frames that easy for us to manage our Pages.
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side=u"top", fill=u"both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MotesPage, Mote1Page, Mote2Page, Mote3Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky=u"nsew")

        self.show_frame(u"StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


# The StartPage is designed to load our update log file.
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = u'#b3d9ff')
        self.controller = controller

        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg= u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label1 = tk.Label(self,
                                 text = u'Data Visualization',
                                 font = (u"Times_New_Roman 30"),
                                 fg = u'black',
                                 bg = u'#b3d9ff')
        heading_label1.pack(pady= 50)

        def s_button():
            controller.show_frame(u'MotesPage')

        start_button = tk.Button(self,
                                 text=u'Get Start',
                                 font=(u"Times_New_Roman 15"),
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 30,
                                 height = 3,
                                 command=s_button)
        start_button.pack(pady= 50)


# The MotesPage is designed for user to choose which mote's data they want
# and also load the data from log when they click one of the load button.
class MotesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#b3d9ff')
        self.controller = controller

        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label1 = tk.Label(self,
                                  text=u'Data Visualization',
                                  font=(u"Times_New_Roman 30"),
                                  fg=u'black',
                                  bg=u'#b3d9ff')
        heading_label1.pack(pady=50)

        motes_label = tk.Label(self,
                               text=u'Motes Choose',
                               font=(u"Times_New_Roman 20"),
                               fg=u'black',
                               bg=u'#b3d9ff'
                               )
        motes_label.pack()

        button_frame = tk.Frame(self, bg = u'#b3d9ff')
        button_frame.pack(expand = True)

        button_frame2 = tk.Frame(self, bg=u'#b3d9ff')
        button_frame2.pack(fill = u'both', expand = True)

        def mote1():
            controller.show_frame(u'Mote1Page')

        mote1_button = tk.Button(button_frame,
                                 text = u'Mote1',
                                 font=(u"Times_New_Roman 15"),
                                 command = mote1,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 20,
                                 height = 4,
                                 )
        mote1_button.grid(row = 0, column= 0, pady = 20, padx = 10)

        def mote2():
            controller.show_frame(u'Mote2Page')

        mote2_button = tk.Button(button_frame,
                                 text = u'Mote2',
                                 font=(u"Times_New_Roman 15"),
                                 command = mote2,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 20,
                                 height = 4)
        mote2_button.grid(row = 0, column= 1, pady = 20, padx = 10)

        def mote3():
            controller.show_frame(u'Mote3Page')

        mote3_button = tk.Button(button_frame,
                                 text = u'Mote3',
                                 font=(u"Times_New_Roman 15"),
                                 command = mote3,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 20,
                                 height = 4)
        mote3_button.grid(row = 0, column= 2, pady = 20, padx = 10)

        def back1():
            controller.show_frame(u'StartPage')

        back1_button = tk.Button(button_frame2,
                                 text = u'Back',
                                 font=(u"Times_New_Roman 15"),
                                 command = back1,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 300, padx = 10)


# This is one of the mote page, it convinces for user to choose which sensors' data they want,
# and also could copy the data and the data graph.
class Mote1Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#b3d9ff')
        self.controller = controller

        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mote1 Data',
                                  font=(u"Times_New_Roman 20"),
                                  fg=u'black',
                                  bg=u'#b3d9ff')
        heading_label2.pack(pady=50)


        button_frame = tk.Frame(self, bg=u'#b3d9ff')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self, bg=u'#b3d9ff')
        button_frame2.pack(fill = u'both', expand = True)

        # Making a plot function in here, then plot the data graph by time
        def temp_function(x):
            pass

        def open_temp():
            img = cv2.imread('plot_show.png')
            cv2.namedWindow('Tempeture data graph')
            cv2.imshow('Tempeture data graph', img)
            cv2.createTrackbar('Time','Tempeture data graph',0,5, temp_function )
            cv2.waitKey(0)
            cv2.destroyAllWindows()



        temp_button = tk.Button(button_frame,
                                text = u'Tempeture Graph',
                                font=(u"Times_New_Roman 12"),
                                relief = u'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4,
                                command = open_temp)
        temp_button.grid(row = 0, column = 0, pady = 10, padx = 30)

        def hum():
            pass

        hum_button = tk.Button(button_frame,
                                text = u'Humidity Graph',
                                font=(u"Times_New_Roman 12"),
                                command = hum,
                                relief = u'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        hum_button.grid(row = 0, column = 1, pady = 10, padx = 10)

        def lig():
            pass

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph',
                               font=(u"Times_New_Roman 12"),
                               command=hum,
                               relief=u'raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        lig_button.grid(row=1, column=0, pady=10, padx=10)

        def vib():
            pass

        vib_button = tk.Button(button_frame,
                               text=u'Vibration Graph',
                               font=(u"Times_New_Roman 12"),
                               command=hum,
                               relief=u'raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        vib_button.grid(row=1, column=1, pady=10, padx=10)


        def back1():
            controller.show_frame(u'MotesPage')

        back1_button = tk.Button(button_frame2,
                                 text = u'Back',
                                 font=(u"Times_New_Roman 15"),
                                 command = back1,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 10, padx = 10)

        text_window = tk.Frame(button_frame, pady =10, padx = 50)
        text_window.configure(bg = u'#b3d9ff')
        text_window.grid(row=0, column=2, rowspan = 6, columnspan = 2, sticky = u"nsew")

        text = tk.Text(text_window, width = 50, height = 20, font = (u"Times_New_Roman 15"))
        text.grid(row=0, column=2, rowspan = 6, columnspan = 2, pady = 5, padx = 5)

        scrollbar = tk.Scrollbar(text_window, command = text.yview)
        text[u'yscroll'] = scrollbar.set
        scrollbar.grid(row=0, column=4, rowspan = 6, sticky = u"ns")

        data_log = u"""xxx"""

        text.insert(tk.INSERT,data_log)



class Mote2Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#b3d9ff')
        self.controller = controller

        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mote2 Data',
                                  font=(u"Times_New_Roman 20"),
                                  fg=u'black',
                                  bg=u'#b3d9ff')
        heading_label2.pack(pady=50)


        button_frame = tk.Frame(self, bg=u'#b3d9ff')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self, bg=u'#b3d9ff')
        button_frame2.pack(fill = u'both', expand = True)

        def temp():
            pass

        temp_button = tk.Button(button_frame,
                                text = u'Tempeture Graph',
                                font=(u"Times_New_Roman 12"),
                                command = temp,
                                relief = u'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        temp_button.grid(row = 0, column = 0, pady = 10, padx = 30)

        def hum():
            pass

        hum_button = tk.Button(button_frame,
                                text = u'Humidity Graph',
                                font=(u"Times_New_Roman 12"),
                                command = hum,
                                relief = u'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        hum_button.grid(row = 0, column = 1, pady = 10, padx = 10)

        def lig():
            pass

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph',
                               font=(u"Times_New_Roman 12"),
                               command=hum,
                               relief=u'raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        lig_button.grid(row=1, column=0, pady=10, padx=10)

        def vib():
            pass

        vib_button = tk.Button(button_frame,
                               text=u'Vibration Graph',
                               font=(u"Times_New_Roman 12"),
                               command=hum,
                               relief=u'raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        vib_button.grid(row=1, column=1, pady=10, padx=10)


        def back1():
            controller.show_frame(u'MotesPage')

        back1_button = tk.Button(button_frame2,
                                 text = u'Back',
                                 font=(u"Times_New_Roman 15"),
                                 command = back1,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 10, padx = 10)

        text_window = tk.Frame(button_frame, pady =10, padx = 50)
        text_window.configure(bg = u'#b3d9ff')
        text_window.grid(row=0, column=2, rowspan = 6, columnspan = 2, sticky = u"nsew")

        text = tk.Text(text_window, width = 50, height = 20, font = (u"Times_New_Roman 15"))
        text.grid(row=0, column=2, rowspan = 6, columnspan = 2, pady = 5, padx = 5)

        scrollbar = tk.Scrollbar(text_window, command = text.yview)
        text[u'yscroll'] = scrollbar.set
        scrollbar.grid(row=0, column=4, rowspan = 6, sticky = u"ns")

        data_log = u"""xxx"""

        text.insert(tk.INSERT,data_log)


class Mote3Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#b3d9ff')
        self.controller = controller

        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mote3 Data',
                                  font=(u"Times_New_Roman 20"),
                                  fg=u'black',
                                  bg=u'#b3d9ff')
        heading_label2.pack(pady=50)


        button_frame = tk.Frame(self, bg=u'#b3d9ff')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self, bg=u'#b3d9ff')
        button_frame2.pack(fill = u'both', expand = True)

        def temp():
            pass

        temp_button = tk.Button(button_frame,
                                text = u'Tempeture Graph',
                                font=(u"Times_New_Roman 12"),
                                command = temp,
                                relief = u'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        temp_button.grid(row = 0, column = 0, pady = 10, padx = 30)

        def hum():
            pass

        hum_button = tk.Button(button_frame,
                                text = u'Humidity Graph',
                                font=(u"Times_New_Roman 12"),
                                command = hum,
                                relief = u'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        hum_button.grid(row = 0, column = 1, pady = 10, padx = 10)

        def lig():
            pass

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph',
                               font=(u"Times_New_Roman 12"),
                               command=hum,
                               relief=u'raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        lig_button.grid(row=1, column=0, pady=10, padx=10)

        def vib():
            pass

        vib_button = tk.Button(button_frame,
                               text=u'Vibration Graph',
                               font=(u"Times_New_Roman 12"),
                               command=hum,
                               relief=u'raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        vib_button.grid(row=1, column=1, pady=10, padx=10)


        def back1():
            controller.show_frame(u'MotesPage')

        back1_button = tk.Button(button_frame2,
                                 text = u'Back',
                                 font=(u"Times_New_Roman 15"),
                                 command = back1,
                                 relief = u'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 10, padx = 10)

        text_window = tk.Frame(button_frame, pady =10, padx = 50)
        text_window.configure(bg = u'#b3d9ff')
        text_window.grid(row=0, column=2, rowspan = 6, columnspan = 2, sticky = u"nsew")

        text = tk.Text(text_window, width = 50, height = 20, font = (u"Times_New_Roman 15"))
        text.grid(row=0, column=2, rowspan = 6, columnspan = 2, pady = 5, padx = 5)

        scrollbar = tk.Scrollbar(text_window, command = text.yview)
        text[u'yscroll'] = scrollbar.set
        scrollbar.grid(row=0, column=4, rowspan = 6, sticky = u"ns")

        data_log = u"""xxx"""

        text.insert(tk.INSERT,data_log)





if __name__ == u"__main__":
    app = SampleApp()
    app.mainloop()