import tkinter as tk
from tkinter.font import BOLD
from data_entry import Data_Table

class Confidence_Interval_App:
    def __init__(self):
        # Initialize window
        self.root = tk.Tk()
        self.root.title("Two Mean CI Calculator")
        self.canvas = tk.Canvas(self.root, height=800, width=800, bg="#FFFFF0")
        self.canvas.pack()
        self.root.eval('tk::PlaceWindow . center')
        
        # Create a title label
        self.title = tk.Label(self.root, text= "Confidence Interval Calculator and Visualization \n for Comparing Means")
        self.title.config(bg="#FFFFF0", fg= "black", font= ("Helvetica", 18))
        self.title.place(relx= 0.5, rely= 0.06, anchor= 'center')

        # Step 1 Label
        self.step1 = tk.Label(self.root, text= "Step 1. Select a Case")
        self.step1.config(bg= "#FFFFF0", fg= "red", font= ("Courier", 14, BOLD))
        self.step1.place(relx= 0.01, rely = 0.13, anchor='w')
        # Step 2 Label
        self.step2 = tk.Label(self.root, text= "Step 2. Data Entry")
        self.step2.config(bg= "#FFFFF0", fg= "green", font= ("Courier", 14, BOLD))
        self.step2.place(relx= 0.01, rely = 0.25, anchor='w')
        # Step 3 Label 
        self.step3 = tk.Label(self.root, text= "Step 3. Calculation & Visualization")
        self.step3.config(bg= "#FFFFF0", fg= "brown", font= ("Courier", 14, BOLD))
        self.step3.place(relx= 0.75, rely = 0.125, anchor='center')

        # Data Members 
        self.cases = [
            "   1. Paired Test (not independent)",
            "   2. Two Independent Groups with Population Variances Known",
            "   3. Two Independent Groups, Population Variance Unknown",
            "   4. Pooled Test (Variance Unknown but Assumed Equal)"
        ]

        self.stats = [
            "Two Means (µ1, µ2)",
            "Two Proportions (p1, p2)"
        ]

        self.data_table = Data_Table(self.root)
        self.submit_data = tk.Button(self.root, text="Calculate Confidence Interval", command=self.data_table.valid_entries)
        
    def confidence_interval_selection(self):
        clicked = tk.StringVar()
        clicked.set("   Select a Sample Type...")
        
        dropdown = tk.OptionMenu(self.root, clicked, *self.cases, command= lambda click: self.__select_case(click))
        dropdown.config(width= 17, anchor= 'w')
        dropdown.place(relx= 0.01, rely= 0.16)

    def run(self):
        self.root.mainloop() 

    # Private Methods
    def __case2_stat_picker(self, stat):
        if stat == self.stats[1]:
            self.data_table.proportion_table()
            self.data_table.case = self.data_table.case_types[1]
            self.submit_data.place(relx=0.01, rely=0.85)
        else:
            self.data_table.mean_table()
            self.data_table.case = self.data_table.case_types[2]
            self.submit_data.place(relx=0.01, rely=0.85)

    def __select_case(self, selected_case):
        if selected_case == self.cases[0]:
            self.data_table.paired_table()
            self.data_table.case = self.data_table.case_types[0]
            self.submit_data.place(relx=0.01, rely=0.85)
        elif selected_case == self.cases[1]:
            next_click = tk.StringVar()
            next_click.set("Select Sample Statistic")

            dropdown2 = tk.OptionMenu(self.root, next_click, *self.stats, command= lambda stat: self.__case2_stat_picker(stat))
            dropdown2.config(width= 17)
            dropdown2.place(relx= 0.01, rely= 0.2)
        elif selected_case == self.cases[3]:
            self.data_table.mean_var_unknown_table()
            self.data_table.case = self.data_table.case_types[3]
            self.submit_data.place(relx=0.01, rely=0.85)
        else: 
            self.data_table.mean_var_unknown_table()
            self.data_table.case = self.data_table.case_types[4]
            self.submit_data.place(relx=0.01, rely=0.85)


if __name__ == "__main__":
    app = Confidence_Interval_App() 
    app.confidence_interval_selection()
    app.run()

