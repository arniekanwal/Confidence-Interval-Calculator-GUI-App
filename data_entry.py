import tkinter as tk
from tkinter import ttk
from tkinter.constants import NO
from calculator import Stats_Calculator

class Data_Table:
    def __init__(self, root):
        self.root = root

        self.label = tk.Label(root, text="Enter the Confidence Level (1 - α):")
        self.label.config(bg= "#FFFFF0", font= ("Helvetica", 14))
        self.label.place(relx= 0.01, rely= 0.28)

        self.interval = tk.Entry(root)
        self.interval.place(relx= 0.01, rely=0.31)

        self.table = ttk.Treeview(root, height=15)

        # Initialize Entries if Paired Test
        self.x1 = tk.Entry(root, width=5)
        self.x2 = tk.Entry(root, width=5)
        self.count = 0 # counter for paired test

        # Variables for Calculating Confidence Interval
        self.data = []
        self.stats_entries = []
        self.confidence: float  # TODO: add this to valid entries
        
        self.case: str
        self.case_types = [
            "paired",
            "proportion",
            "variance known",
            "variance unknown, unequal",
            "pooled"
        ]
        self.calculator = Stats_Calculator(self.root)

    # Private Methods
    def __place_entries(self, num_entries):
        for i in range(num_entries):
            e = tk.Entry(self.root, width=5)
            e.config(highlightbackground="black")
            e.place(relx=0.19, rely=0.46+(i*0.06))
            self.stats_entries.append(e)  

    def __insert_data(self):
        answer = tk.Label(self.root, text="", fg="hot pink", bg="#FFFFF0")
        answer.place(relx=0.32, rely=0.38)

        try:
            x1_val = float(self.x1.get())
            x2_val = float(self.x2.get())
            self.table.insert('', 'end', iid=self.count, text="", values=(x1_val, x2_val, x1_val-x2_val))
            self.count += 1

            self.data.append(x1_val-x2_val)

        except ValueError:
            self.x1.delete(0, 'end')
            self.x2.delete(0, 'end')
            answer.config(text="Enter a valid number...")

    # Public Methods
    def valid_entries(self):
        answer = tk.Label(self.root, text="", fg="hot pink", bg="#FFFFF0")
        answer.place(relx=0.01, rely=0.9)

        try:
            self.confidence = float(self.interval.get())
        except ValueError:
            self.interval.delete(0, 'end')
            answer.config(text="  Ensure all inputs are valid numbers...")

        try:
            for e in self.stats_entries:
                val = float(e.get())
                self.data.append(val)
            
        except ValueError:
            for e in self.stats_entries:
                e.delete(0, 'end')
            self.data.clear()
            answer.config(text="  Ensure all inputs are valid numbers...")

        if self.case == self.case_types[0]:
            self.calculator.paired_test(self.confidence, self.data)
        elif self.case == self.case_types[1]:
            self.calculator.two_proportions(self.confidence, self.data)
        elif self.case == self.case_types[2]:
            self.calculator.two_mean_var_known(self.confidence, self.data)
        elif self.case == self.case_types[3]:
            self.calculator.two_mean_var_unknown(self.confidence, self.data)
        else:
            self.calculator.pooled_test(self.confidence, self.data)


    def proportion_table(self):
        proportion = tk.Label(self.root, text="Enter Data for Proportions \n\n\n p̂1: \n\n\n n1: \n\n\n p̂2: \n\n\n n2: ")
        proportion.config(bg="#FFFFF0", font=("Helvetica", 14))
        proportion.place(relx=0.01, rely=0.4)

        self.__place_entries(4)

    def paired_table(self):
        # Set Columns for Paired Table
        self.table['columns'] = ("x1", "x2", "Difference")
        self.table.column("#0",width=0, stretch=NO)
        self.table.column("x1", width=80, anchor='center')
        self.table.column("x2", width=80, anchor='center')
        self.table.column("Difference", width=80, anchor='center')
        # Set headings
        self.table.heading("#0", text="", anchor='w')
        self.table.heading("x1", text="x1", anchor='center')
        self.table.heading("x2", text="x2", anchor='center')
        self.table.heading("Difference", text="x1-x2 (Diff)", anchor='center')
        # Place table
        self.table.place(relx=0.01, rely=0.47)

        instruction = tk.Label(self.root, text="Enter data pairs and press 'Insert Pair' to add to table...", anchor='w')
        instruction.config(bg= "#FFFFF0", font= ("Helvetica", 14))
        instruction.place(relx= 0.01, rely= 0.35)

        enter_x1 = tk.Label(self.root, text="x1_val:")
        enter_x1.config(bg= "#FFFFF0", font= ("Helvetica", 14))
        enter_x1.place(relx= 0.01, rely= 0.38)

        enter_x2 = tk.Label(self.root, text="x2_val:")
        enter_x2.config(bg= "#FFFFF0", font= ("Helvetica", 14))
        enter_x2.place(relx= 0.17, rely= 0.38)

        self.x1.place(relx=0.08, rely=0.38)
        self.x2.place(relx=0.24, rely=0.38)

        # button to insert data
        insert_pair = tk.Button(self.root, text="Insert Pair", command= self.__insert_data)
        insert_pair.place(relx=0.02, rely=0.425)

    def mean_table(self):
        var_known_label = tk.Label(self.root, 
        text="Enter Data and Population Variance \n\n\n x̄1: \n\n\n n1: \n\n\n var1: \n\n\n x̄2: \n\n\n n2: \n\n\n var2:")
        var_known_label.config(bg="#FFFFF0", font=("Helvetica", 14))
        var_known_label.place(relx=0.01, rely=0.4) 

        self.__place_entries(6)

    def mean_var_unknown_table(self):
        var_unknown_label = tk.Label(self.root, 
        text="Enter Data and Sample Variance \n\n\n x̄1: \n\n\n n1: \n\n\n var1: \n\n\n x̄2: \n\n\n n2: \n\n\n var2:")
        var_unknown_label.config(bg="#FFFFF0", font=("Helvetica", 14))
        var_unknown_label.place(relx=0.01, rely=0.4) 

        self.__place_entries(6)


