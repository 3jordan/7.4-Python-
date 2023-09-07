import customtkinter as ctk
from http.client import HTTPConnection
import os
import shutil
from tkinter import filedialog
from tkinter import messagebox as mb
import tkinter as tk
from tkinter import simpledialog, messagebox, font
from dataclasses import dataclass
import random


@dataclass
class Contact:
    name: str
    email: str
    phone: str
    is_favorite: bool


contact_list = []


def online_site(url, timeout=2):
    try:
        connection = HTTPConnection(url, timeout=timeout)
        connection.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        connection.close()


def read_user_input():
    print("Enter the site names one by one ):")
    urls = []
    while True:
        url = input("Site name: ").strip()
        if url.lower() == "done":
            break
        urls.append(url)
    return urls


def display_check_result(result, url):
    print(f'The status of "{url}" is:', end=" ")
    if result:
        print('"Online!" 👍')
    else:
        print('"Offline?" 👎')


def synchronous_check(urls):
    for url in urls:
        result = online_site(url)
        display_check_result(result, url)


def open_file():
    string = filedialog.askopenfilename()
    if string:
        try:
            os.startfile(string)
        except:
            mb.showinfo("confirmation", "File not found!")


def copy_file():
    source1 = filedialog.askopenfilename()
    if not source1:
        return
    destination1 = filedialog.askdirectory()
    if not destination1:
        return
    shutil.copy(source1, destination1)
    mb.showinfo("confirmation", "File Copied! ")


def move_file():
    source2 = filedialog.askopenfilename()
    if not source2:
        return
    destination2 = filedialog.askdirectory()
    if not destination2:
        return
    shutil.move(source2, destination2)
    mb.showinfo("confirmation", "File Moved! ")


def rename_file():
    source3 = filedialog.askopenfilename()
    if not source3:
        return
    destination3 = filedialog.asksaveasfilename()
    if not destination3:
        return
    os.rename(source3, destination3)
    mb.showinfo("confirmation", "File Renamed! ")


def delete_file():
    source4 = filedialog.askopenfilename()
    if not source4:
        return
    if mb.askyesno("Confirmation", "Are you sure you want to delete this file?"):
        os.remove(source4)
        mb.showinfo("confirmation", "File Deleted! ")


def make_folder():
    folder_name = filedialog.askdirectory()
    if folder_name:
        try:
            os.mkdir(folder_name)
            mb.showinfo("Confirmation", "Folder Created!")
        except FileExistsError:
            mb.showerror("Error", f'The folder "{folder_name}" already exists.')
        except Exception as e:
            mb.showerror("Error", f"An error occurred: {e}")


def remove_folder():
    folder_name2 = filedialog.askdirectory()
    if not folder_name2:
        return
    if mb.askyesno("Confirmation", "Are you sure you want to remove this folder?"):
        os.rmdir(folder_name2)
        mb.showinfo("confirmation", "Folder Removed! ")


def list_files():
    folder_name3 = filedialog.askdirectory()
    if not folder_name3:
        return
    files = os.listdir(folder_name3)
    file_list = "\n".join(files)
    mb.showinfo("Files in Directory", file_list)


def create_contact():
    global new_window

    def save_contact():
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        is_favorite = favorite_var.get()
        contact = Contact(name, email, phone, is_favorite)
        contact_list.append(contact)
        update_contact_listbox()
        messagebox.showinfo("Success", "Contact created successfully.")
        create_window.destroy()

    create_window = ctk.CTkToplevel()
    create_window.title("Create Contact")
    create_window.attributes("-topmost", True)

    name_label = ctk.CTkLabel(create_window, text="Name:")
    name_label.pack()

    name_entry = ctk.CTkEntry(create_window)
    name_entry.pack()

    email_label = ctk.CTkLabel(create_window, text="Email:")
    email_label.pack()

    email_entry = ctk.CTkEntry(create_window)
    email_entry.pack()

    phone_label = ctk.CTkLabel(create_window, text="Phone:")
    phone_label.pack()

    phone_entry = ctk.CTkEntry(create_window)
    phone_entry.pack()

    favorite_var = tk.BooleanVar()
    favorite_var.set(False)
    favorite_label = ctk.CTkLabel(create_window, text="Favorite:")
    favorite_label.pack()

    favorite_checkbox = ctk.CTkCheckBox(
        create_window, text="Favorite", variable=favorite_var
    )
    favorite_checkbox.pack()

    save_button = ctk.CTkButton(create_window, text="Save", command=save_contact)
    save_button.pack()


