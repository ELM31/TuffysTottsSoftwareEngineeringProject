import tkinter as tk                                #tkinter library for GUI
from tkinter import *                   
import time                                         #For current date 
import WindowSet                                    #Sets tool window dimensions off of current screen

#Declarations of Global varibles 
twenties = 0
tens = 0
fives = 0
ones = 0

quarters = 0.0
dimes = 0.0
nickels = 0.0
pennies =0.0

LR = 0.0
the_float = 0.0
total_p = 0.0
crd = 0.0
exp = 0.0 

cash = 0.0
summ = 0.0
diff = 0.0
dep = 0.0
total = 0.0

#univerasal font for widgets 
theFont = "arial"

#String variables for dollar, coin and closing frame widgets
inputBackground = '#343434'
inputForeground = '#ebebeb'
entryBackground = '#4d4d4d'
entryForeground = '#35aeea'
#String varibles for output frame widgets 
outputBackground = '#363636'
outputForeground = '#35aeea'
textBoxBackground = '#101010'
texBoxForeground = '#ebebeb'

#function to calculate cash and display to the cash textbox 
def calculate_cash():
    global cash, twenties, tens, fives, ones, quarters, dimes, nickels, pennies

    twenties = int(twenties_entry.get())
    tens = int(tens_entry.get())
    fives = int(fives_entry.get())
    ones = int(ones_entry.get())
    quarters = float(quarter_entry.get())
    dimes = float(dimes_entry.get())
    nickels = float(nickels_entry.get())
    pennies = float(pennies_entry.get())

    cash = round((twenties + tens + fives + ones + quarters + dimes + nickels + pennies),2)

    cash_text.delete("1.0", tk.END)
    cash_text.insert("1.0",str(cash))

#function to calculate sum and display to the sum textbox 
def calculate_sum():
    global cash, summ, exp, crd
    exp = int(expense_entry.get())
    crd = int(credit_entry.get())

    summ = round((exp + crd + cash),2)

    sum_text.delete("1.0", tk.END)
    sum_text.insert("1.0",str(summ))

#function to calculate difference and display to the difference textbox. As well as total and deposit 
def calculate_rest():
    global summ, total_p ,total, diff, the_float, twenties

    total_p = float(TP_entry.get()) 
    the_float = float(TheFloat_entry.get())
    total = total_p + the_float

    diff =  round((summ - total),2)

    total_text.delete("1.0", tk.END)
    total_text.insert("1.0",str(total))

    diff_text.delete("1.0", tk.END)
    diff_text.insert("1.0",str(diff))

    dep_text.delete("1.0", tk.END)
    dep_text.insert("1.0",str(twenties))
    

#function for the calculate command to use
def calculate():
    calculate_cash()
    calculate_sum()
    calculate_rest()


# Tkinter GUI Setup
global result_label, huffman_codes_text, decoded_text_display

#root
root = tk.Tk()
root.title("Tuffy's Closing Buddy")
root.configure(bg = '#101010')

#dynamically set screen to form fit depending on what window screen is used 
WindowSet.setScreen(root, wRatio = 0.24, hRatio = 0.63) # Dynamically sets window size for program

#declaration of all of the frames used 
dollar_frame  = Frame(root, bg='#343434')
coin_frame = Frame(root, bg='#343434')
closing_frame =  Frame(root, bg= '#343434')
output_frame = Frame(root, bg= '#343434' )

#grid of each of the frames to fit nicely
dollar_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
coin_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
closing_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)
output_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew", columnspan= 2)

name_label = Label(root,
                   text = "Tuffy's Closing Buddy",
                   bg= outputBackground, fg = outputForeground,
                    font=("Fixedsys", 20))
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

