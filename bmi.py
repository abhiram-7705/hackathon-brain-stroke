import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class CalorieEstimatorApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Calorie Estimator")
        self.root.configure(bg='yellow')

        self.main_frame = tk.Frame(root, bg="light blue")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.name_label = tk.Label(self.main_frame, text="Enter Name:", bg='gray', font=("Arial", 12, "bold"))
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.age_label = tk.Label(self.main_frame, text="Enter Age:", bg='gray', font=("Arial", 12, "bold"))
        self.age_label.grid(row=1, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.main_frame)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        self.gender_label = tk.Label(self.main_frame, text="Enter Gender:", bg='gray', font=("Arial", 12, "bold"))
        self.gender_label.grid(row=2, column=0, padx=10, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_var.set("Choose")
        self.gender_menu = tk.OptionMenu(self.main_frame, self.gender_var, "Male", "Female")
        self.gender_menu.config(bg='yellow', font=("Arial", 10, "bold"))
        self.gender_menu.grid(row=2, column=1, padx=10, pady=5)

        self.weight_label = tk.Label(self.main_frame, text="Enter Weight (kg):", bg='gray', font=("Arial", 12, "bold"))
        self.weight_label.grid(row=3, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(self.main_frame)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=5)

        self.height_label = tk.Label(self.main_frame, text="Enter Height (cm):", bg='gray', font=("Arial", 12, "bold"))
        self.height_label.grid(row=4, column=0, padx=10, pady=5)
        self.height_entry = tk.Entry(self.main_frame)
        self.height_entry.grid(row=4, column=1, padx=10, pady=5)

        self.calculate_button = tk.Button(self.main_frame, text="Calculate BMR", command=self.calculate_bmr, bg='yellow', font=("Arial", 12, "bold"))
        self.calculate_button.grid(row=5, column=0, padx=10, pady=5, columnspan=2)

        self.visualize_button = tk.Button(self.main_frame, text="Visualize", command=self.visualize, bg='yellow', font=("Arial", 12, "bold"))
        self.visualize_button.grid(row=6, column=0, padx=10, pady=5, columnspan=2)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=root.destroy, bg='yellow', font=("Arial", 12, "bold"))
        self.exit_button.grid(row=7, column=0, padx=10, pady=5, columnspan=2)

    def calculate_bmr(self):
        try:
            name = self.name_entry.get()
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
    
            if gender == "Female":
                self.bmr_value = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            else:
                self.bmr_value = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    
            messagebox.showinfo("BMR Result", f"Hey {name}, your BMR is: {self.bmr_value:.2f} calories/day.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for age, weight, and height.")
    
    def visualize(self):
        try:
            # Get user input for weight (assuming BMR already calculated in calculate_bmr)
            weight = float(self.weight_entry.get())
    
            # Calculate calories needed for weight goals based on user input and BMR
            maintain_weight = self.bmr_value
            mild_weight_loss = self.get_calories_for_weight_loss(self.bmr_value, 0.25)
            weight_loss = self.get_calories_for_weight_loss(self.bmr_value, 0.5)
            extreme_weight_loss = self.get_calories_for_weight_loss(self.bmr_value, 1)
    
            goals = ["Maintain weight", "Mild weight loss (0.25 kg/week)", "Weight loss (0.5 kg/week)", "Extreme weight loss (1 kg/week)"]
            calories = [maintain_weight, mild_weight_loss, weight_loss, extreme_weight_loss]
    
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(goals, calories, color=['blue', 'green', 'orange', 'red'])
            ax.set_xlabel('Weight Goals', fontweight='bold')
            ax.set_ylabel('Calories Needed (Cal/day)', fontweight='bold')
            ax.set_title('Daily Caloric Intake Based on Weight Goals (Bar Graph)', fontweight='bold')
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
            plt.tight_layout()  # Adjust layout to prevent cropping of axis labels
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
        
    def get_calories_for_weight_loss(self, bmr, loss_rate):
        # Formula to calculate calories needed for weight loss based on loss rate
        # Assuming 1 kg of fat is equivalent to 7700 calories
        return bmr - (loss_rate * 7700 / 7)  # Convert weekly loss to daily loss
    
if __name__ == "_main_":
    root = tk.Tk()
    app = CalorieEstimatorApp(root)
    root.mainloop()