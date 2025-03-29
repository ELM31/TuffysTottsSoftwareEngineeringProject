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

        WindowSet.setScreen(root, wRatio = 0.23, hRatio = .55) # Dynamically sets window size for program

        # Define denominations and their respective values
        self.coins = {
            "Quarters": 0.25, "Dimes": 0.10, "Nickels": 0.05, "Pennies": 0.01 
        }
        
        self.dollars = {
             "100 dollar bills":100.00, "50 dollar bills": 50.00, "20 dollar bills": 20.00, "10 dollar bills": 10.00, "5 dollar bills": 5.00, "1 dollar bills": 1.00
        }
        
        self.entries = {}
        self.create_widgets()
        self.load_previous_float()  # Load stored Float at startup

    
    def create_widgets(self):
        color1 = '#343434'  # dark gray used for background for frames
        color2 = '#29aff1'  # primary blue used throughout the app
        color3 = '#4d4d4d'  # lighter gray used for entry background
        color4 = '#ebebeb'  # cream color used for foreground
        theFont = "arial"   #Primary font used

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

        cash_sumary_frame = tk.Frame(self.root, bg=color1)
        cash_sumary_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

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
        result_fields = ["Sum", "Total", "Difference", "Cash", "Deposit", "Tips"]
        self.result_text = {}
        for i, field in enumerate(result_fields):
            row = i % 3  # Calculate row index
            col = i // 3  # Calculate column index
            tk.Label(cash_sumary_frame, text=field,
                    fg=color2, bg=color1,
                    font=(theFont, 10)).grid(row=row, column=col * 2, padx=5, pady=2)
            text = tk.Text(cash_sumary_frame,
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
                                        fg=color1,
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
                                fg=color1, bg=color2,
                                font=("Fixedsys", 17)
                                )
        current_date.grid(row=4, column=0, padx=15, pady=5, sticky="W")

    def calculate_cash(self):
        #Calulate the total
        try:
            total_p = float(self.additional_entries["Total Payment"].get())
        except ValueError:
            total_p = 0
        try:
            the_float = float(self.additional_entries["The Float"].get())
        except ValueError:
            the_float = 0

        total = total_p + the_float

        #Get expense from widget entry 
        try:
            expense = float(self.additional_entries["Expense"].get() or 0)
        except ValueError:
            expense = 0
        #tips is 90% of the expense 
        tips = round(expense * 0.9)

        #get the sum of all of the cash 
        cash_sum = 0.0
        for x, y in {**self.coins, **self.dollars}.items():
            try:
                count = int(self.entries[x].get())
                cash_sum += count * y
            except ValueError:
                pass  
        #We take the tips through credit from the cash_sum 
        cash_sum = cash_sum - tips 

        remaining_tips = tips
        for denomination in sorted(self.dollars.keys(), key=lambda d: -self.dollars[d]):
            try:
                bill_value = self.dollars[denomination]
                available_bills = int(self.entries[denomination].get())

                if remaining_tips >= bill_value and available_bills > 0:
                    bills_to_remove = min(remaining_tips // bill_value, available_bills)
                    remaining_tips -= bills_to_remove * bill_value

                    self.entries[denomination].delete(0, tk.END)
                    self.entries[denomination].insert(0, str(available_bills - bills_to_remove))
            except ValueError:
                pass

        #Calculate the deposit
        try:
            hundred_dollar_bills = int(self.entries["100 dollar bills"].get()) *100
        except ValueError:
            hundred_dollar_bills = 0
        try:
            fifty_dollar_bills = int(self.entries["50 dollar bills"].get()) *50
        except ValueError:
            fifty_dollar_bills = 0
        try:
            twenty_dollar_bills = int(self.entries["20 dollar bills"].get()) *20
        except ValueError:
            twenty_dollar_bills = 0

        deposit = hundred_dollar_bills + fifty_dollar_bills + twenty_dollar_bills

        float_value = cash_sum - deposit  # Calculate new Float

        with open("float_value.txt", "w") as file: # Save Float value for next use
            file.write(str(float_value))
        
        
        try:
            credit = float(self.additional_entries["Credit"].get() or 0)
        except ValueError:
            credit = 0
        total_sum = tips + credit + cash_sum #calculate sum 

        # Update the UI
        self.result_text["Cash"].delete("1.0", tk.END)
        self.result_text["Cash"].insert("1.0", str(cash_sum))

        self.result_text["Tips"].delete("1.0", tk.END)
        self.result_text["Tips"].insert("1.0", str(tips))

        self.result_text["Deposit"].delete("1.0", tk.END)
        self.result_text["Deposit"].insert("1.0", str(deposit))

        self.result_text["Total"].delete("1.0", tk.END)
        self.result_text["Total"].insert("1.0", f"${total:.2f}")

        #Calculate the difference
        self.result_text["Sum"].delete("1.0", tk.END)
        self.result_text["Sum"].insert("1.0", f"${total_sum:.2f}")
        
        diff = total_sum - total
        # Update the "Diff" textbox with the calculated difference
        self.result_text["Difference"].delete("1.0", tk.END)
        self.result_text["Difference"].insert("1.0", f"${diff:.2f}")


            
        
    #This function is used for button, this is used to run all three main functions in order. 
    def calculate(self):
        self.calculate_cash()
    
    #Function used to load the previous float, we use a file that holds this value of the previous day 
    def load_previous_float(self):
        try:
            with open("float_value.txt", "r") as file:
                float_value = file.read().strip()
                if float_value:
                    self.additional_entries["The Float"].insert(0, float_value)  # Load previous Float
        except FileNotFoundError:
            pass  # No previous float exists yet

#Main function used to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ClosingBuddyGUI(root)
    root.mainloop()
