import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random

class SettingsPage(tk.Frame):
    def __init__(self, master, home_callback, change_wallpaper_callback):
        super().__init__(master)
        self.master = master
        self.home_callback = home_callback
        self.change_wallpaper_callback = change_wallpaper_callback
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Settings Page", font=("Arial", 20))
        label.pack(pady=20)

        wallpaper_label = tk.Label(self, text="Wallpaper:", font=("Arial", 14))
        wallpaper_label.pack()

        self.wallpaper_options = ["bg1.jpg", "bg2.jpg", "bg3.jpg","bg4.jpg","bg5.jpg"]  # List of available wallpapers

        self.wallpaper_var = tk.StringVar()
        self.wallpaper_var.set(self.wallpaper_options[0])  # Default wallpaper
        wallpaper_menu = ttk.Combobox(self, textvariable=self.wallpaper_var, values=self.wallpaper_options, state="readonly")
        wallpaper_menu.pack()

        apply_wallpaper_button = tk.Button(self, text="Apply Wallpaper", command=self.apply_wallpaper)
        apply_wallpaper_button.pack(pady=10)

        brightness_label = tk.Label(self, text="Brightness:", font=("Arial", 14))
        brightness_label.pack()

        self.brightness_var = tk.DoubleVar()
        self.brightness_var.set(1.0)  # Default brightness
        brightness_scale = tk.Scale(self, from_=0.5, to=1.5, resolution=0.1, orient=tk.HORIZONTAL, variable=self.brightness_var, label="Adjust brightness")
        brightness_scale.pack()

        apply_brightness_button = tk.Button(self, text="Apply Brightness", command=self.apply_brightness)
        apply_brightness_button.pack(pady=10)

        home_button = tk.Button(self, text="Home", command=self.go_to_home)
        home_button.pack(pady=10)

    def apply_wallpaper(self):
        selected_wallpaper = self.wallpaper_var.get()
        self.change_wallpaper_callback(selected_wallpaper)

    def apply_brightness(self):
        new_brightness = self.brightness_var.get()
        self.master.master.update_brightness(new_brightness)

    def go_to_home(self):
        self.home_callback()

class NumberGuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.geometry("500x400")

        self.sidebar = tk.Frame(self, bg="gray", width=100)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)

        self.main_content = tk.Frame(self)
        self.main_content.pack(fill=tk.BOTH, expand=True)

        self.current_wallpaper = "bg2.jpg"  # Default wallpaper
        self.current_brightness = 1.0  # Default brightness
        self.create_sidebar_widgets()
        self.show_main_page()

    def create_sidebar_widgets(self):
        settings_button = tk.Button(self.sidebar, text="Settings", command=self.show_settings)
        settings_button.pack(pady=10)

    def show_settings(self):
        self.clear_main_content()
        settings_page = SettingsPage(self.main_content, self.show_main_page, self.change_wallpaper) #settings page class is called
        settings_page.pack(fill=tk.BOTH, expand=True)

    def change_wallpaper(self, wallpaper):
        self.current_wallpaper = wallpaper
        self.update_wallpaper()

    def update_brightness(self, brightness):
        self.current_brightness = brightness
        self.update_wallpaper()

    def update_wallpaper(self):
        bg_image = Image.open(self.current_wallpaper)
        bg_image = bg_image.point(lambda p: p * self.current_brightness)
        bg_photo = ImageTk.PhotoImage(bg_image) # convert the pil image to tkinter supported format

        bg_label = tk.Label(self.main_content, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def show_main_page(self):
        self.clear_main_content()
        self.update_wallpaper()

        welcome_label = tk.Label(self.main_content, text="Welcome to Guessatron", font=("Arial", 20), bg="white")
        welcome_label.pack(pady=20)

        welcome_label = tk.Label(self.main_content, text="A Number guessing game", font=("Arial", 15), bg="white")
        welcome_label.pack()

        level_label = tk.Label(self.main_content, text="Choose your level", font=("Arial", 14), bg="white")
        level_label.pack()

        frame = tk.Frame(self.main_content, bg="black")
        frame.pack(pady=10)

        easy_button = tk.Button(frame, text="Easy", width=10, command=lambda: self.start_game("Easy"))
        easy_button.grid(row=0, column=0, padx=10)

        hard_button = tk.Button(frame, text="Hard", width=10, command=lambda: self.start_game("Hard"))
        hard_button.grid(row=0, column=1, padx=10)

        expert_button = tk.Button(frame, text="Expert", width=10, command=lambda: self.start_game("Expert"))
        expert_button.grid(row=0, column=2, padx=10)

        exit_button = tk.Button(self.main_content, text="Exit", command=self.exit_game)
        exit_button.pack(pady=10)

    def start_game(self, difficulty):
        self.clear_main_content()
        game_page = GamePage(self.main_content, difficulty, self.current_wallpaper, self.current_brightness) #gamescreen launched here
        game_page.pack(fill=tk.BOTH, expand=True)

    def exit_game(self):
        self.destroy()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

class GamePage(tk.Frame):
    def __init__(self, master, difficulty, wallpaper, brightness):
        super().__init__(master)
        self.master = master
        self.difficulty = difficulty
        self.wallpaper = wallpaper
        self.brightness = brightness
        self.attempts_left = self.get_max_attempts(difficulty)
        self.create_widgets()
        self.secret_number = random.randint(1, 100)

    def create_widgets(self):
        bg_image = Image.open(self.wallpaper)
        bg_image = bg_image.point(lambda p: p * self.brightness)

        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0)

        # Label to display the selected level name
        level_display_label = tk.Label(self, text=f"Selected Level: {self.difficulty}", font=("Arial", 12), bg="white")
        level_display_label.pack(pady=10)

        guess_label = tk.Label(self, text="Guess a number between 1 and 100:", font=("Arial", 14), bg="white")
        guess_label.pack(pady=10)
        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack()

        self.message_box = tk.Label(self, text="", font=("Arial", 12), bg="white")
        self.message_box.pack(pady=10)

        guess_button = tk.Button(self, text="Guess", command=self.check_guess)
        guess_button.pack(pady=5)

        button_frame = tk.Frame(self, bg="black")
        button_frame.pack()

        exit_button = tk.Button(button_frame, text="Exit", command=self.exit_game)
        exit_button.pack(side=tk.LEFT, padx=10, pady=5)

        back_button = tk.Button(button_frame, text="Back", command=self.go_to_home)
        back_button.pack(side=tk.LEFT, pady=5)

    def get_max_attempts(self, difficulty):
        if difficulty == "Easy":
            return 10
        elif difficulty == "Hard":
            return 7
        elif difficulty == "Expert":
            return 4

    def check_guess(self):
        if self.attempts_left > 1:
            guess = self.guess_entry.get()
            if guess.isdigit():
                guess = int(guess)
                if 1 <= guess <= 100:
                    self.attempts_left -= 1
                    if guess < self.secret_number:
                        self.message_box.config(text=f"Guess a higher number. {self.attempts_left} attempts left.")
                    elif guess > self.secret_number:
                        self.message_box.config(text=f"Guess a lower number. {self.attempts_left} attempts left.")
                    else:
                        messagebox.showinfo("Congratulations!", "Yay! You won!")
                        self.master.master.show_main_page()
                else:
                    self.message_box.config(text="Please enter a number between 1 and 100.")
            else:
                self.message_box.config(text="Please enter a valid number.")
        else:
            self.message_box.config(text="No attempts left. Game over.")
            self.guess_entry.config(state="disabled")
            messagebox.showinfo("Game Over", f"The secret number was {self.secret_number}. Game over.")

        self.guess_entry.delete(0, tk.END)


    def exit_game(self):
        self.master.master.exit_game()

    def go_to_home(self):
        self.master.master.show_main_page()


if __name__ == "__main__":
    app = NumberGuessingGame()
    app.mainloop()