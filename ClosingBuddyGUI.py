from tkinter import *               #Tkinter library     
from datetime import date           #For current date 
import WindowSet                    #Sets tool window dimensions off of current screen
from dark_title_bar import *        #For dark title bar
import os

#Today's Date
today = date.today()
formatted_date = today.strftime("%m/%d/%Y")
#Global colors used 
color1 = '#343434'  # dark gray used for background for frames
color2 = '#29aff1'  # primary blue used throughout the app
color3 = '#4d4d4d'  # lighter gray used for entry background
color4 = '#ebebeb'  # cream color used for foreground
theFont = "arial"   #Primary font used

#GUI Class 
class ClosingBuddyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tuffy's Closing Buddy")
        root.configure(bg = '#101010') 
        dark_title_bar(root)

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
        #Label widget for header
        name_label = Label(root,
                        text="Tuffy's Closing Buddy",
                        bg=color1, fg=color2,
                        font=("Fixedsys", 20))
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #All the frames used 
        dollar_frame = Frame(self.root, bg=color1)
        dollar_frame.grid(row=1, column=0, padx=10, pady=10)

        coin_frame = Frame(self.root, bg=color1)
        coin_frame.grid(row=1, column=1, padx=10, pady=10)

        report_frame = Frame(self.root, bg=color1)
        report_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        cash_sumary_frame = Frame(self.root, bg=color1)
        cash_sumary_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        #Using forloop to create the label and entry for each of the cash denominations. (We use for loop for scalibility and less redundancy)
        row = 1
        for parent, denominations in [(coin_frame, self.coins), (dollar_frame, self.dollars)]:
            for denomination in denominations:
                Label(parent, text=denomination,
                        fg=color4, bg=color1,
                        font=(theFont, 10)).grid(row=row, column=0, padx=5, pady=2)
                entry = Entry(parent,
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
            Label(report_frame, text=field,
                    fg=color4, bg=color1,
                    font=(theFont, 10)).grid(row=row, column=col * 2, padx=5, pady=2)
            entry = Entry(report_frame,
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
            Label(cash_sumary_frame, text=field,
                    fg=color2, bg=color1,
                    font=(theFont, 10)).grid(row=row, column=col * 2, padx=5, pady=2)
            text = Text(cash_sumary_frame,
                        width=8, height=1,
                        fg=color4, bg='#101010',
                        font=(theFont, 10),
                        borderwidth=0)
            text.grid(row=row, column=col * 2 + 1, padx=5, pady=2)
            self.result_text[field] = text

        #Widget for the calculate button 
        self.calculate_button = Button(self.root, text="Calculate", command=self.clicked,
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
        current_date = Label(root,
                                text=formatted_date,
                                fg=color1, bg=color2,
                                font=("Fixedsys", 17)
                                )
        current_date.grid(row=4, column=0, padx=15, pady=5, sticky="W")

    def calculate(self):
        # Store starting bills before modification
        if not hasattr(self, 'starting_bills'):
            self.starting_bills = {denom: int(self.entries[denom].get() or 0) for denom in self.dollars}
            x = {denom: int(self.entries[denom].get() or 0) for denom in self.dollars}
        
        #Calulate the total
        try:
            total_p = float(self.additional_entries["Total Payment"].get())
        except ValueError:
            total_p = 0
        try:
            the_float = round(float(self.additional_entries["The Float"].get()), 2)
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

        remaining_tips = int(tips)
        for denomination in sorted(self.dollars.keys(), key=lambda d: -self.dollars[d]):
            try:
                bill_value = self.dollars[denomination]
                available_bills = int(self.entries[denomination].get())

                if remaining_tips >= bill_value and available_bills > 0:
                    bills_to_remove = int(min(remaining_tips // bill_value, available_bills))
                    remaining_tips -= bills_to_remove * bill_value

                    self.entries[denomination].delete(0, END)
                    self.entries[denomination].insert(0, int(available_bills - bills_to_remove))
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
        self.result_text["Cash"].delete("1.0", END)
        self.result_text["Cash"].insert("1.0", str(cash_sum))

        self.result_text["Tips"].delete("1.0", END)
        self.result_text["Tips"].insert("1.0", str(tips))

        self.result_text["Deposit"].delete("1.0", END)
        self.result_text["Deposit"].insert("1.0", str(deposit))

        self.result_text["Total"].delete("1.0", END)
        self.result_text["Total"].insert("1.0", f"${total:.2f}")

        #Calculate the difference
        self.result_text["Sum"].delete("1.0", END)
        self.result_text["Sum"].insert("1.0", f"${total_sum:.2f}")
        
        diff = total_sum - total
        # Update the "Diff" textbox with the calculated difference
        self.result_text["Difference"].delete("1.0", END)
        self.result_text["Difference"].insert("1.0", f"{diff:.2f}")
    
    #Function used to load the previous float, we use a file that holds this value of the previous day 
    def load_previous_float(self):
        try:
            with open("float_value.txt", "r") as file:
                float_value = file.read().strip()
                if float_value:
                    self.additional_entries["The Float"].insert(0, float_value)  # Load previous Float
        except FileNotFoundError:
            pass  # No previous float exists yet
    

    #Function used to create a new window for the Summary 
    def show_summary(self):
        # Create a new window
        summary_window = Toplevel(self.root, bg = '#101010')
        summary_window.title("Daily Summary")
        dark_title_bar(summary_window)
        
        # Get main window geometry
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_width = root.winfo_width()

        # Set new window position
        new_window_x = main_x + main_width
        new_window_y = main_y
        summary_window.geometry(f"+{new_window_x}+{new_window_y}")

        #Frames for summary window 
        summary_frame = Frame(summary_window, padx=10, pady=10, bg=color1)
        summary_frame.pack(fill="x", padx=10, pady=5)

        instruction_frame = Frame(summary_window, padx=10, pady=10, bg=color1)
        instruction_frame.pack(fill="x", padx=10, pady=5)

        # Retrieve values from the UI
        total_payment = self.additional_entries["Total Payment"].get()
        labor_report = self.additional_entries["Labor Report"].get()  +"%"
        tips = self.result_text["Tips"].get("1.0", END).strip()
        deposit = self.result_text["Deposit"].get("1.0", END).strip()
        difference = self.result_text["Difference"].get("1.0", END).strip()

        # Labels to display the summary
        summary_data = {
            "Date": formatted_date,
            "Total Payment": total_payment,
            "Labor Report": labor_report,
            "Tips": tips,
            "Deposit": deposit,
            "Difference": difference,
        }
        summary_text =""

        for i, (key, value) in enumerate(summary_data.items()):
            text = f"{key}: {value}"
            Label(summary_frame, text=f"{key}: {value}", font=theFont, 
                                                      bg = color1, fg =color4).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            summary_text += text +"\n"
        # Instructions for removing bills used
        Label(instruction_frame, text="Take out the following bills:", font=theFont, bg=color1, fg=color4).pack(anchor="w", padx=10, pady=5)
        
        for denom, value in self.dollars.items():
            try:
                original_count = int(self.starting_bills.get(denom, 0))
                current_count = int(self.entries[denom].get() or 0)
                used_count = int(max(original_count - current_count, 0))

                if used_count > 0:
                    Label(instruction_frame, text=f"{denom}: Remove {used_count}", font=theFont, bg=color1, fg=color4).pack(anchor="w", padx=10)
            except ValueError:
                pass
            
        # Function to save the summary
        def save_summary():
            date_for_file = today.strftime("%m.%d.%Y")
            # Ensure the "Summaries" folder exists
            save_folder = "Summaries"
            os.makedirs(save_folder, exist_ok=True)  # Creates folder if it doesn’t exist

            # Format filename with current date
            filename = os.path.join(save_folder, f"Summary_{date_for_file}"+".txt")
            print(str(filename)+"\n\n")

            # Open file and write summary data
            with open(filename, "w") as file:  # "w" creates or overwrites the file
                for key, value in summary_data.items():
                    file.write(f"{key}: {value}\n")

        self.save_button = Button(summary_window, text="Save",
                                        command= save_summary,
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
        self.save_button.pack(fill="x", padx=10, pady=5)


    #Function for calculate button to run all the functions
    def clicked(self):
        self.calculate()
        self.show_summary()

#Main function used to run the GUI
if __name__ == "__main__":
    root = Tk()
    app = ClosingBuddyGUI(root)
    root.mainloop()
