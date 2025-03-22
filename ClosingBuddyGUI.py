import tkinter as tk                                #tkinter library for GUI
from tkinter import *   #Import filedialog to allow users to interact with their file system, message box for displaying separate message boxes
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

    cash = twenties + tens + fives + ones + quarters + dimes + nickels + pennies

    cash_text.delete("1.0", tk.END)
    cash_text.insert("1.0",str(cash))

#function to calculate sum and display to the sum textbox 
def calculate_sum():
    global cash, summ, exp, crd
    exp = int(expense_entry.get())
    crd = int(credit_entry.get())

    summ = exp + crd + cash

    sum_text.delete("1.0", tk.END)
    sum_text.insert("1.0",str(summ))

#function to calculate difference and display to the difference textbox. As well as total and deposit 
def calculate_rest():
    global summ, total_p ,total, diff, the_float, twenties

    total_p = float(TP_entry.get()) 
    the_float = float(TheFloat_entry.get())
    total = total_p + the_float

    diff = summ - total 

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
root.configure(bg = '#140042')

#dynamically set screen to form fit depending on what window screen is used 
WindowSet.setScreen(root, wRatio = 0.31, hRatio = 0.55) # Dynamically sets window size for program
root.configure(bg='#140042')

#declaration of all of the frames used 
dollar_frame  = Frame(root, bg='#200067')
coin_frame = Frame(root, bg='#200067')
closing_frame =  Frame(root, bg= '#200067')
output_frame = Frame(root, bg= '#200067' )

#grid of each of the frames to fit nicely
dollar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
coin_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
closing_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)
output_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan= 2)

#Label and entry for the 20 dollar bills 
twenties_labels = Label(dollar_frame, 
                         text="20 dollar bill", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
twenties_labels.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
twenties_entry = Entry(dollar_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                          width=5 )
twenties_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the 10 dollar bills 
tens_label = Label(dollar_frame, 
                         text="10 dollar bill", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
tens_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
tens_entry = Entry(dollar_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
tens_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the 5 dollar bills 
fives_label = Label(dollar_frame, 
                         text="5 dollar bill", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
fives_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
fives_entry = Entry(dollar_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
fives_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the 1 dollar bills 
ones_label = Label(dollar_frame, 
                         text="1 dollar bill", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
ones_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
ones_entry = Entry(dollar_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
ones_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the quarters 
quarter_label = Label(coin_frame, 
                         text="Quarters", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
quarter_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
quarter_entry = Entry(coin_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
quarter_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the dimes 
dimes_label = Label(coin_frame, 
                         text="Dimes   ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
dimes_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
dimes_entry = Entry(coin_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
dimes_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the Nickels 
nickels_label = Label(coin_frame, 
                         text="Nickels ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
nickels_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
nickels_entry = Entry(coin_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
nickels_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the Pennies 
pennies_label = Label(coin_frame, 
                         text="Pennies ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
pennies_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
pennies_entry = Entry(coin_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=5  )
pennies_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")


#Label and entry for the Labor report  
LR_label = Label(closing_frame, 
                         text="Labor report ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
LR_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
LR_entry = Entry(closing_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=8  )
LR_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


#Label and entry for the The Float  
TheFLoat_Label = Label(closing_frame, 
                         text="The Float ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
TheFLoat_Label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
TheFloat_entry = Entry(closing_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=8  )
TheFloat_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")


#Label and entry for the Total Payment  
TP_label = Label(closing_frame, 
                         text="Total Payment ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
TP_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
TP_entry = Entry(closing_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=8  )
TP_entry.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")


#Label and entry for the Credit  
credit_label = Label(closing_frame, 
                         text="Credit ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
credit_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
credit_entry = Entry(closing_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=8  )
credit_entry.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")


#Label and entry for the Expense   
expense_label = Label(closing_frame, 
                         text="Expense ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
expense_label.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
expense_entry = Entry(closing_frame, 
                         bg='#6a6a6a', 
                         fg='#c1bec8', 
                         font ='Fixedsys',
                         width=8  )
expense_entry.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

#Label and entry for Cash   
cash_label = Label(output_frame, 
                         text="Cash ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
cash_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
cash_text = tk.Text(output_frame,  
                                width=6, height= 1,
                                fg = "#c1bec8",
                                bg="#585858",
                                font=("Fixedsys", 10))
cash_text.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for Sum   
sum_label = Label(output_frame, 
                         text="Sum ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
sum_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
sum_text = tk.Text(output_frame,  
                                width=6, height= 1,
                                fg = "#c1bec8",
                                bg="#585858",
                                font=("Fixedsys", 10))
sum_text.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

#Label and entry for the Difference   
diff_label = Label(output_frame, 
                         text="Difference ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
diff_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
diff_text = tk.Text(output_frame,  
                                width=6, height= 1,
                                fg = "#c1bec8",
                                bg="#585858",
                                font=("Fixedsys", 10))
diff_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Label and entry for the Deposit   
dep_label = Label(output_frame, 
                         text="Deposit ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
dep_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
dep_text = tk.Text(output_frame,  
                                width=6, height= 1,
                                fg = "#c1bec8",
                                bg="#585858",
                                font=("Fixedsys", 10))
dep_text.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

#Label and entry for the Total   
total_label = Label(output_frame, 
                         text="Total ", 
                         fg='#c1bec8',bg='#200067',
                         font=("Fixedsys", 10))
total_label.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
total_text = tk.Text(output_frame,  
                                width=6, height= 1,
                                fg = "#c1bec8",
                                bg="#585858",
                                font=("Fixedsys", 10))
total_text.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")



#Widget properties for the calculate button
calculate_button = tk.Button(root, 
                             text="Calculate", 
                             activebackground="#6a6a6a",
                             command = calculate,
                             activeforeground="white",
                             fg='#c1bec8',
                             bg='#200067',
                             font=("Fixedsys", 17),
                             cursor="hand2",
                             bd=3,
                             disabledforeground="gray",
                             highlightbackground="black",
                             highlightcolor="green",
                             highlightthickness=2)
calculate_button.grid(row = 3, column= 1, padx=15, pady=5, sticky="E", )


root.mainloop()