import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from scipy import stats
import math

class Stats_Calculator:
    def __init__(self, root):
        self.root = root

    # Private Methods
    def __confidence_to_alpha(self, confidence):
        if (confidence > 1 and confidence < 100):
            alpha = (100 - confidence) / 100
        else:
            alpha = 1 - confidence
        return alpha

    def __compute_variance(self, data, mean):
        n = len(data)
        sum_squares = 0
        square = 0
        for val in data:
            square = (val - mean) * (val - mean)
            sum_squares += square
        variance = sum_squares / (n-1)
        return variance

    def __compute_mean(self, data):
        sum = 0
        n = len(data)
        for val in data:
            sum += val
        
        mean = sum/n
        return mean
        
    def __make_visualization(self, interval, alpha):
        self.normal_pic = Image.open("/Users/SpicyCurry/VSCodeProjects/Confidence_Interval_Calculator/normal.png")
        self.resized = self.normal_pic.resize((300, 225), Image.ANTIALIAS)
        self.normal_graph = ImageTk.PhotoImage(self.resized)
        self.display_graph = tk.Label(image=self.normal_graph)
        self.display_graph.place(x=430, y=360)

        self.ci_percent = (1-alpha) * 100
        self.explain_graph = tk.Label(self.root, text=f'{self.ci_percent}% Confidence Interval for µ1 - µ2', bg="#FFFFF0", font=("Helvetica, 14"))
        self.explain_graph.place(relx=0.55, rely=0.75)

        self.ci_label = tk.Label(self.root, text=f'Confidence Interval: ({interval[0]:.4f},{interval[1]:.4f})', 
            font=("Helvetica, 14"), bg="#FFFFF0")
        self.ci_label.place(relx=0.55, rely= 0.8)

    # Public Methods
    def paired_test(self, confidence, data):
        mean = self.__compute_mean(data)
        variance = self.__compute_variance(data, mean)
        standard_error = math.sqrt((variance/len(data)))

        alpha = self.__confidence_to_alpha(confidence)
        t_stat = stats.t.ppf(1-alpha/2, len(data)-1)

        interval = []
        interval.append(mean - (t_stat * standard_error))
        interval.append(mean + (t_stat * standard_error))

        stats_display = f'Important Statistics:\n\nSample Mean (x̄) = {mean}\nSample Variance = {variance}\nT-Stat = {t_stat}\nStandard Error = {standard_error}\nDegrees of Freedom = {len(data)-1}'
        stats_label = tk.Label(self.root, text=stats_display, font=("Helvetica", 14), bg="#FFFFF0", anchor='w')
        stats_label.place(relx=0.6, rely=0.2)
        
        self.__make_visualization(interval, alpha)
        self.explain_graph.config(text=f'{self.ci_percent}% Estimate for paired µ...')


    def two_mean_var_known(self, confidence, data):
        mean1 = data[0]
        n1 = data[1]
        var1 = data[2]

        mean2 = data[3]
        n2 = data[4]
        var2 = data[5]
        
        new_variance = (var1/n1) + (var2/n2)
        standard_error = math.sqrt(new_variance)
        mean_diff = mean1-mean2
        alpha = self.__confidence_to_alpha(confidence)

        if n1 > 30 and n2 > 30:
            stat = stats.norm.ppf(1-alpha/2)
            is_z_score = False
        else:
            is_z_score = True
            stat = stats.t.ppf(1-alpha/2, n1 + n2 - 2)

        interval = []
        interval.append(mean_diff - (stat * standard_error))
        interval.append(mean_diff + (stat * standard_error))

        if is_z_score:
            stat_display = "Z-Score = "
            df = "N/A"
        else:
            stat_display = "T-Stat = "
            df = str(n1 + n2 - 2)

        display = f'Important Statistics:\n\nx̄1 - x̄2 = {mean_diff}\n{stat_display}{stat}\nStandard Error = {standard_error}\nDegrees of Freedom = {df}'
        stats_label = tk.Label(self.root, text=display, font=("Helvetica", 14), bg="#FFFFF0", anchor='w')
        stats_label.place(relx=0.6, rely=0.2)
        
        self.__make_visualization(interval, alpha)


    def two_proportions(self, confidence, data):
        p1 = data[0]
        n1 = data[1]
        p2 = data[2]
        n2 = data[3]
        
        variance = ((p1 * (1 - p1))/n1) + ((p2 * (1 - p2))/n2)
        standard_error = math.sqrt(variance)
        p_diff = p1-p2
        alpha = self.__confidence_to_alpha(confidence)

        z_stat = stats.norm.ppf(1-alpha/2)

        interval = []
        interval.append(p_diff - (z_stat * standard_error))
        interval.append(p_diff + (z_stat * standard_error))

        stats_display = f'Important Statistics:\n\np̂1 - p̂2 = {p_diff}\nZ-Score = {z_stat}\nStandard Error = {standard_error}'
        stats_label = tk.Label(self.root, text=stats_display, font=("Helvetica", 14), bg="#FFFFF0", anchor='w')
        stats_label.place(relx=0.6, rely=0.2)
        
        self.__make_visualization(interval, alpha)
        self.explain_graph.config(text=f'{self.ci_percent}% Estimate for p1 - p2')


    def two_mean_var_unknown(self, confidence, data):
        mean1 = data[0]
        n1 = data[1]
        var1 = data[2]

        mean2 = data[3]
        n2 = data[4]
        var2 = data[5]
        
        joint_var = (var1/n1) + (var2/n2)
        standard_error = math.sqrt(joint_var)
        mean_diff = mean1-mean2
        alpha = self.__confidence_to_alpha(confidence)
        is_z_score = False

        if n1 > 30 and n2 > 30:
            stat = stats.norm.ppf(1-alpha/2)
            is_z_score = True
        else:
            degrees_freedom = (math.pow(joint_var, 2)) / ( ((1/(n1-1)) * math.pow(var1/n1, 2)) + ((1/(n2-1)) * math.pow(var2/n2, 2)) )
            stat = stats.t.ppf(1-alpha/2, degrees_freedom)

        interval = []
        interval.append(mean_diff - (stat * standard_error))
        interval.append(mean_diff + (stat * standard_error))

        if is_z_score:
            stat_display = "Z-Score: "
            df = "N/A"
        else:
            stat_display = "T-Stat = "
            df = str(degrees_freedom)
        display = f'Important Statistics:\n\nx̄1 - x̄2 = {mean_diff}\n{stat_display}{stat}\nStandard Error = {standard_error}\nDegrees of Freedom = {df}'
        stats_label = tk.Label(self.root, text=display, font=("Helvetica", 14), bg="#FFFFF0", anchor='w')
        stats_label.place(relx=0.6, rely=0.2)
        
        self.__make_visualization(interval, alpha)

    def pooled_test(self, confidence, data):
        mean1 = data[0]
        n1 = data[1]
        var1 = data[2]

        mean2 = data[3]
        n2 = data[4]
        var2 = data[5]
        
        degrees_freedom = n1 + n2 - 2
        pooled_var = (((n1-1) * var1) + ((n2-1)*var2)) / degrees_freedom
        standard_error = math.sqrt(pooled_var)
        mean_diff = mean1-mean2
        alpha = self.__confidence_to_alpha(confidence)
        
        stat = stats.t.ppf(1-alpha/2, degrees_freedom)

        interval = []
        interval.append(mean_diff - (stat * standard_error))
        interval.append(mean_diff + (stat * standard_error))

        
        display = f'Important Statistics:\n\nx̄1 - x̄2 = {mean_diff}\nT-Stat = {stat}\nStandard Error = {standard_error}\nDegrees of Freedom = {degrees_freedom}'
        stats_label = tk.Label(self.root, text=display, font=("Helvetica", 14), bg="#FFFFF0", anchor='w')
        stats_label.place(relx=0.6, rely=0.2)
        
        self.__make_visualization(interval, alpha)

    