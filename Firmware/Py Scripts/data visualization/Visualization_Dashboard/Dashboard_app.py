# Dashboard_app base on python2.7
from __future__ import absolute_import
import Tkinter as tk
import cv2
import read_smartmesh


num = []
TimesList = u""
MotesList = u""


# Making a class frames that easy for us to manage our Pages.
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side=u"top", fill=u"both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ModesPage, Mode1Page, Mode2Page, Mode3Page, Mode4Page):
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
        tk.Frame.__init__(self, parent, bg=u'#4700b3')
        self.controller = controller
        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label1 = tk.Label(self,
                                  text=u'Data Visualization', font=(u"Bauhaus 93", 50), fg=u'white', bg=u'#4700b3')
        heading_label1.pack(pady=100)

        def s_button():
            controller.show_frame(u'ModesPage')

        start_button = tk.Button(self,
                                 text=u'Get Start', font=(u"Eras Demi ITC", 20), bg=u"white", command=s_button,
                                 relief=u'raised', borderwidth=4, width=10, height=2)
        start_button.pack(pady=50)


# The MotesPage is designed for user to choose which mote's data they want
# and also load the data from log when they click one of the load button.
class ModesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#4700b3')
        self.controller = controller
        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label1 = tk.Label(self,
                                  text=u'Data Visualization', font=(u"Bauhaus 93", 50), fg=u'white', bg=u'#4700b3')
        heading_label1.pack(pady=50)

        # Creating frames in oder to manage the window layout.
        mode_button_frame = tk.Frame(self,
                                     bg=u'#4700b3')
        mode_button_frame.pack(expand=True)

        notation_frame = tk.Frame(self,
                                  bg=u'#4700b3')
        notation_frame.pack(fill=u'both', expand=True, anchor=u'nw')

        back_button_frame = tk.Frame(self,
                                     bg=u'#4700b3')
        back_button_frame.pack(fill=u'both', expand=True)

        # Creating "get data" button so that it could switch Page when the user choose on of our mode.
        def get_data():
            print num
            if num[0] == 2:
                controller.show_frame(u'Mode1Page')
            if num[0] == 3:
                controller.show_frame(u'Mode2Page')
            if num[0] == 4:
                controller.show_frame(u'Mode3Page')
            if num[0] == 5:
                controller.show_frame(u'Mode4Page')

        get_data_button = tk.Button(mode_button_frame,
                                    text=u'Get Data', font=(u"Eras Demi ITC", 15), command=get_data,
                                    relief=u'raised', borderwidth=3, width=10, height=1)
        get_data_button.grid(row=1, column=2, pady=20, padx=10)

        # Listbox could show the user what they choose
        choose_label = tk.Label(mode_button_frame,
                                text=u'Motes Choose', font=(u"Eras Demi ITC", 20), fg=u'white', bg=u'#4700b3')
        choose_label.grid(row=0, column=1)

        choose_listbox = tk.Listbox(mode_button_frame,
                                    font=(u"Eras Demi ITC", 15), height=1, width=18)
        choose_listbox.grid(row=1, column=1, pady=20, padx=10)

        # Basically, num[] could save a num that corresponding with each mode,
        # then it could call one of the mode the user choose.
        def mode1():
            del num[:]
            num.append(2)
            choose_listbox.delete(0, 10)
            choose_listbox.insert(u"end", u"Read Mode1 File")

        mote1_button = tk.Button(mode_button_frame,
                                 text=u'Mode 1', font=(u"Eras Demi ITC", 15), command=mode1,
                                 relief=u'raised', borderwidth=4, width=15, height=2)
        mote1_button.grid(row=2, column=0, pady=20, padx=10)

        def mode2():
            del num[:]
            num.append(3)
            choose_listbox.delete(0, 10)
            choose_listbox.insert(u"end", u"Read Mode2 File")

        mote2_button = tk.Button(mode_button_frame,
                                 text=u'Mode 2', font=(u"Eras Demi ITC", 15), command=mode2,
                                 relief=u'raised', borderwidth=4, width=15, height=2)
        mote2_button.grid(row=2, column=1, pady=20, padx=10)

        def mode3():
            del num[:]
            num.append(4)
            choose_listbox.delete(0, 10)
            choose_listbox.insert(u"end", u"Read Mode3 File")

        mote3_button = tk.Button(mode_button_frame,
                                 text=u'Mode 3', font=(u"Eras Demi ITC", 15), command=mode3,
                                 relief=u'raised', borderwidth=4, width=15, height=2)
        mote3_button.grid(row=2, column=2, pady=20, padx=10)

        def mode4():
            del num[:]
            num.append(5)
            choose_listbox.delete(0, 10)
            choose_listbox.insert(u"end", u"Read All Data")

        mote3_button = tk.Button(mode_button_frame,
                                 text=u'Mode 4', font=(u"Eras Demi ITC", 15), command=mode4,
                                 relief=u'raised', borderwidth=4, width=15, height=2)
        mote3_button.grid(row=3, column=1, pady=20, padx=10)

        # Just a notation of the mode buttons.
        notation_label = tk.Label(notation_frame,
                                  text=u'Mode 1 index data through time\n'
                                       u'Mode 2 index data through address\n'
                                       u'Mode 3 index data through time and address\n'
                                       u'Mode 4 index all data from updated log',
                                  font=(u"Eras Demi ITC", 13), fg=u'white', bg=u'#4700b3', justify=u'left')
        notation_label.grid(row=0, column=0, padx=211)

        # Back button could back to the previous page.
        def back():
            controller.show_frame(u'StartPage')

        back_button = tk.Button(back_button_frame,
                                text=u'Back', font=(u"Eras Demi ITC", 15), command=back,
                                relief=u'raised', borderwidth=4, width=10, height=2)
        back_button.grid(row=0, column=0, padx=30)