def format_contact(contact):
    return f"Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}\nFavorite: {contact.is_favorite}\n"


def format_contact_for_listbox(contact):
    return f"{contact.name} - {contact.email} - {contact.phone}"


def view_all():
    contacts_text.delete(1.0, ctk.END)
    if not contact_list:
        contacts_text.insert(ctk.END, "No contacts found.")
    else:
        for contact in contact_list:
            contacts_text.insert(ctk.END, format_contact(contact))


def search_by_name():
    def view_name():
        contacts_text.delete(1.0, ctk.END)
        search_result = []
        contact_name = name_entry.get().lower()
        for contact in contact_list:
            if contact_name in contact.name.lower():
                search_result.append(contact)
        if search_result:
            for contact in search_result:
                contacts_text.insert(ctk.END, format_contact(contact) + "\n")
        else:
            contacts_text.insert(ctk.END, "Contact not found.")

    search_window = ctk.CTkToplevel()
    search_window.title("Search by Name")
    search_window.attributes("-topmost", True)

    name_label = ctk.CTkLabel(search_window, text="Enter Name:")
    name_label.pack()

    name_entry = ctk.CTkEntry(search_window)
    name_entry.pack()

    search_button = ctk.CTkButton(search_window, text="Search", command=view_name)
    search_button.pack()


def view_favorites():
    contacts_text.delete(1.0, ctk.END)
    search_result = [contact for contact in contact_list if contact.is_favorite]
    if search_result:
        for contact in search_result:
            contacts_text.insert(ctk.END, format_contact(contact) + "\n")
    else:
        contacts_text.insert(ctk.END, "You have no favorites.")


def update_contact_details():
    def update_contact():
        update_name = name_entry.get().lower()
        for contact in contact_list:
            if update_name == contact.name.lower():
                update_name = simpledialog.askstring("Name", "Enter Name:")
                update_email = simpledialog.askstring("Email", "Enter Email:")
                update_phone = simpledialog.askstring("Phone", "Enter Phone:")
                update_favorite = simpledialog.askstring(
                    "Favorite", "Favorite(Y or N)?"
                )
                contact.name = update_name
                contact.email = update_email
                contact.phone = update_phone
                if update_favorite.lower() == "y":
                    contact.is_favorite = "Yes"
                elif update_favorite.lower() == "n":
                    contact.is_favorite = "No"
                update_contact_listbox()
                messagebox.showinfo("Success", "Contact updated successfully.")
                return
        messagebox.showinfo("Contact Not Found", "Contact not found.")

    update_window = ctk.CTkToplevel()
    update_window.title("Update Contact Details")
    update_window.attributes("-topmost", True)

    name_label = ctk.CTkLabel(update_window, text="Enter Name:")
    name_label.pack()

    name_entry = ctk.CTkEntry(update_window)
    name_entry.pack()

    update_button = ctk.CTkButton(update_window, text="Update", command=update_contact)
    update_button.pack()


def delete_contact():
    delete_name = name_entry.get().lower()
    for contact in contact_list:
        if delete_name == contact.name.lower():
            contact_list.remove(contact)
            update_contact_listbox()
            messagebox.showinfo("Success", "Contact deleted successfully.")
            return
    messagebox.showinfo("Contact Not Found", "Contact not found.")


