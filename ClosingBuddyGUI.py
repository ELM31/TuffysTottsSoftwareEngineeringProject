import tkinter as tk
from tkinter import *               #Tkinter library     
from datetime import date           #For current date 
import WindowSet                    #Sets tool window dimensions off of current screen

#Today's Date
today = date.today()
formatted_date = today.strftime("%m/%d/%Y")

#GUI Class 
class ClosingBuddyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tuffy's Closing Buddy")
        root.configure(bg = '#101010') 

        WindowSet.setScreen(root, wRatio = 0.23, hRatio = 0.49) # Dynamically sets window size for program

        # Define denominations and their respective values
        self.coins = {
            "Quarters": 0.25, "Dimes": 0.10, "Nickels": 0.05, "Pennies": 0.01 
        }
        
        self.dollars = {
             "20 dollar bills": 20.00, "10 dollar bills": 10.00, "5 dollar bills": 5.00, "1 dollar bills": 1.00
        }
        
        self.entries = {}
        self.create_widgets()
    
    def create_widgets(self):
        color1 = '#343434'  # dark gray used for background for frames
        color2 = '#35aeea'  # primary blue used throughout the app
        color3 = '#4d4d4d'  # lighter gray used for entry background
        color4 = '#ebebeb'  # cream color used for foreground
        theFont = "arial"   #Priamry font used

        #Label widget for header
        name_label = Label(root,
                        text="Tuffy's Closing Buddy",
                        bg=color1, fg=color2,
                        font=("Fixedsys", 20))
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #All the frames used 
        dollar_frame = tk.Frame(self.root, bg=color1)
        dollar_frame.grid(row=1, column=0, padx=10, pady=10)

        coin_frame = tk.Frame(self.root, bg=color1)
        coin_frame.grid(row=1, column=1, padx=10, pady=10)

        report_frame = tk.Frame(self.root, bg=color1)
        report_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        summary_frame = tk.Frame(self.root, bg=color1)
        summary_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        #Using forloop to create the label and entry for each of the cash denominations. (We use for loop for scalibility and less redundancy)
        row = 1
        for parent, denominations in [(coin_frame, self.coins), (dollar_frame, self.dollars)]:
            for denomination in denominations:
                tk.Label(parent, text=denomination,
                        fg=color4, bg=color1,
                        font=(theFont, 10)).grid(row=row, column=0, padx=5, pady=2)
                entry = tk.Entry(parent,
                                bg=color3, fg=color2,
                                font=(theFont, 10),
                                width=5,
                                borderwidth=0,
                                justify=RIGHT)
                entry.grid(row=row, column=1, padx=5, pady=2)
                self.entries[denomination] = entry
                row += 1
        #Using foor loop to for the additional financial field for text and entry. We use a 3x2 grid this time, we use modulo and int division for the logic 
        self.additional_entries = {}
        extra_fields = ["Labor Report", "The Float", "Total Payment", "Credit", "Expense"]
        for i, field in enumerate(extra_fields):
            row = i % 3  # Calculate row index
            col = i // 3  # Calculate column index
            tk.Label(report_frame, text=field,
                    fg=color4, bg=color1,
                    font=(theFont, 10)).grid(row=row, column=col * 2, padx=5, pady=2)
            entry = tk.Entry(report_frame,
                            bg=color3, fg=color2,
                            font=(theFont, 10),
                            width=8,
                            borderwidth=0,
                            justify=RIGHT)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
            self.additional_entries[field] = entry

        #Use of forloop for the result field, this time we use textboxes. We have a 3x2 grid same as the last grid 
        result_fields = ["Sum", "Total", "Difference", "Cash", "Deposit"]
        self.result_text = {}
        for i, field in enumerate(result_fields):
            row = i % 3  # Calculate row index
            col = i // 3  # Calculate column index
            tk.Label(summary_frame, text=field,
                    fg=color2, bg=color1,
                    font=(theFont, 10)).grid(row=row, column=col * 2, padx=5, pady=2)
            text = tk.Text(summary_frame,
                        width=8, height=1,
                        fg=color4, bg='#101010',
                        font=(theFont, 10),
                        borderwidth=0)
            text.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
            self.result_text[field] = text

        #Widget for the calculate button 
        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate,
                                        activeforeground="white",
                                        activebackground="#6a6a6a",
                                        fg='#363636',
                                        bg=color2,
                                        font=("Fixedsys", 17),
                                        cursor="hand2",
                                        bd=3,
                                        disabledforeground="gray",
                                        highlightbackground="black",
                                        highlightcolor="green",
                                        highlightthickness=2)
        self.calculate_button.grid(row=4, column=1, padx=15, pady=5, sticky="E")

        # Widget properties of the current date Label
        current_date = tk.Label(root,
                                text=formatted_date,
                                fg='#363636', bg=color2,
                                font=("Fixedsys", 17)
                                )
        current_date.grid(row=4, column=0, padx=15, pady=5, sticky="W")

    #Function to calculate cash, we use the coin and dollar entries, and change the textbox of sum 
    def calculate_cash(self):
        summ = 0.0
        for x, y in {**self.coins, **self.dollars}.items():
            try:
                count = int(self.entries[x].get())
                summ += count * y
            except ValueError:
                pass  # Ignore non-integer inputs
        
        self.result_text["Cash"].delete("1.0", tk.END)
        self.result_text["Cash"].insert("1.0", str(summ))

    #Function to calculate sum, we get the entries from expense, credit and the textbox output of cash from the last function used 
    def calculate_sum(self):
        try:
            expense = float(self.additional_entries["Expense"].get() or 0)
        except ValueError:
            expense = 0
        
        try:
            credit = float(self.additional_entries["Credit"].get() or 0)
        except ValueError:
            credit = 0

        try:
            cash_value = float(self.result_text["Cash"].get("1.0", tk.END).strip().replace("$", "") or 0)
        except ValueError:
            cash_value = 0

        total_sum = expense + credit + cash_value

        # Update the "Sum" textbox with the calculated sum
        self.result_text["Sum"].delete("1.0", tk.END)
        self.result_text["Sum"].insert("1.0", f"${total_sum:.2f}")

    #Calculate the rest of the output needed, total, deposit and difference 
    def calcualte_rest(self):
        #Calulate the total
        total_p = float(self.additional_entries["Total Payment"].get())
        the_float = float(self.additional_entries["The Float"].get())

        total = total_p + the_float

        #Calculate the difference
        summ = float(self.result_text["Sum"].get("1.0", tk.END).strip().replace("$", "") or 0)

        diff = summ - total

        #Calculate the deposit
        try:
            twenty_dollar_bills = int(self.entries["20 dollar bills"].get()) *20
        except ValueError:
            twenty_dollar_bills = 0

        # Update the "Total" textbox with the calculated total
        self.result_text["Total"].delete("1.0", tk.END)
        self.result_text["Total"].insert("1.0", f"${total:.2f}")

        # Update the "Diff" textbox with the calculated difference
        self.result_text["Difference"].delete("1.0", tk.END)
        self.result_text["Difference"].insert("1.0", f"${diff:.2f}")

        # Update the "Deposit" textbox with the value from "20 dollar bills"
        self.result_text["Deposit"].delete("1.0", tk.END)
        self.result_text["Deposit"].insert("1.0", f"{twenty_dollar_bills}")

    #This function is used for button, this is used to run all three main functions in order. 
    def calculate(self):
        self.calculate_cash()
        self.calculate_sum()
        self.calcualte_rest()
        
#Main function used to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ClosingBuddyGUI(root)
    root.mainloop()