#Label and entry for the 20 dollar bills 
twenties_labels = Label(dollar_frame, 
                         text="20 dollar bill", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
twenties_labels.grid(row=0, column=0, padx=0, pady=5, sticky="e")
twenties_entry = Entry(dollar_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT)
twenties_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

#Label and entry for the 10 dollar bills 
tens_label = Label(dollar_frame, 
                         text="10 dollar bill", 
                         fg=inputForeground,bg=inputBackground,
                         font=(theFont, 10))
tens_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
tens_entry = Entry(dollar_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
tens_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the 5 dollar bills 
fives_label = Label(dollar_frame, 
                         text="5 dollar bill", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
fives_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
fives_entry = Entry(dollar_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
fives_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the 1 dollar bills 
ones_label = Label(dollar_frame, 
                         text="1 dollar bill", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
ones_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
ones_entry = Entry(dollar_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont, 10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
ones_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the quarters 
quarter_label = Label(coin_frame, 
                         text="Quarters", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
quarter_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
quarter_entry = Entry(coin_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
quarter_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the dimes 
dimes_label = Label(coin_frame, 
                         text="Dimes   ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
dimes_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
dimes_entry = Entry(coin_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
dimes_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the Nickels 
nickels_label = Label(coin_frame, 
                         text="Nickels ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
nickels_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
nickels_entry = Entry(coin_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
nickels_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the Pennies 
pennies_label = Label(coin_frame, 
                         text="Pennies ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
pennies_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
pennies_entry = Entry(coin_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=5,
                          borderwidth=0, 
                          justify=RIGHT  )
pennies_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")


#Label and entry for the Labor report  
LR_label = Label(closing_frame, 
                         text="Labor report ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
LR_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
LR_entry = Entry(closing_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=8,
                          borderwidth=0, 
                          justify=RIGHT  )
LR_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


#Label and entry for the The Float  
TheFLoat_Label = Label(closing_frame, 
                         text="The Float ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
TheFLoat_Label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
TheFloat_entry = Entry(closing_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=8,
                          borderwidth=0, 
                          justify=RIGHT  )
TheFloat_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")


#Label and entry for the Total Payment  
TP_label = Label(closing_frame, 
                         text="Total Payment ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
TP_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
TP_entry = Entry(closing_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont,10),
                         width=8,
                          borderwidth=0, 
                          justify=RIGHT  )
TP_entry.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")


#Label and entry for the Credit  
credit_label = Label(closing_frame, 
                         text="Credit ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
credit_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
credit_entry = Entry(closing_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont, 10),
                         width=8,
                          borderwidth=0, 
                          justify=RIGHT  )
credit_entry.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")


#Label and entry for the Expense   
expense_label = Label(closing_frame, 
                         text="Expense ", 
                         fg=inputForeground, bg=inputBackground,
                         font=(theFont, 10))
expense_label.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
expense_entry = Entry(closing_frame, 
                         bg=entryBackground, fg=entryForeground, 
                         font =(theFont, 10),
                         width=8,
                          borderwidth=0, 
                          justify=RIGHT  )
expense_entry.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

#Label and entry for Cash   
cash_label = Label(output_frame, 
                         text="Cash", 
                         fg=outputForeground, bg=outputBackground,
                         font=(theFont, 10))
cash_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
cash_text = tk.Text(output_frame,  
                                width=8, height= 1,
                                fg = texBoxForeground, bg=textBoxBackground,
                                font=(theFont, 10),
                                borderwidth=0)
cash_text.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for Sum   
sum_label = Label(output_frame, 
                         text="Sum", 
                         fg=outputForeground,bg=outputBackground,
                         font=(theFont, 10))
sum_label.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
sum_text = tk.Text(output_frame,  
                                width=8, height= 1,
                                fg = texBoxForeground, bg=textBoxBackground,
                                font=(theFont, 10),
                                borderwidth=0)
sum_text.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

#Label and entry for the Difference   
diff_label = Label(output_frame, 
                         text="Difference", 
                         fg=outputForeground,bg=outputBackground,
                         font=(theFont, 10))
diff_label.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")
diff_text = tk.Text(output_frame,  
                                width=8, height= 1,
                                fg = texBoxForeground, bg=textBoxBackground,
                                font=(theFont, 10),
                                borderwidth=0)
diff_text.grid(row=3, column=4, padx=5, pady=5, sticky="nsew")

#Label and entry for the Deposit   
dep_label = Label(output_frame, 
                         text="Deposit", 
                         fg=outputForeground,bg=outputBackground,
                         font=(theFont, 10))
dep_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
dep_text = tk.Text(output_frame,  
                                width=8, height= 1,
                                fg = texBoxForeground, bg=textBoxBackground,
                                font=(theFont, 10),
                                borderwidth=0)
dep_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the Total   
total_label = Label(output_frame, 
                         text="Total", 
                         fg=outputForeground,bg=outputBackground,
                         font=(theFont, 10))
total_label.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
total_text = tk.Text(output_frame,  
                                width=8, height= 1,
                                fg = texBoxForeground, bg=textBoxBackground,
                                font=(theFont, 10),
                                borderwidth=0)
total_text.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")



#Widget properties for the calculate button
calculate_button = tk.Button(root, 
                             text="Calculate", 
                             activebackground="#6a6a6a",
                             command = calculate,
                             activeforeground="white",
                             fg='#363636',
                             bg='#35aeea',
                             font=("Fixedsys", 17),
                             cursor="hand2",
                             bd=3,
                             disabledforeground="gray",
                             highlightbackground="black",
                             highlightcolor="green",
                             highlightthickness=2)
calculate_button.grid(row = 4, column= 1, padx=15, pady=5, sticky="E", )


root.mainloop()