def update_contact_listbox():
    contact_listbox.delete(0, tk.END)
    for contact in contact_list:
        contact_listbox.insert(tk.END, format_contact_for_listbox(contact))


def on_close_contacts(contacts_window):
    if messagebox.askokcancel("Quit", "Do you want to close the Contacts List?"):
        contacts_window.destroy()


def contacts_list_window(root):
    global contact_listbox, contacts_text, name_entry, contacts_window

    if not hasattr(root, "_contacts_window"):
        contacts_window = ctk.CTkToplevel(root)
        contacts_window.title("Contacts List")
        contacts_window.protocol(
            "WM_DELETE_WINDOW", lambda: on_close_contacts(contacts_window)
        )
        root._contacts_window = contacts_window

    contact_listbox = tk.Listbox(contacts_window, width=45, height=10, font=4)
    contact_listbox.pack(padx=10, pady=10)

    contacts_text = ctk.CTkTextbox(contacts_window, width=375, height=60)
    contacts_text.pack(padx=10, pady=10)

    create_button = ctk.CTkButton(
        contacts_window, text="Create", command=create_contact
    )
    create_button.pack(pady=5)

    view_all_button = ctk.CTkButton(contacts_window, text="View All", command=view_all)
    view_all_button.pack(pady=5)

    search_by_name_button = ctk.CTkButton(
        contacts_window, text="Search by Name", command=search_by_name
    )
    search_by_name_button.pack(pady=5)

    view_favorites_button = ctk.CTkButton(
        contacts_window, text="View Favorites", command=view_favorites
    )
    view_favorites_button.pack(pady=5)

    update_contact_details_button = ctk.CTkButton(
        contacts_window, text="Update Contact Details", command=update_contact_details
    )
    update_contact_details_button.pack(pady=5)

    delete_contact_button = ctk.CTkButton(
        contacts_window, text="Delete Contact", command=delete_contact
    )
    delete_contact_button.pack(pady=5)

    update_contact_listbox()

    return contacts_window


global player


def toggle_player():
    global player
    player = "X" if player == "O" else "O"
    update_status_label()


def update_status_label():
    status_label.config(text=f"Player {player}'s turn")


def make_move(row, col):
    global board, player
    if board[row][col] == "":
        board[row][col] = player
        update_game_buttons()
        check_winner()
        toggle_player()


def update_game_buttons():
    for row in range(3):
        for col in range(3):
            button = board_buttons[row][col]
            button.config(
                text=board[row][col],
                state=tk.DISABLED if board[row][col] != "" else tk.NORMAL,
            )


def check_winner():
    global board
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            highlight_winner_cells([(board.index(row), i) for i in range(3)])
            update_score(row[0])
            mb.showinfo("Game Over", f"Player {row[0]} wins!")
            reset_game()
            return

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            highlight_winner_cells([(i, col) for i in range(3)])
            update_score(board[0][col])
            mb.showinfo("Game Over", f"Player {board[0][col]} wins!")
            reset_game()
            return

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        highlight_winner_cells([(i, i) for i in range(3)])
        update_score(board[0][0])
        mb.showinfo("Game Over", f"Player {board[0][0]} wins!")
        reset_game()
        return

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        highlight_winner_cells([(i, 2 - i) for i in range(3)])
        update_score(board[0][2])
        mb.showinfo("Game Over", f"Player {board[0][2]} wins!")
        reset_game()
        return

    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        update_status_label()
        mb.showinfo("Game Over", "It's a draw!")
        reset_game()


def highlight_winner_cells(cells):
    for row, col in cells:
        board_buttons[row][col].config(bg="yellow")


def update_score(winner):
    scores[winner] += 1
    score_label.config(text=f"X: {scores['X']}    O: {scores['O']}")


def reset_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for row in board_buttons:
        for button in row:
            button.config(text="", state=tk.NORMAL, bg="white")
    update_status_label()


