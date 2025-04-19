from tkinter import *               #Tkinter library     
from tkinter import simpledialog    #login messagebox 
from datetime import date           #For current date 
import time                         #Recording time employee starts 
import WindowSet                    #Sets tool window dimensions off of current screen
from dark_title_bar import *        #For dark title bar
import sqlite3                      #For locally saved database
import os                           #used to make folders and use pathnames 
import random                       #for simulation 

#Today's Date
today = date.today()
formatted_date = today.strftime("%m/%d/%Y")

#Global colors used + main font used 
color1 = '#343434'  # dark gray used for background for frames
color2 = '#29aff1'  # primary blue used throughout the app
color3 = '#4d4d4d'  # lighter gray used for entry background
color4 = '#ebebeb'  # cream color used for foreground
theFont = "arial"   #Primary font used

#GUI Class 
class ClosingBuddyGUI:
    #Initlize everything
    def __init__(self, root):
        self.root = root
        self.root.title("Tuffy's Closing Buddy")
        root.configure(bg = '#101010') 
        dark_title_bar(root)

        self.employee_list = create_employees()
        self.current_employee = None 

        WindowSet.setScreen(root, wRatio = 0.23, hRatio = .60) # Dynamically sets window size for program

        # Define denominations and their respective values using a dictonary 
        self.coins = {
            "Quarters": 0.25, "Dimes": 0.10, "Nickels": 0.05, "Pennies": 0.01 
        }

        self.dollars = {
             "100 dollar bills":100.00, "50 dollar bills": 50.00, "20 dollar bills": 20.00, "10 dollar bills": 10.00, "5 dollar bills": 5.00, "1 dollar bills": 1.00
        }
        
        self.total_payment = 0.0  
        self.credit = 0.0
        self.expected_cash = 0.0

        self.entries = {}
        self.create_widgets()
        self.load_previous_float()  # Load stored Float at startup

    #create Widgets
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

        #Using forloop to create the label and entry box for each of the cash denominations. (We use for loop for scalibility and less redundancy)
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
        extra_fields = ["Labor Report", "The Float", "Total Payment", "Credit", "Expense", "Expected Cash"]
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

        self.simulate_button = Button(self.root, text="Simulate", command=self.simulate_day,
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
        self.simulate_button.grid(row=6, column=0, padx=15, pady=5, columnspan= 2)

        self.login_button = Button(self.root, text="Login", command=self.open_login_window,
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
        self.login_button.grid(row=5, column=0, padx=15, pady=5)

        self.close_buttonn = Button(self.root, text="Close Day Out", command=self.close_day_out,
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
        self.close_buttonn.grid(row=5, column=1, padx=15, pady=5)

        # Widget properties of the current date Label
        current_date = Label(root,
                                text=formatted_date,
                                fg=color1, bg=color2,
                                font=("Fixedsys", 17)
                                )
        current_date.grid(row=4, column=0, padx=15, pady=5, sticky="W")
    
    #Function to calculate 
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
                float_value = round(float(file.read().strip()), 2)
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
            Label(summary_frame, text=f"{key}: {value}",
                font=theFont, 
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
            
            # Database save logic
            try:
                conn = sqlite3.connect("closing_summary.db")
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS summaries (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        total_payment TEXT,
                        labor_report TEXT,
                        tips REAL,
                        deposit REAL,
                        difference REAL
                    )
                ''')

                cursor.execute('''
                    INSERT INTO summaries (date, total_payment, labor_report, tips, deposit, difference)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    formatted_date,
                    total_payment,
                    labor_report,
                    float(tips) if tips else 0,
                    float(deposit) if deposit else 0,
                    float(difference) if difference else 0
                ))

                conn.commit()
                conn.close()
                print("Summary saved to database.")
            except Exception as e:
                print(f"Database error: {e}")

        # Function to view all saved summaries from the database
        def view_saved_summaries():
            saved_window = Toplevel(self.root)
            saved_window.title("Saved Summaries")
            saved_window.configure(bg="#101010")
            dark_title_bar(saved_window)

             # Get main window geometry
            main_x = root.winfo_x()
            main_y = root.winfo_y()
            main_width = root.winfo_width()

            # Set new window position
            new_window_x = main_x + main_width
            new_window_y = main_y
            saved_window.geometry(f"+{new_window_x}+{new_window_y}")


            text_area = Text(saved_window, 
                             bg=color1, fg=color4, 
                             font=theFont, wrap="word",
                             width =27, height=19)
            text_area.pack(padx=10, pady=10)

            try:
                conn = sqlite3.connect("closing_summary.db")
                cursor = conn.cursor()
                cursor.execute("SELECT date, total_payment, labor_report, tips, deposit, difference FROM summaries ORDER BY date DESC")
                records = cursor.fetchall()
                conn.close()

                for record in records:
                    text_area.insert("end", f"Date: {record[0]}\nTotal Payment: {record[1]}\nLabor Report: {record[2]}\nTips: ${record[3]:.2f}\nDeposit: ${record[4]:.2f}\nDifference: ${record[5]:.2f}\n{'-'*40}\n")
            except Exception as e:
                text_area.insert("end", f"Error retrieving summaries: {e}")
        
        #Button widet for save 
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

        #Button Widget for History
        self.history_button =Button(summary_window, text="View History",
                                        command= view_saved_summaries,
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
        self.history_button.pack(fill="x", padx=10, pady=5)

    #Function for calculate button to run all the functions
    def clicked(self):
        self.calculate()
        self.show_summary()

    #Function to open loginwindow
    def open_login_window(self):
        LoginWindow(self.root, self.employee_list, self.on_employee_logged_in)

    #Function opens POS window with employee that is logged in
    def on_employee_logged_in(self, employee):
        self.current_employee = employee
        self.menu_items = create_menu()
        self.open_pos_window(employee)

    #Function to simulate a days worth of work. Purely for the presentation, no real applicable use 
    def simulate_day(self):
        employees = create_employees()
        menu_items = create_menu()

        theFloat = float(self.additional_entries["The Float"].get())

        # Simulate random quantity ordered for each menu item
        for item in menu_items:
            item.quantity_ordered = random.randint(15, 30)

        # Simulate random hours worked for each employee
        for emp in employees:
            emp.hours_worked = random.uniform(3, 10)

        # Calculate total payment
        total_payment = sum(item.price * item.quantity_ordered for item in menu_items)

        # Labor report as % of total payment
        total_hours = sum(emp.hours_worked for emp in employees)
        labor_total = 0
        if total_hours > 0:
            for emp in employees:
                share = emp.hours_worked / total_hours
                emp_wage = total_payment * share * 0.15  # Assume 15% goes to wages
                labor_total += emp_wage
        labor_percentage = ((labor_total / total_payment) * 100) if total_payment else 0

        # Simulate credit tips and expected cash
        credit = round(total_payment * 0.9, 2)  # 90% paid by credit
        expense = round(total_payment * 0.05, 2)  # 10% as tips
        expected_cash = (total_payment + theFloat)  - credit 

        # Insert into GUI
        self.additional_entries["Total Payment"].delete(0, END)
        self.additional_entries["Total Payment"].insert(0, f"{total_payment:.2f}")

        self.additional_entries["Labor Report"].delete(0, END)
        self.additional_entries["Labor Report"].insert(0, f"{labor_percentage:.2f}")

        self.additional_entries["Credit"].delete(0, END)
        self.additional_entries["Credit"].insert(0, f"{credit:.2f}")

        self.additional_entries["Expense"].delete(0, END)
        self.additional_entries["Expense"].insert(0, f"{expense:.2f}")

        self.additional_entries["Expected Cash"].delete(0, END)
        self.additional_entries["Expected Cash"].insert(0, f"{expected_cash:.2f}")

    #Function to open POS Window
    def open_pos_window(self, employee):
        self.ticket = []  # Reset the current ticket

        pos_win = Toplevel(self.root)
        pos_win.title(f"POS - {employee.first_name}")
        pos_win.configure(bg='#101010')
        dark_title_bar(pos_win)
        
        # Get main window geometry
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_width = root.winfo_width()

        # Set new window position
        new_window_x = main_x + main_width
        new_window_y = main_y
        pos_win.geometry(f"+{new_window_x}+{new_window_y}")

        Label(pos_win, text=f"Welcome, {employee.first_name}", fg=color4, bg='#101010', font=("Fixedsys", 20)).pack(pady=5)
        
        self.ticket_display = Listbox(pos_win,
                                      bg=color3, fg=color4,
                                      height=10, font=theFont)
        self.ticket_display.pack(pady=5, fill="both", padx=20)

        for item in self.menu_items:
            Button(pos_win, text=f"{item.name} - ${item.price:.2f}", 
                    command=lambda i=item: self.add_to_ticket(i),
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
                    highlightthickness=2).pack(fill="x", padx=20, pady=2)

        Button(pos_win, text="Pay", command=lambda: self.process_payment(pos_win),
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
                highlightthickness=2).pack(pady=10)

    #Fucntion to add tiems into ticket along with price 
    def add_to_ticket(self, item):
        self.ticket.append(item)
        self.ticket_display.insert(END, f"{item.name} - ${item.price:.2f}")

    #Function to process payment, choose between Credit or cash 
    def process_payment(self, pos_win):
        if not self.ticket:
            print("Empty Ticket: No items in ticket.")
            return

        total = sum(item.price for item in self.ticket)

        # Create a payment selection window
        pay_popup = Toplevel(self.root)
        pay_popup.title("Select Payment Type")
        pay_popup.configure(bg="#101010")
        dark_title_bar(pay_popup)

        # Get main window geometry
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_width = root.winfo_width()

        # Set new window position
        new_window_x = main_x + main_width
        new_window_y = main_y
        pay_popup.geometry(f"+{new_window_x}+{new_window_y}")

        Label(pay_popup, text=f"Total: ${total:.2f}\nChoose payment type:", fg="white", bg="#101010", font=("Fixedsys", 16)).pack(pady=10)

        def handle_payment(method):
            self.total_payment += total
            if method == "credit":
                self.credit += total
            else:
                self.expected_cash += total

            self.additional_entries["Total Payment"].delete(0, END)
            self.additional_entries["Total Payment"].insert(0, f"{self.total_payment:.2f}")

            self.additional_entries["Credit"].delete(0, END)
            self.additional_entries["Credit"].insert(0, f"{self.credit:.2f}")

            # Clear the ticket
            self.ticket.clear()
            self.ticket_display.delete(0, END)

            pay_popup.destroy()

        Button(pay_popup, text="Cash", width=10, command=lambda: handle_payment("cash"),activeforeground="white",
                    activebackground="#6a6a6a",
                    fg=color1,
                    bg=color2,
                    font=("Fixedsys", 17),
                    cursor="hand2",
                    bd=3,
                    disabledforeground="gray",
                    highlightbackground="black",
                    highlightcolor="green",
                    highlightthickness=2).pack(pady=5)
        Button(pay_popup, text="Credit", width=10, command=lambda: handle_payment("credit"),activeforeground="white",
                    activebackground="#6a6a6a",
                    fg=color1,
                    bg=color2,
                    font=("Fixedsys", 17),
                    cursor="hand2",
                    bd=3,
                    disabledforeground="gray",
                    highlightbackground="black",
                    highlightcolor="green",
                    highlightthickness=2).pack(pady=5)

        
    #Function to record hours that all employees have been clocked in and update addiotnal entries GUI
    def close_day_out(self):
        if not self.current_employee:
            print("Error", "No employee is currently clocked in.")
            return
        
        theFloat = float(self.additional_entries["The Float"].get())

        expense = round(self.total_payment * 0.05, 2)  # 10% as tips 

        expected_cash = (self.total_payment + theFloat)  - self.credit 

        self.current_employee.clock_out()
        hours = self.current_employee.hours_worked()
        wage = self.current_employee.hourly_rate * hours

        if self.total_payment == 0:
            labor_report = 0.0
        else:
            labor_report = (wage / self.total_payment) * 100

        # Update GUI
        self.additional_entries["Labor Report"].delete(0, END)
        self.additional_entries["Labor Report"].insert(0, f"{labor_report:.2f}")

        self.additional_entries["Expense"].delete(0, END)
        self.additional_entries["Expense"].insert(0, f"{expense:.2f}")

        self.additional_entries["Expected Cash"].delete(0, END)
        self.additional_entries["Expected Cash"].insert(0, f"{expected_cash:.2f}")

        self.current_employee = None        

#Resurant Classes: Menu and employee 
class Menu:
    def __init__(self, name, price):
        self.name = name 
        self.price = price
        self.quantity_ordered = 0  # For simulation

class Employee:
    def __init__(self, first_name, last_name, emp_id, hourly_rate):
        self.first_name = first_name
        self.last_name = last_name
        self.emp_id = emp_id
        self.hourly_rate = hourly_rate
        self.clock_in_time = None
        self.clock_out_time = None
    
    def clock_in(self):
        self.clock_in_time = time.time()
    
    def clock_out(self):
        self.clock_out_time = time.time()

    def hours_worked(self):
        if self.clock_in_time and self.clock_out_time:
            return (self.clock_out_time - self.clock_in_time) / 3600 #seconds to hours 
        return 0

def create_employees():
    return [
        Employee("Tuffy", "Titan", 1111, 20.50),
        Employee("Huey", "Gutierrez", 2222, 16.50),
        Employee("Elena", "Gutierrez", 3333, 20.50),
        Employee("Optimus", "Prime", 4444, 17.25),
        Employee("John", "Jacobs", 5555, 30.00)
    ]

def create_menu():
    return [
        Menu("Classic", 14.50),
        Menu("Fiesta", 18.50),
        Menu("Nori", 19.50),
        Menu("Kimchi", 15.50),
        Menu("Shrimp", 16.50)
    ]

#Class for Login Window
class LoginWindow(Toplevel):
    def __init__(self, master, employee_list, on_login):
        super().__init__(master)
        self.title("Employee Login")
        self.geometry("300x150")
        self.employee_list = employee_list
        self.on_login = on_login
        self.configure(bg="#101010")
        dark_title_bar(self)

        Label(self, text="Enter Employee ID:", font=("Fixedsys", 20), 
              fg="white", bg="#101010").pack(pady=10)
        self.emp_id_entry = Entry(self, bg = color1, fg =color2, font=theFont)
        self.emp_id_entry.pack()

        Button(self, text="Clock In", command=self.verify_login,
                activebackground="#6a6a6a",
                fg=color1,
                bg=color2,
                font=("Fixedsys", 17),
                cursor="hand2",
                bd=3,
                disabledforeground="gray",
                highlightbackground="black",
                highlightcolor="green",
                highlightthickness=2).pack(pady=10)

    def verify_login(self):
        emp_id = self.emp_id_entry.get()
        if not emp_id.isdigit():
            print("Invalid Input: Employee ID must be a number.")
            return

        emp_id = int(emp_id)
        for emp in self.employee_list:
            if emp.emp_id == emp_id:
                emp.clock_in()
                print("Login Successful", f"Welcome, {emp.first_name}!")
                self.on_login(emp)  # Pass the logged-in employee to main app
                self.destroy()
                return

        print("Login Failed", "Employee ID not found.")



#Main function used to run the GUI
if __name__ == "__main__":    
    root = Tk()
    app = ClosingBuddyGUI(root)
    root.mainloop()
