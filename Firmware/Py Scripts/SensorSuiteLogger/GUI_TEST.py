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

root.mainloop()