def start_tic_tac_toe_game():
    ttt_window = tk.Tk()
    ttt_window.title("Tic Tac Toe")

    global board_buttons, status_label, score_label, board, player, scores
    board_buttons = [[None for _ in range(3)] for _ in range(3)]
    board = [["" for _ in range(3)] for _ in range(3)]
    player = "X"
    scores = {"X": 0, "O": 0}

    for row in range(3):
        for col in range(3):
            button = tk.Button(
                ttt_window,
                text="",
                width=10,
                height=3,
                command=lambda r=row, c=col: make_move(r, c),
            )
            button.grid(row=row, column=col)
            board_buttons[row][col] = button

    status_label = tk.Label(ttt_window, text="", font=("Helvetica", 12))
    status_label.grid(row=3, column=0, columnspan=3)

    score_label = tk.Label(ttt_window, text="X: 0    O: 0", font=("Helvetica", 12))
    score_label.grid(row=4, column=0, columnspan=3)

    update_status_label()


expenses = []
incomes = []


def add_expense():
    expense_name = name_entry.get()
    expense_amount = float(amount_entry.get())
    expenses.append((expense_name, expense_amount))
    update_expense_list()
    update_total_income()


def add_income():
    income_name = income_name_entry.get()
    income_amount = float(income_amount_entry.get())
    incomes.append((income_name, income_amount))
    update_income_list()
    update_total_income()


def update_expense_list():
    expense_list.delete(0, tk.END)
    for expense in expenses:
        expense_list.insert(tk.END, f"{expense[0]}: ${expense[1]:.2f}")


def update_income_list():
    income_list.delete(0, tk.END)
    for income in incomes:
        income_list.insert(tk.END, f"{income[0]}: ${income[1]:.2f}")


def update_total_income():
    total_income = sum(income[1] for income in incomes)
    total_expenses = sum(expense[1] for expense in expenses)
    remaining_income = total_income - total_expenses
    remaining_income_label.configure(text=f"Remaining Income: ${remaining_income:.2f}")


def calculate_percentages():
    total_income = sum(income[1] for income in incomes)
    percentage_frame = ctk.CTkFrame(root)
    percentage_frame.pack()

    for income in incomes:
        income_percentage = (income[1] / total_income) * 100
        label = ctk.CTkLabel(
            percentage_frame,
            text=f"{income[0]}: {income_percentage:.2f}%",
            font=("Helvetica", 12),
        )
        label.pack()

    total_expense = sum(expense[1] for expense in expenses)
    for expense in expenses:
        expense_percentage = (expense[1] / total_expense) * 100
        label = ctk.CTkLabel(
            percentage_frame,
            text=f"{expense[0]}: {expense_percentage:.2f}%",
            font=("Helvetica", 12),
        )
        label.pack()


def expense_tracker_window():
    global remaining_income_label, name_entry, name_label, root, income_list, income_amount_label, income_name_label, income_name_entry, income_amount_entry, expense_list, amount_entry
    root = ctk.CTk()
    root.title("Expense Tracker")

    name_label = ctk.CTkLabel(root, text="Expense Name:")
    name_label.pack()

    name_entry = ctk.CTkEntry(root)
    name_entry.pack()

    amount_label = ctk.CTkLabel(root, text="Expense Amount:")
    amount_label.pack()

    amount_entry = ctk.CTkEntry(root)
    amount_entry.pack()

    add_button = ctk.CTkButton(root, text="Add Expense", command=add_expense)
    add_button.pack()

    income_name_label = ctk.CTkLabel(root, text="Income Source:")
    income_name_label.pack()

    income_name_entry = ctk.CTkEntry(root)
    income_name_entry.pack()

    income_amount_label = ctk.CTkLabel(root, text="Income Amount:")
    income_amount_label.pack()

    income_amount_entry = ctk.CTkEntry(root)
    income_amount_entry.pack()

    add_income_button = ctk.CTkButton(root, text="Add Income", command=add_income)
    add_income_button.pack()

    remaining_income_label = ctk.CTkLabel(root, text="Remaining Income: $0.00")
    remaining_income_label.pack()

    show_percentages_button = ctk.CTkButton(
        root, text="Show Income and Expense Percentages", command=calculate_percentages
    )
    show_percentages_button.pack()

    expense_list = tk.Listbox(root, font=("Helvetica", 12), width=40, height=10)
    expense_list.pack()

    income_list = tk.Listbox(root, font=("Helvetica", 12), width=40, height=10)
    income_list.pack()

    root.mainloop()


