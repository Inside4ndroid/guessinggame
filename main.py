import random
import tkinter as tk
from tkinter import messagebox

class GuessingGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Guessing Game")

        self.master.geometry("400x400")  # Set initial window size
        self.master.configure(bg='#3498db')  # Set background color to a shade of blue

        self.label = tk.Label(master, text="Welcome to the Guessing Game!", font=("Helvetica", 16), bg='#3498db', fg='white')
        self.label.pack(pady=20)

        self.difficulty_label = tk.Label(master, text="Choose difficulty level:", font=("Helvetica", 12), bg='#3498db', fg='white')
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar(master, value="1")
        self.difficulty_menu = tk.OptionMenu(master, self.difficulty_var, "1", "2", "3")
        self.difficulty_menu.config(font=("Helvetica", 12), bg='#3498db', fg='white')
        self.difficulty_menu.pack()

        self.game_type_button = tk.Button(master, text="Select Game Type", command=self.select_game_type, font=("Helvetica", 12), bg='#e67e22', fg='white')
        self.game_type_button.pack(pady=10)

        self.selected_game_type = tk.StringVar()  # Initialize the variable here

        self.start_button = tk.Button(master, text="Start New Game", command=self.start_game, font=("Helvetica", 14), bg='#2ecc71', fg='white')
        self.start_button.pack(pady=10)

        self.leave_button = tk.Button(master, text="Leave Game", command=self.leave_game, font=("Helvetica", 12), bg='#e74c3c', fg='white', state=tk.DISABLED)
        self.leave_button.pack(pady=10)

        self.instructions_button = tk.Button(master, text="View Instructions", command=self.view_instructions, font=("Helvetica", 12), bg='#f39c12', fg='white')
        self.instructions_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=self.master.destroy, font=("Helvetica", 12), bg='#e74c3c', fg='white')
        self.exit_button.pack(pady=10)

        self.game_widgets = []  # To store game-related widgets
        self.game_in_progress = False

    def select_game_type(self):
        game_types = ["Number Guessing", "Word Guessing"]  # Add more game types as needed

        # Create a Toplevel window for game type selection
        top_level = tk.Toplevel(self.master)
        top_level.title("Select Game Type")
        top_level.geometry("200x150")
        top_level.configure(bg='#3498db')

        label = tk.Label(top_level, text="Choose a game type:", font=("Helvetica", 12), bg='#3498db', fg='white')
        label.pack(pady=10)

        selected_type = tk.StringVar()

        for game_type in game_types:
            button = tk.Button(top_level, text=game_type, command=lambda t=game_type: selected_type.set(t), font=("Helvetica", 12), bg='#e67e22', fg='white')
            button.pack(pady=5)

        confirm_button = tk.Button(top_level, text="Confirm", command=top_level.destroy, font=("Helvetica", 12), bg='#2ecc71', fg='white')
        confirm_button.pack(pady=10)

        top_level.wait_window()

        if selected_type.get():
            self.label.config(text=f"Selected Game Type: {selected_type.get()}", font=("Helvetica", 12), bg='#3498db', fg='white')
            self.selected_game_type.set(selected_type.get())  # Update the instance variable

    def get_difficulty(self):
        return int(self.difficulty_var.get())

    def set_max_attempts(self, difficulty):
        if difficulty == 1:
            return 10
        elif difficulty == 2:
            return 7
        else:
            return 5

    def start_game(self):
        if self.game_in_progress:
            messagebox.showinfo("Error", "A game is already in progress. Finish or leave the current game.")
            return

        self.game_in_progress = True
        self.leave_button.config(state=tk.NORMAL)
        difficulty = self.get_difficulty()
        max_attempts = self.set_max_attempts(difficulty)

        if self.selected_game_type.get():
            if self.selected_game_type.get() == "Number Guessing":
                self.start_number_guessing_game(max_attempts)
            elif self.selected_game_type.get() == "Word Guessing":
                self.start_word_guessing_game(max_attempts)
        else:
            messagebox.showinfo("Error", "Please select a game type first.")

    def leave_game(self):
        self.game_in_progress = False
        self.leave_button.config(state=tk.DISABLED)
        self.label.config(text="Welcome to the Guessing Game!", font=("Helvetica", 16), bg='#3498db', fg='white')

        # Remove game-related widgets
        for widget in self.game_widgets:
            widget.destroy()

        self.game_widgets = []

    def start_number_guessing_game(self, max_attempts):
        secret_number = random.randint(1, 100)
        attempts = 0

        self.label.config(text=f"I have selected a number between 1 and 100. You have {max_attempts} attempts. Good luck!", font=("Helvetica", 12), bg='#3498db', fg='white')

        guess_label = tk.Label(self.master, text="Enter your guess:", font=("Helvetica", 12), bg='#3498db', fg='white')
        guess_label.pack()
        self.game_widgets.append(guess_label)

        guess_entry = tk.Entry(self.master, font=("Helvetica", 12))
        guess_entry.pack()
        self.game_widgets.append(guess_entry)

        submit_button = tk.Button(self.master, text="Submit Guess", command=lambda: make_guess(), font=("Helvetica", 14), bg='#3498db', fg='white')
        submit_button.pack(pady=20)
        self.game_widgets.append(submit_button)

        result_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg='#3498db', fg='white')
        result_label.pack()
        self.game_widgets.append(result_label)

        def make_guess():
            nonlocal attempts
            try:
                guess = int(guess_entry.get())
                attempts += 1

                if guess == secret_number:
                    result_label.config(text=f"Congratulations! You guessed the correct number in {attempts} attempts.", font=("Helvetica", 12), bg='#3498db', fg='white')
                    self.leave_game()
                elif guess < secret_number:
                    result_label.config(text="Too low! Try again.", font=("Helvetica", 12), bg='#3498db', fg='white')
                else:
                    result_label.config(text="Too high! Try again.", font=("Helvetica", 12), bg='#3498db', fg='white')

            except ValueError:
                result_label.config(text="Invalid input. Please enter a number.", font=("Helvetica", 12), bg='#3498db', fg='white')

            if attempts == max_attempts and guess != secret_number:
                result_label.config(text=f"Sorry, you've run out of attempts. The correct number was {secret_number}.", font=("Helvetica", 12), bg='#3498db', fg='white')
                self.leave_game()

    def start_word_guessing_game(self, max_attempts):
        word_list = ["python", "java", "ruby", "javascript", "html", "css", "php", "swift", "csharp"]
        secret_word = random.choice(word_list)
        attempts = 0

        self.label.config(text=f"I have selected a word. Try to guess it. You have {max_attempts} attempts. Good luck!", font=("Helvetica", 12), bg='#3498db', fg='white')

        guess_label = tk.Label(self.master, text="Enter your guess:", font=("Helvetica", 12), bg='#3498db', fg='white')
        guess_label.pack()
        self.game_widgets.append(guess_label)

        guess_entry = tk.Entry(self.master, font=("Helvetica", 12))
        guess_entry.pack()
        self.game_widgets.append(guess_entry)

        submit_button = tk.Button(self.master, text="Submit Guess", command=lambda: make_guess(), font=("Helvetica", 14), bg='#3498db', fg='white')
        submit_button.pack(pady=20)
        self.game_widgets.append(submit_button)

        result_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg='#3498db', fg='white')
        result_label.pack()
        self.game_widgets.append(result_label)

        def make_guess():
            nonlocal attempts
            try:
                guess = guess_entry.get().lower()
                attempts += 1

                if guess == secret_word:
                    result_label.config(text=f"Congratulations! You guessed the correct word '{secret_word}' in {attempts} attempts.", font=("Helvetica", 12), bg='#3498db', fg='white')
                    self.leave_game()
                else:
                    result_label.config(text="Incorrect! Try again.", font=("Helvetica", 12), bg='#3498db', fg='white')

            except ValueError:
                result_label.config(text="Invalid input.", font=("Helvetica", 12), bg='#3498db', fg='white')

            if attempts == max_attempts and guess != secret_word:
                result_label.config(text=f"Sorry, you've run out of attempts. The correct word was '{secret_word}'.", font=("Helvetica", 12), bg='#3498db', fg='white')
                self.leave_game()

    def view_instructions(self):
        instructions = (
            "Welcome to the Guessing Game!\n"
            "I have selected a random number between 1 and 100 or a word from a predefined list.\n"
            "Your task is to guess the correct number or word.\n"
            "After each guess, I will provide feedback on whether your guess is correct or incorrect.\n"
            "You can choose the difficulty level, which affects the maximum number of attempts:\n"
            "- Easy: 10 attempts\n"
            "- Medium: 7 attempts\n"
            "- Hard: 5 attempts\n"
            "Good luck!"
        )
        messagebox.showinfo("Instructions", instructions)

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameGUI(root)
    root.mainloop()
