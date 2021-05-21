try:
    from Tkinter import *
except:
    from tkinter import *

dir = sys.path[0] + "/DataOrganization/"
# initialize GUI
root = Tk();
root.title("Sensor Suite Data Viewer")
#root.iconbitmap('')
root.geometry("500x1000")

Frame_Setup = LabelFrame(root, text = 'setup',relief = GROOVE, padx=10, pady=10)
Frame_Setup.pack(side=TOP, expand=True)

Lab_Directory = Label (Frame_Setup,
                       text = "Directory:  {directory}".format( directory = dir[0:10]+ "..." + dir[-30:-1])
                       ).grid(row = 0, column = 0, columnspan= 2)

Lab_ChangeDir = Label(Frame_Setup, text = "Change Directory: ").grid(row = 1, column = 0)
In_dir = Entry(Frame_Setup, width=50, borderwidth=2) #seperate button call and grip placement so you can call button object in other places
In_dir.grid(row = 1, column = 1)

Frame_Motes = LabelFrame(root, text = 'setup',relief = GROOVE, padx=10, pady=10)
Frame_Motes.pack(side=TOP, expand=True)
Lab_moteTable = Label (Frame_Motes, text = "Motes").pack()



# PACKING
Lab_Directory
Lab_ChangeDir
In_dir.
root.mainloop()