class HangmanGame:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Hangman Game")

        self.secret_word = self.generate_secret_word()
        self.guesses = []
        self.max_attempts = 6
        self.remaining_attempts = self.max_attempts

        self.word_label = ctk.CTkLabel(
            self.window,
            text=" ".join(["_"] * len(self.secret_word)),
            font=("Helvetica", 24),
        )
        self.word_label.pack(pady=10)

        self.guess_label = ctk.CTkLabel(
            self.window, text="Enter a letter:", font=("Helvetica", 14)
        )
        self.guess_label.pack(pady=5)

        self.guess_entry = ctk.CTkEntry(self.window, font=("Helvetica", 14))
        self.guess_entry.pack(pady=5)

        self.submit_button = ctk.CTkButton(
            self.window, text="Guess", font=("Helvetica", 14), command=self.on_guess
        )
        self.submit_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.window, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=5)

        self.update_word_label()
        self.window.mainloop()

    def generate_secret_word(self):
        word_list = word_list = [
            "apple",
            "banana",
            "cherry",
            "grape",
            "melon",
            "orange",
            "peach",
            "pear",
            "plum",
            "lemon",
            "kiwi",
            "berry",
            "fruit",
            "mango",
            "guava",
            "papaya",
            "water",
            "apricot",
            "avocado",
            "juicy",
            "tasty",
            "sweet",
            "sour",
            "flavor",
            "pineapple",
            "blueberry",
            "blackberry",
            "strawberry",
            "raspberry",
            "coconut",
            "lime",
            "fig",
            "dragonfruit",
            "kiwifruit",
            "pomegranate",
            "passionfruit",
            "cat",
            "dog",
            "elephant",
            "giraffe",
            "lion",
            "tiger",
            "zebra",
            "penguin",
            "monkey",
            "kangaroo",
            "dolphin",
            "whale",
            "shark",
            "turtle",
            "ostrich",
            "ocean",
            "forest",
            "mountain",
            "desert",
            "beach",
            "castle",
            "rainbow",
            "unicorn",
            "wizard",
            "planet",
            "moon",
            "star",
            "spaceship",
            "astronaut",
        ]
        return random.choice(word_list)
        return random.choice(word_list)

    def update_word_label(self):
        display_word = [
            letter if letter in self.guesses else "_" for letter in self.secret_word
        ]
        self.word_label.configure(text=" ".join(display_word))

    def on_guess(self):
        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            self.result_label.configure(text="Please enter a valid letter.")
            return

        if guess in self.guesses:
            self.result_label.configure(text="You already guessed that letter.")
            return

        self.guesses.append(guess)
        self.update_word_label()

        if guess in self.secret_word:
            self.result_label.configure(text="Good guess!")
        else:
            self.result_label.configure(text="Wrong guess!")
            self.remaining_attempts -= 1

        if self.remaining_attempts == 0:
            self.result_label.configure(
                text=f"Game over! The word was {self.secret_word}."
            )
            self.guess_entry.configure(state=tk.DISABLED)
            self.submit_button.configure(state=tk.DISABLED)
        elif "_" not in self.word_label.cget("text"):
            self.result_label.configure(text="Congratulations! You guessed the word.")
            self.guess_entry.configure(state=tk.DISABLED)
            self.submit_button.configure(state=tk.DISABLED)
        else:
            self.result_label.configure(
                text=f"Remaining attempts: {self.remaining_attempts}"
            )