# This is one of the mote page, it convinces for user to choose which sensors' data they want,
# and also could copy the data and the data graph.
class Mode1Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#4700b3')
        self.controller = controller
        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mode1 Data', font=(u"Bauhaus 93", 40),
                                  fg=u'white', bg=u'#4700b3')
        heading_label2.pack(pady=50)

        # Creating frames in oder to manage the window layout.
        button_frame = tk.Frame(self,
                                bg=u'#4700b3')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self,
                                 bg=u'#4700b3')
        button_frame2.pack(fill=u'both', expand=True)

        # Creating one frames that base on "button_frames" could help to manage a deeper layout.
        text_window = tk.Frame(button_frame,
                               bg=u'#4700b3', pady=10, padx=50)
        text_window.grid(row=0, column=2, rowspan=6, columnspan=2, sticky=u"nsew")

        # Creating a spinbox for user to type a time number,
        # then clicking the get_data button could index the data from read_smartmesh file.
        # For example, 18# (18:00-19:00) or 18#,19# for 2 hours.
        time_box = tk.Spinbox(button_frame,
                              font=(u"Eras Demi ITC", 11), width=15)

        time_box_label = tk.Label(button_frame,
                                  text=u'Time: ', font=(u"Eras Demi ITC", 15), fg=u'white', bg=u'#4700b3')
        time_box_label.grid(row=0, column=0, pady=10, padx=30)
        time_box.grid(row=0, column=1, pady=10, padx=30)

        def get_data():
            print num
            if num[0] == 2:
                text.delete(1.0, u'end')
                for item in read_smartmesh.test2(time_box.get()):
                    text.insert(u'end', item)

        get_data1_button = tk.Button(button_frame2,
                                     text=u'Get Data', font=(u"Eras Demi ITC", 15), command=get_data,
                                     relief=u'raised', borderwidth=3, width=10, height=2)
        get_data1_button.grid(row=0, column=1, pady=15)

        # Setting different sensor buttons allow user to access the graphs which plot from data.
        # Using opencv2 to read the png file from read_smartmesh file, then show them when the user click these buttons.
        def temp_graphing():
            img = cv2.imread(u"Temperature.png")
            cv2.imshow(u"Temperature", img)

        temp_button = tk.Button(button_frame,
                                text=u'Tempeture Graph', font=(u"Eras Demi ITC", 12), command=temp_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        temp_button.grid(row=1, column=0, pady=10, padx=30)

        def hum_graphing():
            img = cv2.imread(u"humidity.png")
            cv2.imshow(u"humidity", img)

        hum_button = tk.Button(button_frame,
                               text=u'Humidity Graph', font=(u"Eras Demi ITC", 12), command=hum_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        hum_button.grid(row=1, column=1, pady=10, padx=10)

        def lig_graphing():
            img = cv2.imread(u"light.png")
            cv2.imshow(u"light", img)

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph', font=(u"Eras Demi ITC", 12), command=lig_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        lig_button.grid(row=2, column=0, pady=10, padx=10)

        def wind_graphing():
            img = cv2.imread(u"windSpeed.png")
            cv2.imshow(u"windSpeed", img)

        wind_button = tk.Button(button_frame,
                                text=u'WindSpeed Graph', font=(u"Eras Demi ITC", 12), command=wind_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        wind_button.grid(row=2, column=1, pady=10, padx=10)

        # Creating x axis and y axis scrollbar.
        scrollbar_y = tk.Scrollbar(text_window)
        scrollbar_x = tk.Scrollbar(text_window,
                                   orient=u'horizontal')
        # Creating a Text box that could show the data even copy the data from it.
        text = tk.Text(text_window,
                       xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set, wrap=u"none",
                       width=75, height=25, font=(u"Times_New_Roman", 10))
        # Connecting the scrollbars and Text box, then packing(grid()) them for showing.
        scrollbar_y.config(command=text.yview)
        scrollbar_y.grid(row=0, column=4, rowspan=6, sticky=u"ns")
        scrollbar_x.config(command=text.xview)
        scrollbar_x.grid(row=6, column=2, columnspan=2, sticky=u"ew")
        text.grid(row=0, column=2, rowspan=6, columnspan=2, pady=5, padx=5)

        # Back button could back to the previous page.
        def back():
            controller.show_frame(u'ModesPage')

        back_button = tk.Button(button_frame2,
                                text=u'Back', font=(u"Eras Demi ITC", 15), command=back,
                                relief=u'raised', borderwidth=3, width=10, height=2)
        back_button.grid(row=0, column=0, pady=15, padx=30)


class Mode2Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#4700b3')
        self.controller = controller
        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mode1 Data', font=(u"Bauhaus 93", 40),
                                  fg=u'white', bg=u'#4700b3')
        heading_label2.pack(pady=50)

        # Creating frames in oder to manage the window layout.
        button_frame = tk.Frame(self,
                                bg=u'#4700b3')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self,
                                 bg=u'#4700b3')
        button_frame2.pack(fill=u'both', expand=True)

        # Creating one frames that base on "button_frames" could help to manage a deeper layout.
        text_window = tk.Frame(button_frame,
                               bg=u'#4700b3', pady=10, padx=50)
        text_window.grid(row=0, column=2, rowspan=6, columnspan=2, sticky=u"nsew")

        # Creating a spinbox for user to type a address,
        # then clicking the get_data button could index the data from read_smartmesh file.
        # For example, (00-17-0d-00-00-32-dc-61)#
        address_box = tk.Spinbox(button_frame,
                                 font=(u"Eras Demi ITC", 11), width=15)

        address_box_label = tk.Label(button_frame,
                                     text=u'Address: ', font=(u"Eras Demi ITC", 15), fg=u'white', bg=u'#4700b3')
        address_box_label.grid(row=0, column=0, pady=10, padx=30)
        address_box.grid(row=0, column=1, pady=10, padx=30)

        def get_data():
            print num
            if num[0] == 3:
                text.delete(1.0, u'end')
                for item in read_smartmesh.test3(address_box.get()):
                    text.insert(u'end', item)

        get_data1_button = tk.Button(button_frame2,
                                     text=u'Get Data', font=(u"Eras Demi ITC", 15), command=get_data,
                                     relief=u'raised', borderwidth=3, width=10, height=2)
        get_data1_button.grid(row=0, column=1, pady=15)

        # Setting different sensor buttons allow user to access the graphs which plot from data.
        # Using opencv2 to read the png file from read_smartmesh file, then show them when the user click these buttons.
        def temp_graphing():
            img = cv2.imread(u"Temperature.png")
            cv2.imshow(u"Temperature", img)

        temp_button = tk.Button(button_frame,
                                text=u'Tempeture Graph', font=(u"Eras Demi ITC", 12), command=temp_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        temp_button.grid(row=1, column=0, pady=10, padx=30)

        def hum_graphing():
            img = cv2.imread("humidity.png")
            cv2.imshow("humidity", img)

        hum_button = tk.Button(button_frame,
                               text='Humidity Graph', font=("Eras Demi ITC", 12), command=hum_graphing,
                               relief='raised', borderwidth=3, width=16, height=4)
        hum_button.grid(row=1, column=1, pady=10, padx=10)

        def lig_graphing():
            img = cv2.imread(u"light.png")
            cv2.imshow(u"light", img)

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph', font=(u"Eras Demi ITC", 12), command=lig_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        lig_button.grid(row=2, column=0, pady=10, padx=10)

        def wind_graphing():
            img = cv2.imread(u"windSpeed.png")
            cv2.imshow(u"windSpeed", img)

        wind_button = tk.Button(button_frame,
                                text=u'WindSpeed Graph', font=(u"Eras Demi ITC", 12), command=wind_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        wind_button.grid(row=2, column=1, pady=10, padx=10)

        # Creating x axis and y axis scrollbar.
        scrollbar_y = tk.Scrollbar(text_window)
        scrollbar_x = tk.Scrollbar(text_window,
                                   orient=u'horizontal')
        # Creating a Text box that could show the data even copy the data from it.
        text = tk.Text(text_window,
                       xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set, wrap=u"none",
                       width=75, height=25, font=(u"Times_New_Roman", 10))
        # Connecting the scrollbars and Text box, then packing(grid()) them for showing.
        scrollbar_y.config(command=text.yview)
        scrollbar_y.grid(row=0, column=4, rowspan=6, sticky=u"ns")
        scrollbar_x.config(command=text.xview)
        scrollbar_x.grid(row=6, column=2, columnspan=2, sticky=u"ew")
        text.grid(row=0, column=2, rowspan=6, columnspan=2, pady=5, padx=5)

        # Back button could back to the previous page.
        def back():
            controller.show_frame(u'ModesPage')

        back_button = tk.Button(button_frame2,
                                text=u'Back', font=(u"Eras Demi ITC", 15), command=back,
                                relief=u'raised', borderwidth=3, width=10, height=2)
        back_button.grid(row=0, column=0, pady=15, padx=30)


class Mode3Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#4700b3')
        self.controller = controller
        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mode1 Data', font=(u"Bauhaus 93", 40),
                                  fg=u'white', bg=u'#4700b3')
        heading_label2.pack(pady=50)

        # Creating frames in oder to manage the window layout.
        button_frame = tk.Frame(self,
                                bg=u'#4700b3')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self,
                                 bg=u'#4700b3')
        button_frame2.pack(fill=u'both', expand=True)

        # Creating one frames that base on "button_frames" could help to manage a deeper layout.
        text_window = tk.Frame(button_frame,
                               bg=u'#4700b3', pady=10, padx=50)
        text_window.grid(row=0, column=2, rowspan=7, columnspan=2, sticky=u"nsew")

        # Creating two spinbox for user to type a time and a address,
        # then clicking the get_data button could index the data from read_smartmesh file.
        # For example, 18#; (00-17-0d-00-00-32-dc-61)#
        time_box = tk.Spinbox(button_frame,
                              font=(u"Eras Demi ITC", 11), width=15)

        time_box_label = tk.Label(button_frame,
                                  text=u'Time: ', font=(u"Eras Demi ITC", 15), fg=u'white', bg=u'#4700b3')
        time_box_label.grid(row=0, column=0, pady=10, padx=30)
        time_box.grid(row=0, column=1, pady=10, padx=30)

        address_box = tk.Spinbox(button_frame,
                                 font=(u"Eras Demi ITC", 11), width=15)

        address_box_label = tk.Label(button_frame,
                                     text=u'Address: ', font=(u"Eras Demi ITC", 15), fg=u'white', bg=u'#4700b3')
        address_box_label.grid(row=1, column=0, pady=10, padx=30)
        address_box.grid(row=1, column=1, pady=10, padx=30)

        def get_data():
            print num
            if num[0] == 4:
                text.delete(1.0, u'end')
                for item in read_smartmesh.test4(time_box.get(), address_box.get()):
                    text.insert(u'end', item)

        get_data1_button = tk.Button(button_frame2,
                                     text=u'Get Data', font=(u"Eras Demi ITC", 15), command=get_data,
                                     relief=u'raised', borderwidth=3, width=10, height=2)
        get_data1_button.grid(row=0, column=1, pady=15)

        # Setting different sensor buttons allow user to access the graphs which plot from data.
        # Using opencv2 to read the png file from read_smartmesh file, then show them when the user click these buttons.
        def temp_graphing():
            img = cv2.imread(u"Temperature.png")
            cv2.imshow(u"Temperature", img)

        temp_button = tk.Button(button_frame,
                                text=u'Tempeture Graph', font=(u"Eras Demi ITC", 12), command=temp_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        temp_button.grid(row=2, column=0, pady=10, padx=30)

        def hum_graphing():
            img = cv2.imread(u"humidity.png")
            cv2.imshow(u"humidity", img)

        hum_button = tk.Button(button_frame,
                               text=u'Humidity Graph', font=(u"Eras Demi ITC", 12), command=hum_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        hum_button.grid(row=2, column=1, pady=10, padx=10)

        def lig_graphing():
            img = cv2.imread(u"light.png")
            cv2.imshow(u"light", img)

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph', font=(u"Eras Demi ITC", 12), command=lig_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        lig_button.grid(row=3, column=0, pady=10, padx=10)

        def wind_graphing():
            img = cv2.imread(u"windSpeed.png")
            cv2.imshow(u"windSpeed", img)

        wind_button = tk.Button(button_frame,
                                text=u'WindSpeed Graph', font=(u"Eras Demi ITC", 12), command=wind_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        wind_button.grid(row=3, column=1, pady=10, padx=10)

        # Creating x axis and y axis scrollbar.
        scrollbar_y = tk.Scrollbar(text_window)
        scrollbar_x = tk.Scrollbar(text_window,
                                   orient=u'horizontal')
        # Creating a Text box that could show the data even copy the data from it.
        text = tk.Text(text_window,
                       xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set, wrap=u"none",
                       width=75, height=25, font=(u"Times_New_Roman", 10))
        # Connecting the scrollbars and Text box, then packing(grid()) them for showing.
        scrollbar_y.config(command=text.yview)
        scrollbar_y.grid(row=0, column=4, rowspan=7, sticky=u"ns")
        scrollbar_x.config(command=text.xview)
        scrollbar_x.grid(row=7, column=2, columnspan=2, sticky=u"ew")
        text.grid(row=0, column=2, rowspan=7, columnspan=2, pady=5, padx=5)

        # Back button could back to the previous page.
        def back():
            controller.show_frame(u'ModesPage')

        back_button = tk.Button(button_frame2,
                                text=u'Back', font=(u"Eras Demi ITC", 15), command=back,
                                relief=u'raised', borderwidth=3, width=10, height=2)
        back_button.grid(row=0, column=0, pady=15, padx=30)


class Mode4Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=u'#4700b3')
        self.controller = controller
        self.controller.title(u"Data Visualization")
        self.controller.geometry(u"1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap(u"agriculture_plants_icon.ico")
        self.controller.configure(bg=u"white")
        self.controller.attributes(u"-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text=u'Data Visualization - Mode1 Data', font=(u"Bauhaus 93", 40),
                                  fg=u'white', bg=u'#4700b3')
        heading_label2.pack(pady=50)

        # Creating frames in oder to manage the window layout.
        button_frame = tk.Frame(self,
                                bg=u'#4700b3')
        button_frame.pack(fill=u'both', expand=True)

        button_frame2 = tk.Frame(self,
                                 bg=u'#4700b3')
        button_frame2.pack(fill=u'both', expand=True)

        # Creating one frames that base on "button_frames" could help to manage a deeper layout.
        text_window = tk.Frame(button_frame,
                               bg=u'#4700b3', pady=10, padx=50)
        text_window.grid(row=0, column=2, rowspan=7, columnspan=2, sticky=u"nsew")

        def get_data():
            print num
            if num[0] == 5:
                text.delete(1.0, u'end')
                for item in read_smartmesh.test1():
                    text.insert(u'end', item)

        get_data1_button = tk.Button(button_frame2,
                                     text=u'Get Data', font=(u"Eras Demi ITC", 15), command=get_data,
                                     relief=u'raised', borderwidth=3, width=10, height=2)
        get_data1_button.grid(row=0, column=1, pady=15)

        # Setting different sensor buttons allow user to access the graphs which plot from data.
        # Using opencv2 to read the png file from read_smartmesh file, then show them when the user click these buttons.
        def temp_graphing():
            img = cv2.imread(u"Temperature.png")
            cv2.imshow(u"Temperature", img)

        temp_button = tk.Button(button_frame,
                                text=u'Tempeture Graph', font=(u"Eras Demi ITC", 12), command=temp_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        temp_button.grid(row=2, column=0, pady=10, padx=30)

        def hum_graphing():
            img = cv2.imread(u"humidity.png")
            cv2.imshow(u"humidity", img)

        hum_button = tk.Button(button_frame,
                               text=u'Humidity Graph', font=(u"Eras Demi ITC", 12), command=hum_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        hum_button.grid(row=2, column=1, pady=10, padx=10)

        def lig_graphing():
            img = cv2.imread(u"light.png")
            cv2.imshow(u"light", img)

        lig_button = tk.Button(button_frame,
                               text=u'Light Graph', font=(u"Eras Demi ITC", 12), command=lig_graphing,
                               relief=u'raised', borderwidth=3, width=16, height=4)
        lig_button.grid(row=3, column=0, pady=10, padx=10)

        def wind_graphing():
            img = cv2.imread(u"windSpeed.png")
            cv2.imshow(u"windSpeed", img)

        wind_button = tk.Button(button_frame,
                                text=u'WindSpeed Graph', font=(u"Eras Demi ITC", 12), command=wind_graphing,
                                relief=u'raised', borderwidth=3, width=16, height=4)
        wind_button.grid(row=3, column=1, pady=10, padx=10)

        # Creating x axis and y axis scrollbar.
        scrollbar_y = tk.Scrollbar(text_window)
        scrollbar_x = tk.Scrollbar(text_window,
                                   orient=u'horizontal')
        # Creating a Text box that could show the data even copy the data from it.
        text = tk.Text(text_window,
                       xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set, wrap=u"none",
                       width=75, height=25, font=(u"Times_New_Roman", 10))
        # Connecting the scrollbars and Text box, then packing(grid()) them for showing.
        scrollbar_y.config(command=text.yview)
        scrollbar_y.grid(row=0, column=4, rowspan=7, sticky=u"ns")
        scrollbar_x.config(command=text.xview)
        scrollbar_x.grid(row=7, column=2, columnspan=2, sticky=u"ew")
        text.grid(row=0, column=2, rowspan=7, columnspan=2, pady=5, padx=5)

        # Back button could back to the previous page.
        def back():
            controller.show_frame(u'ModesPage')

        back_button = tk.Button(button_frame2,
                                text=u'Back', font=(u"Eras Demi ITC", 15), command=back,
                                relief=u'raised', borderwidth=3, width=10, height=2)
        back_button.grid(row=0, column=0, pady=15, padx=30)


if __name__ == u"__main__":
    app = SampleApp()
    app.mainloop()
