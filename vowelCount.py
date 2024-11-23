import tkinter as tk
from tkinter import simpledialog


class VowelCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vowel Counter")

        # Button to open the text input dialog
        self.open_button = tk.Button(root, text="Enter Sentence", command=self.open_text_input)
        self.open_button.pack(pady=10)

        # Label to display the result
        self.result_label = tk.Label(root, text="Vowel count will appear here.")
        self.result_label.pack(pady=10)

    def open_text_input(self):
        # Open a dialog box for text input
        sentence = simpledialog.askstring("Input", "Enter your sentence:")
        if sentence:
            vowel_count = self.count_vowels(sentence)
            self.show_large_message(f"'{sentence}' contains {vowel_count} vowels.")
        else:
            self.show_large_message("No sentence entered.")

    def show_large_message(self, message):
        # Custom larger message box
        large_msg_box = tk.Toplevel(self.root)
        large_msg_box.title("Message")
        large_msg_box.geometry("400x200")  # Set the size of the window

        # Add message to the box
        label = tk.Label(large_msg_box, text=message, wraplength=350, font=("Helvetica", 14))
        label.pack(expand=True, pady=20)

        # Add an OK button to close the window
        ok_button = tk.Button(large_msg_box, text="OK", command=large_msg_box.destroy, font=("Helvetica", 12))
        ok_button.pack(pady=10)

    @staticmethod
    def count_vowels(sentence):
        # Count vowels in the sentence
        vowels = "aeiouAEIOU"
        return sum(1 for char in sentence if char in vowels)


if __name__ == "__main__":
    root = tk.Tk()
    app = VowelCounterApp(root)
    root.mainloop()


