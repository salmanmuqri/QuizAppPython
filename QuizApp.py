import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import uuid
import pickle
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")

        # 50 Unique IT Engineering Questions
        self.questions = [
            ("What does CPU stand for?", "Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Processor Unit", "Central Processing Unit"),
            ("What is the primary function of an operating system?", "Data storage", "User authentication", "Process management", "Email handling", "Process management"),
            ("Which language is primarily used for web development?", "Python", "HTML", "Java", "C++", "HTML"),
            ("What does RAM stand for?", "Random Access Memory", "Read Access Memory", "Random Allowed Memory", "Read Allowed Memory", "Random Access Memory"),
            ("Who is known as the father of computers?", "Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs", "Charles Babbage"),
            # Add 45 more questions here, each with 4 options and the correct answer at the end
        ]

        self.user_database = {}
        self.load_data()

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

        self.user_id = self.generate_unique_id()
        messagebox.showinfo("Welcome", f"Welcome, {self.user_name}! Your ID is: {self.user_id}")

        # Select 10 random, unique questions
        self.random_questions = random.sample(self.questions, 10)
        self.score = 0
        self.current_question_index = 0

        self.show_quiz_page()

    def show_quiz_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.question_label = tk.Label(self.root, text=self.random_questions[self.current_question_index][0], wraplength=400)
        self.question_label.pack(pady=10)

        self.selected_answer = tk.StringVar(value="")

        for i in range(1, 5):
            option = tk.Radiobutton(self.root, text=self.random_questions[self.current_question_index][i], variable=self.selected_answer, value=self.random_questions[self.current_question_index][i])
            option.pack(anchor='w')

        tk.Button(self.root, text="Next", command=self.next_question).pack(pady=10)

    def next_question(self):
        selected_answer = self.selected_answer.get()
        if not selected_answer:
            messagebox.showwarning("Warning", "Please select an answer before proceeding!")
            return

        correct_answer = self.random_questions[self.current_question_index][5]
        if selected_answer == correct_answer:
            self.score += 1

        self.current_question_index += 1
        if self.current_question_index < len(self.random_questions):
            self.show_quiz_page()
        else:
            self.end_quiz()

    def end_quiz(self):
        messagebox.showinfo("Quiz Completed", f"{self.user_name}, your score is: {self.score}/10")
        self.user_database[self.user_id] = {'name': self.user_name, 'score': self.score}
        self.save_data()
        
        if messagebox.askyesno("Return to Home", "Would you like to return to the home screen?"):
            self.show_home_page()
        else:
            self.root.quit()

    def check_score(self):
        user_id = simpledialog.askstring("ID Check", "Enter your ID:")
        if user_id in self.user_database:
            user_info = self.user_database[user_id]
            messagebox.showinfo("Score", f"Name: {user_info['name']}\nScore: {user_info['score']}/10")
        else:
            messagebox.showerror("Error", "User ID not found.")

    def exit_quiz(self):
        self.root.quit()

    def generate_unique_id(self):
        return "U" + uuid.uuid4().hex[:6]

    def save_data(self):
        with open("user_data.pkl", "wb") as file:
            pickle.dump(self.user_database, file)

    def load_data(self):
        if os.path.exists("user_data.pkl"):
            with open("user_data.pkl", "rb") as file:
                self.user_database = pickle.load(file)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
