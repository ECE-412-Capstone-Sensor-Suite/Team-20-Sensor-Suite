import tkinter as tk     # python 2
import time

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MotesPage, Mote1Page, Mote2Page, Mote3Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#b3d9ff')
        self.controller = controller

        self.controller.title("Data Visualization")
        self.controller.geometry("1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap("agriculture_plants_icon.ico")
        self.controller.configure(bg= "white")
        self.controller.attributes("-topmost", 1)

        heading_label1 = tk.Label(self,
                                 text = 'Data Visualization',
                                 font = ("Times_New_Roman 30"),
                                 fg = 'black',
                                 bg = '#b3d9ff')
        heading_label1.pack(pady = 50)

        def s_button():
            controller.show_frame('MotesPage')

        start_button = tk.Button(self,
                                 text = 'Get Start',
                                 font=("Times_New_Roman 15"),
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 30,
                                 height = 3,
                                 command=s_button)
        start_button.pack(pady= 50)


class MotesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#b3d9ff')
        self.controller = controller

        self.controller.title("Data Visualization")
        self.controller.geometry("1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap("agriculture_plants_icon.ico")
        self.controller.configure(bg="white")
        self.controller.attributes("-topmost", 1)

        heading_label1 = tk.Label(self,
                                  text='Data Visualization',
                                  font=("Times_New_Roman 30"),
                                  fg='black',
                                  bg='#b3d9ff')
        heading_label1.pack(pady=50)

        motes_label = tk.Label(self,
                               text='Motes Choose',
                               font=("Times_New_Roman 20"),
                               fg='black',
                               bg='#b3d9ff'
                               )
        motes_label.pack()

        button_frame = tk.Frame(self, bg = '#b3d9ff')
        button_frame.pack(expand = True)

        button_frame2 = tk.Frame(self, bg='#b3d9ff')
        button_frame2.pack(fill = 'both', expand = True)

        def mote1():
            controller.show_frame('Mote1Page')

        mote1_button = tk.Button(button_frame,
                                 text = 'Mote1',
                                 font=("Times_New_Roman 15"),
                                 command = mote1,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 20,
                                 height = 4,
                                 )
        mote1_button.grid(row = 0, column= 0, pady = 20, padx = 10)

        def mote2():
            controller.show_frame('Mote2Page')

        mote2_button = tk.Button(button_frame,
                                 text = 'Mote2',
                                 font=("Times_New_Roman 15"),
                                 command = mote2,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 20,
                                 height = 4)
        mote2_button.grid(row = 0, column= 1, pady = 20, padx = 10)

        def mote3():
            controller.show_frame('Mote3Page')

        mote3_button = tk.Button(button_frame,
                                 text = 'Mote3',
                                 font=("Times_New_Roman 15"),
                                 command = mote3,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 20,
                                 height = 4)
        mote3_button.grid(row = 0, column= 2, pady = 20, padx = 10)

        def back1():
            controller.show_frame('StartPage')

        back1_button = tk.Button(button_frame2,
                                 text = 'Back',
                                 font=("Times_New_Roman 15"),
                                 command = back1,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 300, padx = 10)

class Mote1Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#b3d9ff')
        self.controller = controller

        self.controller.title("Data Visualization")
        self.controller.geometry("1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap("agriculture_plants_icon.ico")
        self.controller.configure(bg="white")
        self.controller.attributes("-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text='Data Visualization - Mote1 Data',
                                  font=("Times_New_Roman 20"),
                                  fg='black',
                                  bg='#b3d9ff')
        heading_label2.pack(pady=50)


        button_frame = tk.Frame(self, bg='#b3d9ff')
        button_frame.pack(fill='both', expand=True)

        button_frame2 = tk.Frame(self, bg='#b3d9ff')
        button_frame2.pack(fill = 'both', expand = True)

        def temp():
            pass

        temp_button = tk.Button(button_frame,
                                text = 'Tempeture Graph',
                                font=("Times_New_Roman 12"),
                                command = temp,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        temp_button.grid(row = 0, column = 0, pady = 10, padx = 30)

        def hum():
            pass

        hum_button = tk.Button(button_frame,
                                text = 'Humidity Graph',
                                font=("Times_New_Roman 12"),
                                command = hum,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        hum_button.grid(row = 0, column = 1, pady = 10, padx = 10)

        def lig():
            pass

        lig_button = tk.Button(button_frame,
                               text='Light Graph',
                               font=("Times_New_Roman 12"),
                               command=hum,
                               relief='raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        lig_button.grid(row=1, column=0, pady=10, padx=10)

        def vib():
            pass

        vib_button = tk.Button(button_frame,
                               text='Vibration Graph',
                               font=("Times_New_Roman 12"),
                               command=hum,
                               relief='raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        vib_button.grid(row=1, column=1, pady=10, padx=10)


        def back1():
            controller.show_frame('MotesPage')

        back1_button = tk.Button(button_frame2,
                                 text = 'Back',
                                 font=("Times_New_Roman 15"),
                                 command = back1,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 10, padx = 10)

        text_window = tk.Frame(button_frame, pady =10, padx = 50)
        text_window.configure(bg = '#b3d9ff')
        text_window.grid(row=0, column=2, rowspan = 6, columnspan = 2, sticky = "nsew")

        text = tk.Text(text_window, width = 50, height = 20, font = ("Times_New_Roman 15"))
        text.grid(row=0, column=2, rowspan = 6, columnspan = 2, pady = 5, padx = 5)

        scrollbar = tk.Scrollbar(text_window, command = text.yview)
        text['yscroll'] = scrollbar.set
        scrollbar.grid(row=0, column=4, rowspan = 6, sticky = "ns")

        data_log = """Friedrich Wilhelm Nietzsche, 
        15 October 1844 – 25 August 1900) was a German philosopher, 
        cultural critic, composer, poet, writer, and philologist 
        whose work has exerted a profound influence on modern intellectual history.
        He began his career as a classical philologist before turning to philosophy. 
        He became the youngest person ever to hold the Chair of Classical Philology 
        at the University of Basel in 1869 at the age of 24.[44] Nietzsche resigned in 1879 
        due to health problems that plagued him most of his life; he completed much of his core writing 
        in the following decade.[45] In 1889, at age 44, he suffered a collapse 
        and afterward a complete loss of his mental faculties. He lived his remaining years 
        in the care of his mother until her death in 1897 and then with his sister Elisabeth Förster-Nietzsche. 
        Nietzsche died in 1900.
        Nietzsche's writing spans philosophical polemics, poetry, cultural criticism, 
        and fiction while displaying a fondness for aphorism and irony.[47] Prominent elements of his philosophy 
        include his radical critique of truth in favor of perspectivism; a genealogical critique of religion 
        and Christian morality and related theory of master–slave morality;[40][48][i] the aesthetic affirmation of life 
        in response to both the "death of God" and the profound crisis of nihilism;[40] the notion of Apollonian 
        and Dionysian forces; and a characterization of the human subject as the expression of competing wills, 
        collectively understood as the will to power.[49] He also developed influential concepts such as the Übermensch 
        and the doctrine of eternal return.[50][51] In his later work, he became increasingly preoccupied 
        with the creative powers of the individual to overcome cultural and moral mores in pursuit of new values 
        and aesthetic health.[43] His body of work touched a wide range of topics, including art, philology, history, 
        religion, tragedy, culture, and science, and drew inspiration from figures such as Socrates, Zoroaster, 
        Arthur Schopenhauer,[23] Ralph Waldo Emerson, Richard Wagner[23] and Johann Wolfgang von Goethe."""

        text.insert(tk.INSERT,data_log)



class Mote2Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#b3d9ff')
        self.controller = controller

        self.controller.title("Data Visualization")
        self.controller.geometry("1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap("agriculture_plants_icon.ico")
        self.controller.configure(bg="white")
        self.controller.attributes("-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text='Data Visualization - Mote2 Data',
                                  font=("Times_New_Roman 20"),
                                  fg='black',
                                  bg='#b3d9ff')
        heading_label2.pack(pady=50)


        button_frame = tk.Frame(self, bg='#b3d9ff')
        button_frame.pack(fill='both', expand=True)

        button_frame2 = tk.Frame(self, bg='#b3d9ff')
        button_frame2.pack(fill = 'both', expand = True)

        def temp():
            pass

        temp_button = tk.Button(button_frame,
                                text = 'Tempeture Graph',
                                font=("Times_New_Roman 12"),
                                command = temp,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        temp_button.grid(row = 0, column = 0, pady = 10, padx = 30)

        def hum():
            pass

        hum_button = tk.Button(button_frame,
                                text = 'Humidity Graph',
                                font=("Times_New_Roman 12"),
                                command = hum,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        hum_button.grid(row = 0, column = 1, pady = 10, padx = 10)

        def lig():
            pass

        lig_button = tk.Button(button_frame,
                               text='Light Graph',
                               font=("Times_New_Roman 12"),
                               command=hum,
                               relief='raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        lig_button.grid(row=1, column=0, pady=10, padx=10)

        def vib():
            pass

        vib_button = tk.Button(button_frame,
                               text='Vibration Graph',
                               font=("Times_New_Roman 12"),
                               command=hum,
                               relief='raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        vib_button.grid(row=1, column=1, pady=10, padx=10)


        def back1():
            controller.show_frame('MotesPage')

        back1_button = tk.Button(button_frame2,
                                 text = 'Back',
                                 font=("Times_New_Roman 15"),
                                 command = back1,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 10, padx = 10)

        text_window = tk.Frame(button_frame, pady =10, padx = 50)
        text_window.configure(bg = '#b3d9ff')
        text_window.grid(row=0, column=2, rowspan = 6, columnspan = 2, sticky = "nsew")

        text = tk.Text(text_window, width = 50, height = 20, font = ("Times_New_Roman 15"))
        text.grid(row=0, column=2, rowspan = 6, columnspan = 2, pady = 5, padx = 5)

        scrollbar = tk.Scrollbar(text_window, command = text.yview)
        text['yscroll'] = scrollbar.set
        scrollbar.grid(row=0, column=4, rowspan = 6, sticky = "ns")

        data_log = """Friedrich Wilhelm Nietzsche, 
        15 October 1844 – 25 August 1900) was a German philosopher, 
        cultural critic, composer, poet, writer, and philologist 
        whose work has exerted a profound influence on modern intellectual history.
        He began his career as a classical philologist before turning to philosophy. 
        He became the youngest person ever to hold the Chair of Classical Philology 
        at the University of Basel in 1869 at the age of 24.[44] Nietzsche resigned in 1879 
        due to health problems that plagued him most of his life; he completed much of his core writing 
        in the following decade.[45] In 1889, at age 44, he suffered a collapse 
        and afterward a complete loss of his mental faculties. He lived his remaining years 
        in the care of his mother until her death in 1897 and then with his sister Elisabeth Förster-Nietzsche. 
        Nietzsche died in 1900.
        Nietzsche's writing spans philosophical polemics, poetry, cultural criticism, 
        and fiction while displaying a fondness for aphorism and irony.[47] Prominent elements of his philosophy 
        include his radical critique of truth in favor of perspectivism; a genealogical critique of religion 
        and Christian morality and related theory of master–slave morality;[40][48][i] the aesthetic affirmation of life 
        in response to both the "death of God" and the profound crisis of nihilism;[40] the notion of Apollonian 
        and Dionysian forces; and a characterization of the human subject as the expression of competing wills, 
        collectively understood as the will to power.[49] He also developed influential concepts such as the Übermensch 
        and the doctrine of eternal return.[50][51] In his later work, he became increasingly preoccupied 
        with the creative powers of the individual to overcome cultural and moral mores in pursuit of new values 
        and aesthetic health.[43] His body of work touched a wide range of topics, including art, philology, history, 
        religion, tragedy, culture, and science, and drew inspiration from figures such as Socrates, Zoroaster, 
        Arthur Schopenhauer,[23] Ralph Waldo Emerson, Richard Wagner[23] and Johann Wolfgang von Goethe."""

        text.insert(tk.INSERT,data_log)


class Mote3Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#b3d9ff')
        self.controller = controller

        self.controller.title("Data Visualization")
        self.controller.geometry("1080x720")
        self.controller.maxsize(1080, 720)
        self.controller.minsize(1080, 720)
        self.controller.iconbitmap("agriculture_plants_icon.ico")
        self.controller.configure(bg="white")
        self.controller.attributes("-topmost", 1)

        heading_label2 = tk.Label(self,
                                  text='Data Visualization - Mote3 Data',
                                  font=("Times_New_Roman 20"),
                                  fg='black',
                                  bg='#b3d9ff')
        heading_label2.pack(pady=50)


        button_frame = tk.Frame(self, bg='#b3d9ff')
        button_frame.pack(fill='both', expand=True)

        button_frame2 = tk.Frame(self, bg='#b3d9ff')
        button_frame2.pack(fill = 'both', expand = True)

        def temp():
            pass

        temp_button = tk.Button(button_frame,
                                text = 'Tempeture Graph',
                                font=("Times_New_Roman 12"),
                                command = temp,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        temp_button.grid(row = 0, column = 0, pady = 10, padx = 30)

        def hum():
            pass

        hum_button = tk.Button(button_frame,
                                text = 'Humidity Graph',
                                font=("Times_New_Roman 12"),
                                command = hum,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 16,
                                height = 4)
        hum_button.grid(row = 0, column = 1, pady = 10, padx = 10)

        def lig():
            pass

        lig_button = tk.Button(button_frame,
                               text='Light Graph',
                               font=("Times_New_Roman 12"),
                               command=hum,
                               relief='raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        lig_button.grid(row=1, column=0, pady=10, padx=10)

        def vib():
            pass

        vib_button = tk.Button(button_frame,
                               text='Vibration Graph',
                               font=("Times_New_Roman 12"),
                               command=hum,
                               relief='raised',
                               borderwidth=3,
                               width=16,
                               height=4)
        vib_button.grid(row=1, column=1, pady=10, padx=10)


        def back1():
            controller.show_frame('MotesPage')

        back1_button = tk.Button(button_frame2,
                                 text = 'Back',
                                 font=("Times_New_Roman 15"),
                                 command = back1,
                                 relief = 'raised',
                                 borderwidth = 3,
                                 width = 10,
                                 height = 2)
        back1_button.grid(row = 0, column= 0, pady = 10, padx = 10)

        text_window = tk.Frame(button_frame, pady =10, padx = 50)
        text_window.configure(bg = '#b3d9ff')
        text_window.grid(row=0, column=2, rowspan = 6, columnspan = 2, sticky = "nsew")

        text = tk.Text(text_window, width = 50, height = 20, font = ("Times_New_Roman 15"))
        text.grid(row=0, column=2, rowspan = 6, columnspan = 2, pady = 5, padx = 5)

        scrollbar = tk.Scrollbar(text_window, command = text.yview)
        text['yscroll'] = scrollbar.set
        scrollbar.grid(row=0, column=4, rowspan = 6, sticky = "ns")

        data_log = """Friedrich Wilhelm Nietzsche, 
        15 October 1844 – 25 August 1900) was a German philosopher, 
        cultural critic, composer, poet, writer, and philologist 
        whose work has exerted a profound influence on modern intellectual history.
        He began his career as a classical philologist before turning to philosophy. 
        He became the youngest person ever to hold the Chair of Classical Philology 
        at the University of Basel in 1869 at the age of 24.[44] Nietzsche resigned in 1879 
        due to health problems that plagued him most of his life; he completed much of his core writing 
        in the following decade.[45] In 1889, at age 44, he suffered a collapse 
        and afterward a complete loss of his mental faculties. He lived his remaining years 
        in the care of his mother until her death in 1897 and then with his sister Elisabeth Förster-Nietzsche. 
        Nietzsche died in 1900.
        Nietzsche's writing spans philosophical polemics, poetry, cultural criticism, 
        and fiction while displaying a fondness for aphorism and irony.[47] Prominent elements of his philosophy 
        include his radical critique of truth in favor of perspectivism; a genealogical critique of religion 
        and Christian morality and related theory of master–slave morality;[40][48][i] the aesthetic affirmation of life 
        in response to both the "death of God" and the profound crisis of nihilism;[40] the notion of Apollonian 
        and Dionysian forces; and a characterization of the human subject as the expression of competing wills, 
        collectively understood as the will to power.[49] He also developed influential concepts such as the Übermensch 
        and the doctrine of eternal return.[50][51] In his later work, he became increasingly preoccupied 
        with the creative powers of the individual to overcome cultural and moral mores in pursuit of new values 
        and aesthetic health.[43] His body of work touched a wide range of topics, including art, philology, history, 
        religion, tragedy, culture, and science, and drew inspiration from figures such as Socrates, Zoroaster, 
        Arthur Schopenhauer,[23] Ralph Waldo Emerson, Richard Wagner[23] and Johann Wolfgang von Goethe."""

        text.insert(tk.INSERT,data_log)





if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()