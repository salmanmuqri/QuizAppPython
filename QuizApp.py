import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")
        
        self.questions = [
            ("What does CPU stand for?", "Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Processor Unit", "Central Processing Unit"),
            # Add more questions here up to a total of 50
            ("Which language is primarily used for data science?", "Java", "C#", "Python", "C++", "Python"),
            # Add more questions here for testing
        ] * 25  # Multiplies the question for the test; replace with 50 unique questions

        self.user_database = {}  # To store user ID, name, and score
        self.random_questions = []
        self.current_question_index = 0
        self.score = 0

        # Home Page
        self.show_home_page()

    def show_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.root, text="Check Score", command=self.check_score).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.exit_quiz).pack(pady=10)

    def start_quiz(self):
        self.user_name = simpledialog.askstring("Name", "Enter your name:")
        if not self.user_name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        self.user_id = f"U{random.randint(1000, 9999)}"
        messagebox.showinfo("Welcome", f"Welcome, {self.user_name}! Your ID is: {self.user_id}")

        # Select 10 random questions
        self.random_questions = random.sample(self.questions, 10)
        self.score = 0
        self.current_question_index = 0

        self.show_quiz_page()

    def show_quiz_page(self):
    # Clear previous question widgets
        for widget in self.root.winfo_children():
            widget.destroy()

    # Display the current question
        self.question_label = tk.Label(self.root, text=self.random_questions[self.current_question_index][0], wraplength=400)
        self.question_label.pack(pady=10)

    # Create a single StringVar for all options
        self.selected_answer = tk.StringVar(value="")  # Default empty, so no option is pre-selected

    # Display answer options with Radiobuttons
        for i in range(1, 5):
            option = tk.Radiobutton(self.root, text=self.random_questions[self.current_question_index][i], variable=self.selected_answer, value=self.random_questions[self.current_question_index][i])
            option.pack(anchor='w')

    # Next button
        tk.Button(self.root, text="Next", command=self.next_question).pack(pady=10)

    def next_question(self):
    # Get selected answer
        selected_answer = self.selected_answer.get()

    # Check if selected answer matches the correct answer
        correct_answer = self.random_questions[self.current_question_index][5]
        if selected_answer == correct_answer:
            self.score += 1
    
        # Move to the next question or end quiz
        self.current_question_index += 1
        if self.current_question_index < len(self.random_questions):
            self.show_quiz_page()
        else:
            self.end_quiz() 

    def end_quiz(self):
        messagebox.showinfo("Quiz Completed", f"{self.user_name}, your score is: {self.score}/10")
        self.user_database[self.user_id] = {'name': self.user_name, 'score': self.score}
        self.show_home_page()

    def check_score(self):
        user_id = simpledialog.askstring("ID Check", "Enter your ID:")
        if user_id in self.user_database:
            user_info = self.user_database[user_id]
            messagebox.showinfo("Score", f"Name: {user_info['name']}\nScore: {user_info['score']}/10")
        else:
            messagebox.showerror("Error", "User ID not found.")

    def exit_quiz(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