projects_per_category = {
    "File and Data Management": ["Site Connectivity Checker", "File Manager"],
    "Personal Organization": ["Contact Book", "Expense Tracker"],
    "Games": ["Hangman", "Tic-Tac-Toe"],
}


def open_category_window(category, main_frame, root):
    new_window = ctk.CTkToplevel(root)
    new_window.title(f"{category} Projects")

    for idx, project in enumerate(projects_per_category.get(category, [])):
        project_button = ctk.CTkButton(
            new_window,
            text=project,
            command=lambda p=project: open_project_window(p, root),
        )
        project_button.pack(pady=5)


def open_project_window(project, root):
    if project == "Contact Book":
        contacts_list_window(root)
    elif project == "Tic-Tac-Toe":
        None
    elif project == "Expense Tracker":
        None
    elif project == "Hangman":
        None
    else:
        new_window = ctk.CTkToplevel(root)
        new_window.title(f"{project}")
        new_window.attributes("-topmost", True)

    if project == "Site Connectivity Checker":
        ctk.CTkLabel(new_window, text="Enter the site names one by one:").pack(pady=10)

        site_names_entry = ctk.CTkEntry(new_window)
        site_names_entry.pack(pady=5)

        result_label = ctk.CTkLabel(new_window, text="")
        result_label.pack(pady=10)

        def check_sites():
            sites = site_names_entry.get().strip()
            if not sites:
                tk.messagebox.showerror("Error", "No site names provided.")
                return

            sites_list = sites.split()
            for site in sites_list:
                result = online_site(site)
                status = "Online 👍" if result else "Offline 👎"
                result_label.configure(
                    text=result_label.cget("text") + f"{site}: {status}\n"
                )

        check_button = ctk.CTkButton(
            new_window, text="Check Sites", command=check_sites
        )
        check_button.pack(pady=5)

    elif project == "File Manager":
        frame = ctk.CTkFrame(new_window)
        frame.pack()

        ctk.CTkLabel(frame, text="File Manager", font=("Helvetica", 16)).pack()

        ctk.CTkButton(frame, text="Open a File", command=open_file).pack(pady=5)

        ctk.CTkButton(frame, text="Copy a File", command=copy_file).pack(pady=5)

        ctk.CTkButton(frame, text="Move a File", command=move_file).pack(pady=5)

        ctk.CTkButton(frame, text="Rename a File", command=rename_file).pack(pady=5)

        ctk.CTkButton(frame, text="Delete a File", command=delete_file).pack(pady=5)

        ctk.CTkButton(frame, text="Make a Folder", command=make_folder).pack(pady=5)

        ctk.CTkButton(frame, text="Remove a Folder", command=remove_folder).pack(pady=5)

        ctk.CTkButton(
            frame, text="List all Files in Directory", command=list_files
        ).pack(pady=5)

    elif project == "Contact Book":
        contacts_window = contacts_list_window(new_window)
        contacts_window.grab_set()

    elif project == "Tic-Tac-Toe":
        start_tic_tac_toe_game()
    elif project == "Expense Tracker":
        expense_tracker_window()
    elif project == "Hangman":
        HangmanGame()


def show_projects(category, root):
    projects_window = tk.Toplevel(root)
    projects_window.title(f"{category} Projects")

    for project in projects_per_category[category]:
        project_button = ctk.CTkButton(
            projects_window,
            text=project,
            command=lambda p=project: open_project_window(p, projects_window),
        )
        project_button.pack(pady=5)

    back_button = ctk.CTkButton(
        projects_window, text="Back", command=projects_window.destroy
    )
    back_button.pack(pady=5)


def main_window():
    main_window = ctk.CTk()
    main_window.title("Software Suite")
    categories = ["File and Data Management", "Personal Organization", "Games"]

    for category in categories:
        category_button = ctk.CTkButton(
            main_window,
            text=category,
            command=lambda cat=category: show_projects(cat, main_window),
        )
        category_button.pack(pady=5)

    main_window.mainloop()


if __name__ == "__main__":
    main_window()
