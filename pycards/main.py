import math
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling the background image
import datetime
import time

from database import *

# database function
conn, cursor = initialize_connection()
userInfo = {}

class PyCards:
    def __init__(self, root):
        self.root = root
        self.root.title("PyCards")
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        # Configure grid layout
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Create main frame
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.side_panel_width = math.floor(self.width * 0.2)
        self.content_width = self.width - self.side_panel_width

        self.login()


    def login(self):
        def validate():
            # left_panel.grid_forget()
            # right_panel.grid_forget()
            # self.show_main()
            data = {}
            data['username'] = username.get()
            data['password'] = password.get()

            #database function
            result = login(cursor, data)
            if result is None:
                messagebox.showerror("Error", "* Login failed")
            else:
                global userInfo
                userInfo = result
                messagebox.showinfo("Success", "Login successful")
                self.left_panel.grid_forget()
                self.right_panel.grid_forget()
                self.show_main()

        def create():
            self.right_panel.grid_forget()
            self.create_account()

        ##### LEFT PANEL
        self.left_panel = tk.Frame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        # Load and display the background image
        image = Image.open("bg.jpg")  # Replace with your gradient image file
        image = image.resize((self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight()), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.left_panel,
                            text="Welcome to PyCards!\nEngage into fun and interactive learning with flashcards. \nReady to boost your knowledge? \nLet's get started! \U0001F604\U0001F31F",
                            font=("Arial", 26, "bold"),
                            bg="#ab23ff",
                            fg="white",
                            wraplength=800,
                            compound="center",
                            justify="center",
                            image=self.background_image)
        bg_label.place(relwidth=1, relheight=1)

        #### RIGHT PANEL
        self.right_panel = tk.Frame(self.main_frame, bg="white", padx=20, pady=20)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        form = tk.Frame(self.right_panel, bg="white", padx=20, pady=20)
        form.place(relx=0.5, rely=0.5, anchor="center")
        # Welcome text
        welcome_label = tk.Label(
            form, text="Welcome Back to \nPyCards!", font=("Arial", 24, "bold"), bg="white"
        )
        welcome_label.pack(pady=(10, 50))

        username = ctk.CTkEntry(master=form,
                                width=350,
                                height=30,
                                corner_radius=6,
                                placeholder_text='username',
                                bg_color='transparent',
                                fg_color='white',
                                text_color='black',
                                border_color='gray70',
                                border_width=1,
                                font=("Arial", 16)

                                )
        password = ctk.CTkEntry(master=form,
                                width=350,
                                height=30,
                                corner_radius=6,
                                placeholder_text='password',
                                bg_color='transparent',
                                fg_color='white',
                                text_color='black',
                                border_color='gray70',
                                border_width=1,
                                font=("Arial", 16)

                                )
        password.configure(show="*")
        username.pack(pady=5)
        password.pack(pady=5)
        # Login button
        LoginButton = ctk.CTkButton(
            master=form,
            text='Log In',
            font=('Open Sans', 16, 'bold'),
            fg_color='#8F00FF',
            hover_color='#800080',
            width=350,
            height=30,
            corner_radius=6,
            command=validate
        )
        LoginButton.pack(pady=20)
        line2 = tk.Label(form, text="---- Don't have an account? ----", font=('Arial', 10), fg='gray', bg='white')
        line2.pack()
        RegisterSwitchButton = ctk.CTkButton(
            master=form,
            text='Sign Up',
            font=('Open Sans', 16, 'bold'),
            fg_color='black',
            hover_color='#800080',
            width=350,
            height=30,
            corner_radius=6,
            command=create
        )
        RegisterSwitchButton.pack(pady=20)

    def create_account(self):
        def validate():
            error_messages = []
            has_upper = False
            has_lower = False
            has_digit = False
            has_special = False
            user_username = username.get()
            user_password = password.get()
            user_confirm_password = confirm_password.get()

            # database function
            if is_already_exist(cursor, user_username):
                error_messages.append("* Username already exist")
            if len(user_username) <=3:
                error_messages.append("* Username must be at least 4 characters long.")
            if user_password != user_confirm_password:
                error_messages.append("* Passwords not match")
            else:
                for char in user_password:
                    if char.isupper():
                        has_upper = True
                    if char.islower():
                        has_lower = True
                    if char.isdigit():
                        has_digit = True
                    if char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?~":
                        has_special = True
                if len(user_password) < 8:
                    error_messages.append("* Password must be at least 8 characters long.")
                if not has_upper:
                    error_messages.append("* Password must contain at least one uppercase letter.")
                if not has_lower:
                    error_messages.append("* Password must contain at least one lowercase letter.")
                if not has_digit:
                    error_messages.append("* Password must contain at least one digit.")
                if not has_special:
                    error_messages.append("* Password must contain at least one special character.")
            if len(error_messages) != 0:
                message = ''
                for error_message in error_messages:
                    message += error_message + "\n"
                messagebox.showerror("Error", message)
            else:
                data = {}
                data['username'] = user_username
                data['password'] = user_password

                # database function
                result = register(conn, cursor, data);
                if result is not None:
                    global userInfo
                    userInfo = result
                    messagebox.showinfo("Success", "Account created successfully")
                    self.left_panel.grid_forget()
                    self.right_panel.grid_forget()
                    self.show_main()
                else:
                    messagebox.showerror("Error", "* Account creation failed")

        def back_to_login():
            # left_panel.grid_forget()
            self.right_panel.grid_forget()
            self.login()

        ##### LEFT PANEL
        # left_panel = tk.Frame(self.main_frame)
        # left_panel.grid(row=0, column=0, sticky="nsew")
        # # Load and display the background image
        # image = Image.open("bg.jpg")  # Replace with your gradient image file
        # image = image.resize((self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight()), Image.LANCZOS)
        # self.background_image = ImageTk.PhotoImage(image)
        #
        # bg_label = tk.Label(left_panel,
        #                     text="Welcome to PyCards!\nEngage into fun and interactive learning with flashcards. \nReady to boost your knowledge? \nLet's get started! \U0001F604\U0001F31F",
        #                     font=("Arial", 26, "bold"),
        #                     bg="#ab23ff",
        #                     fg="white",
        #                     wraplength=800,
        #                     compound="center",
        #                     justify="center",
        #                     image=self.background_image)
        # bg_label.place(relwidth=1, relheight=1)

        #### RIGHT PANEL
        self.right_panel = tk.Frame(self.main_frame, bg="white", padx=20, pady=20)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        form = tk.Frame(self.right_panel, bg="white", padx=20, pady=20)
        form.place(relx=0.5, rely=0.5, anchor="center")
        # Welcome text
        welcome_label = tk.Label(
            form, text="Welcome Back to \nPyCards!", font=("Arial", 24, "bold"), bg="white"
        )
        welcome_label.pack(pady=(10, 20))

        # Login instruction
        login_instruction = tk.Label(
            form,
            text="Create an account",
            font=("Arial", 14, 'bold'),
            bg="white",
            fg="black",
        )
        login_instruction.pack(pady=(0, 10))
        login_instruction2 = tk.Label(
            form,
            text="Enter your username and password",
            font=("Arial", 12),
            bg="white",
            fg="black",
        )
        login_instruction2.pack(pady=(0, 10))

        # Username entry
        username = ctk.CTkEntry(master=form,
                                width=350,
                                height=30,
                                corner_radius=6,
                                placeholder_text='username',
                                bg_color='transparent',
                                fg_color='white',
                                text_color='black',
                                border_color='gray70',
                                border_width=1,
                                font=("Arial", 16)

                                )
        password = ctk.CTkEntry(master=form,
                                width=350,
                                height=30,
                                corner_radius=6,
                                placeholder_text='password',
                                bg_color='transparent',
                                fg_color='white',
                                text_color='black',
                                border_color='gray70',
                                border_width=1,
                                font=("Arial", 16)

                                )
        password.configure(show="*")
        confirm_password = ctk.CTkEntry(master=form,
                                        width=350,
                                        height=30,
                                        corner_radius=6,
                                        placeholder_text='confirm password',
                                        bg_color='transparent',
                                        fg_color='white',
                                        text_color='black',
                                        border_color='gray70',
                                        border_width=1,
                                        font=("Arial", 16)

                                        )
        confirm_password.configure(show="*")
        username.pack(pady=5)
        password.pack(pady=5)
        confirm_password.pack(pady=5)
        # Login button
        SignupButton = ctk.CTkButton(
            master=form,
            text='Sign Up',
            font=('Open Sans', 16, 'bold'),
            fg_color='black',
            hover_color='#800080',
            width=350,
            height=30,
            corner_radius=6,
            command=validate
        )
        SignupButton.pack(pady=20)
        line2 = tk.Label(form, text="---- Already have an account? ----", font=('Arial', 10), fg='gray', bg='white')
        line2.pack()
        LoginSwitchButton = ctk.CTkButton(
            master=form,
            text='Log In',
            font=('Open Sans', 16, 'bold'),
            fg_color='#8F00FF',
            hover_color='#800080',
            width=350,
            height=30,
            corner_radius=6,
            command=back_to_login
        )
        LoginSwitchButton.pack(pady=20)

    def show_main(self):
        def show_progress():
            if hasattr(self, 'main_component'):
                self.main_component.grid_forget()
            if hasattr(self, 'history'):
                self.history.grid_forget()
            if hasattr(self, 'selected_flashcard'):
                self.selected_flashcard.grid_forget()
            if hasattr(self, 'timer_running'):
                self.timer_running = False
            self.progress = ctk.CTkScrollableFrame(self.main_frame, fg_color="white")
            self.progress.columnconfigure(0, weight=1)
            self.progress.grid(row=0, column=1, sticky="nsew")
            flashcards = get_flashcards(cursor, userInfo["id"])
            if len(flashcards) != 0:
                for i in range(len(flashcards)):
                    card = ctk.CTkFrame(self.progress,fg_color="#6A4DA3")
                    card.grid(row=i, column=0, sticky="nsew", pady=20, padx=(0, 20))
                    card.bind("<Button-1>", lambda e, i=i : show_flashcard(flashcards[i]))
                    bg_label = ctk.CTkLabel(card,
                                        text=f"{flashcards[i]['name']}",
                                        font=("Arial", 26, "bold"),
                                        fg_color="#6A4DA3",
                                        text_color="white",
                                        justify="left")
                    bg_label.grid(row=0, column=0, sticky="nsw", pady=20, padx=20)
                    progress_bar = ctk.CTkProgressBar(card,
                                                      fg_color="gray",
                                                      progress_color="pink",
                                                      height=20,
                                                      width=900
                                                      )
                    progress_bar.grid(row=1, column=0, sticky="nsw", pady=20, padx=20)
                    if flashcards[i]['completed'] != 0:
                        progress_bar.set(round(flashcards[i]['completed']/flashcards[i]['total'], 2))
                        progress_bar.configure(progress_color="pink")
                    else:
                        progress_bar.set(0)
                        progress_bar.configure(progress_color="gray")
                    progress_label = ctk.CTkLabel(card,
                                                  text=f"{round(progress_bar.get() * 100)}%",
                                                  font=("Arial", 14, "bold"),
                                                  fg_color="#6A4DA3",
                                                  text_color="black"
                                                  )
                    progress_label.grid(row=1, column=1, sticky="nsw", pady=20, padx=20)

        def show_history():
            if hasattr(self, 'main_component'):
                self.main_component.grid_forget()
            if hasattr(self, 'progress'):
                self.progress.grid_forget()
            if hasattr(self, 'selected_flashcard'):
                self.selected_flashcard.grid_forget()
            if hasattr(self, 'timer_running'):
                self.timer_running = False
            self.history = ctk.CTkScrollableFrame(self.main_frame, fg_color="white")
            self.history.columnconfigure(0, weight=1)
            self.history.grid(row=0, column=1, sticky="nsew")

            header = ctk.CTkFrame(self.history, fg_color="white")
            header.grid(row=0, column=0, sticky="nsew", pady=20, padx=(0, 20))

            bg_label = ctk.CTkLabel(header,
                                text='"History: Where the past is always present."',
                                font=("Arial", 36, "bold"),
                                fg_color="white",
                                text_color="black",
                                justify="left")
            bg_label.grid(row=0, column=0, sticky="nsw", pady=20, padx=20)


            flashcards = get_flashcards(cursor, userInfo["id"])
            if len(flashcards) != 0:
                for i in range(len(flashcards)):
                    card = ctk.CTkFrame(self.history,fg_color="#6A4DA3")
                    card.grid(row=i+1, column=0, sticky="nsew", pady=10, padx=(0, 20))
                    card.bind("<Button-1>", lambda e, i=i : show_flashcard(flashcards[i]))
                    bg_label = ctk.CTkLabel(card,
                                        text=f"{flashcards[i]['name']}",
                                        font=("Arial", 26, "bold"),
                                        fg_color="#6A4DA3",
                                        text_color="white",
                                        justify="left")
                    bg_label.grid(row=0, column=0, sticky="nsw", pady=(20,0), padx=20)
                    deck_count_label = ctk.CTkLabel(card,
                                                  text=f"{flashcards[i]['total']} decks",
                                                  font=("Arial", 18, "bold"),
                                                  fg_color="#6A4DA3",
                                                  text_color="black"
                                                  )
                    deck_count_label.grid(row=1, column=0, sticky="nsw", pady=(0,20), padx=20)
                    progress_label = ctk.CTkLabel(card,
                                                  text=f"{flashcards[i]['completed']}/{flashcards[i]['total']}",
                                                  font=("Arial", 28, "bold"),
                                                  fg_color="#6A4DA3",
                                                  text_color="black"
                                                  )
                    progress_label.place(relx=0.96, rely=0.5, anchor="center")

        def show_flashcard(selected):
            response = check_flashcard_by_id(cursor, selected['id'])
            if len(response) != 0:
                message = ''
                for error_message in response:
                    message += error_message + "\n"
                messagebox.showinfo("Completed", message)
                return
            if hasattr(self, 'main_component'):
                self.main_component.grid_forget()
            if hasattr(self, 'selected_flashcard'):
                self.selected_flashcard.grid_forget()
            # database function
            self.selected_flashcard_data = get_flashcard_by_id(cursor, selected['id'])
            self.selected_flashcard_cards = get_cards_by_id(cursor, selected['id'])
            self.remaining_time = timeLimitMinusOne(conn, cursor, selected['id']) + 1
            self.timer_running = True
            current_index = self.selected_flashcard_data['completed']


            heartImage = ctk.CTkImage(light_image=Image.open("heart.png"),
                                              dark_image=Image.open("heart.png"),
                                              size=(30, 30))
            def validate_answer(index, answer):
                nonlocal current_index, heart
                user_answer = answer
                correct_answer = self.selected_flashcard_cards[index]['answer']
                if user_answer != correct_answer:
                    remainingHeart = heartMinusOne(conn, cursor, selected['id'])
                    heart.configure(text=f"{remainingHeart}")
                    if remainingHeart == 0:
                        self.selected_flashcard.grid_forget()
                        messagebox.showinfo("Error", f"No heart remaining !!!")
                        show_main_component()
                    else:
                        messagebox.showerror("Wrong !!!", "Wrong answer !!!\n One heart deducted")
                else:
                    messagebox.showinfo("Success", "Correct !!!")
                    completedDeckPlusOne(conn, cursor, selected['id'])
                    if current_index < len(self.selected_flashcard_cards)-1:
                        self.card.grid_forget()
                        current_index += 1
                        show_question()
                    else:
                        self.selected_flashcard.grid_forget()
                        messagebox.showinfo("Success", f"Successfully completed {selected['name']} !!!")
                        show_main_component()

            def show_question():
                self.card = ctk.CTkFrame(self.selected_flashcard, fg_color="#CCCCE1")
                self.card.grid(row=1, column=0, sticky="nsew", pady=20,
                               padx=(0, 20))
                id = tk.Label(self.card,
                              text=f"{current_index + 1}",
                              font=("Arial", 20, "bold"),
                              bg="#CCCCE1",
                              fg="#CCCCE1",
                              justify="left")
                id.grid(row=0, column=0, sticky="nsw", pady=(20, 0), padx=20)
                bg_label = tk.Label(self.card,
                                    text=f"CARD {current_index + 1}:",
                                    font=("Arial", 20, "bold"),
                                    bg="#CCCCE1",
                                    fg="black",
                                    wraplength=1000,
                                    justify="left")
                bg_label.grid(row=0, column=0, sticky="nsw", pady=(20, 0), padx=20)

                description = tk.Label(self.card,
                                       text="Description/Definition:",
                                       font=("Arial", 14),
                                       bg="#CCCCE1",
                                       fg="black",
                                       justify="left")
                description.grid(row=1, column=0, sticky="nsw", pady=(20, 0), padx=20)
                description_entry = ctk.CTkLabel(master=self.card,
                                                 width=1000,
                                                 height=50,
                                                 corner_radius=6,
                                                 bg_color='transparent',
                                                 fg_color='white',
                                                 text_color='black',
                                                 font=("Arial", 16),
                                                 text=f"{self.selected_flashcard_cards[current_index]['description']}",
                                                 anchor="w"
                                                 )
                description_entry.grid(row=2, column=0, sticky="nsw", pady=(0, 20), padx=20, ipady=20)
                answer = tk.Label(self.card,
                                  text="Answer:",
                                  font=("Arial", 14),
                                  bg="#CCCCE1",
                                  fg="black",
                                  wraplength=1000,
                                  justify="left")
                answer.grid(row=3, column=0, sticky="nsw", padx=20)
                answer_entry = ctk.CTkEntry(master=self.card,
                                            width=600,
                                            height=50,
                                            corner_radius=6,
                                            placeholder_text='Enter correct answer here',
                                            bg_color='transparent',
                                            fg_color='white',
                                            text_color='black',
                                            border_color='gray70',
                                            border_width=1,
                                            font=("Arial", 16)

                                            )
                answer_entry.grid(row=4, column=0, sticky="nsw", pady=(0, 20), padx=20)

                SubmitButton = ctk.CTkButton(
                    master=self.card,
                    text='Submit',
                    font=('Open Sans', 14, "bold"),
                    text_color="white",
                    fg_color="#D66ACE",
                    hover_color='#D66ACE',
                    width=60,
                    height=40,
                    corner_radius=10,
                    command=lambda: validate_answer(current_index, answer_entry.get())
                )
                SubmitButton.place(relx=0.5, rely=0.95, anchor="center")
            def update_timer():
                if self.timer_running and self.remaining_time > 0:
                    self.remaining_time = timeLimitMinusOne(conn, cursor, selected['id'])
                    self.timer_label.configure(text=f"{str(datetime.timedelta(seconds=self.remaining_time))}")
                    self.selected_flashcard.after(1000, update_timer)
                elif self.timer_running and self.remaining_time <= 0:
                    self.selected_flashcard.grid_forget()
                    messagebox.showinfo("Error", f"No time remaining !!!")
                    show_main_component()

            self.selected_flashcard = tk.Frame(self.main_frame, bg="white")
            self.selected_flashcard.columnconfigure(0, weight=1)
            self.selected_flashcard.rowconfigure(1, weight=1)
            self.selected_flashcard.grid(row=0, column=1, sticky="nsew")

            header = ctk.CTkFrame(self.selected_flashcard, fg_color="white")
            header.grid(row=0, column=0, sticky="nsew", pady=20, padx=(0, 20))

            bg_label = ctk.CTkLabel(header,
                                    text=f"{selected['name']}",
                                    font=("Arial", 40, "bold"),
                                    fg_color="#5168FF",
                                    text_color="white",
                                    corner_radius=8)
            bg_label.place(relx=0.5, rely=0.1, anchor="center")
            self.timer_label = ctk.CTkLabel(header,
                                 text=f"{self.remaining_time}",
                                 font=("Arial", 30),
                                 text_color="black",
                                 corner_radius=8)
            self.timer_label.place(relx=0.05, rely=0.85, anchor="center")
            heart = ctk.CTkLabel(header,
                                 text=f"{self.selected_flashcard_data['hearts']}",
                                 font=("Arial", 30),
                                 text_color="red",
                                 corner_radius=8,
                                 image=heartImage,
                                 compound="right"
                                 )
            heart.place(relx=0.95, rely=0.85, anchor="center")

            # progress_bar = ctk.CTkProgressBar(header,
            #                                   fg_color="gray",
            #                                   progress_color="pink",
            #                                   width=900,
            #                                   height=20,
            #                                   )
            # progress_bar.place(relx=0.5, rely=0.95, anchor="center")
            # progress_bar.set(0.70)

            update_timer()
            show_question()

        def show_main_component():
            if hasattr(self, 'history'):
                self.history.grid_forget()
            if hasattr(self, 'progress'):
                self.progress.grid_forget()
            if hasattr(self, 'selected_flashcard'):
                self.selected_flashcard.grid_forget()
            if hasattr(self, 'timer_running'):
                self.timer_running = False
            self.main_component = tk.Frame(self.main_frame, bg="white")
            self.main_component.columnconfigure(0, weight=1)
            self.main_component.grid(row=0, column=1, sticky="nsew")

            header = ctk.CTkFrame(self.main_component, fg_color="#6A4DA3")
            header.grid(row=0, column=0, sticky="nsew", pady=20, padx=(0, 20))

            bg_label = tk.Label(header,
                                text=f"Welcome back, {userInfo['username']} Let's continue where we left off. \nWhat would you like to dive into next?",
                                font=("Arial", 26, "bold"),
                                bg="#6A4DA3",
                                fg="white",
                                wraplength=1000,
                                justify="left")
            bg_label.grid(row=0, column=0, sticky="nsw", pady=20, padx=20)

            self.main_component.rowconfigure(1, weight=1)
            card_container = ctk.CTkScrollableFrame(self.main_component, fg_color="white")
            card_container.grid(row=1, column=0, sticky="nsew")


            screen_limit=3
            flashcards = get_flashcards(cursor, userInfo["id"])
            print("len", len(flashcards), len(flashcards)//screen_limit, len(flashcards)%screen_limit, len(flashcards)/screen_limit)
            if len(flashcards) != 0:
                limit = len(flashcards)/screen_limit if len(flashcards) % screen_limit == 0 else (len(flashcards) // screen_limit) + 1
                print("limit", limit)
                for i in range(int(limit)):
                    column = 0
                    range_limit = (i+1)*screen_limit if (i+1)*screen_limit < len(flashcards) else len(flashcards)
                    for j in range(i*screen_limit, range_limit):
                        column += 1
                        print("j", j)
                        color = "pink" if flashcards[j]['total'] == flashcards[j]['completed'] else "gray"
                        cardbutton = ctk.CTkButton(
                            master=card_container,
                            font=('Open Sans', 80, 'bold'),
                            text=f"{flashcards[j]['completed']}/{flashcards[j]['total']}",
                            text_color="black",
                            fg_color=color,
                            hover_color=color,
                            width=300,
                            height=200,
                            corner_radius=6,
                            anchor="center",
                            command=lambda j=j : show_flashcard(flashcards[j])
                        )
                        cardbutton.grid(row=i+1, column=column, sticky="new", padx=(0, 30), pady=(20, 0))
                        button_label = ctk.CTkLabel(cardbutton,
                                                    text=f"{flashcards[j]['name']}",
                                                    font=('Open Sans', 20, 'bold'),
                                                    text_color="black",
                                                    fg_color="white",
                                                    corner_radius=6,
                                                    width=290,
                                                    height=50
                                                    )
                        button_label.place(relx=0.5, rely=0.85, anchor="center")
            AddButton = ctk.CTkButton(
                master=card_container,
                font=('Open Sans', 80, 'bold'),
                text="+",
                text_color="black",
                fg_color="#804BDB",
                hover_color='#804BDB',
                width=300,
                height=200,
                corner_radius=6,
                anchor="center",
                command=new_flashcard
            )
            AddButton.grid(row=(len(flashcards)//screen_limit) + 1, column=(len(flashcards) % screen_limit) + 1, sticky="new", padx=(0, 30), pady=(20, 0))
            button_label = ctk.CTkLabel(AddButton,
                                        text="Create New",
                                        font=('Open Sans', 20, 'bold'),
                                        text_color="black",
                                        fg_color="white",
                                        corner_radius=6,
                                        width=290,
                                        height=50
                                        )
            button_label.place(relx=0.5, rely=0.85, anchor="center")

        def new_flashcard():
            card_count = 0
            card_list = {}
            last_index = 0;
            def add_card():
                nonlocal card_count, card_list, new_card_container, last_index
                key = f"{last_index}"
                card_count += 1
                card_list[key] = ctk.CTkFrame(new_card_container, fg_color="#CCCCE1")
                # id = tk.Label(card_list[len(card_list) - 1],
                #                     text=f"{card_count}",
                #                     font=("Arial", 20, "bold"),
                #                     bg="#CCCCE1",
                #                     fg="#CCCCE1",
                #                     justify="left")
                # id.grid(row=0, column=0, sticky="nsw", pady=(20, 0), padx=20)
                bg_label = tk.Label(card_list[key],
                                    text=f"CARD {last_index+1}:",
                                    font=("Arial", 20, "bold"),
                                    bg="#CCCCE1",
                                    fg="black",
                                    wraplength=1000,
                                    justify="left")
                bg_label.grid(row=0, column=0, sticky="nsw", pady=(20, 0), padx=20)
                CloseButton = ctk.CTkButton(
                    master=card_list[key],
                    text='X',
                    font=('Open Sans', 24),
                    text_color="black",
                    fg_color="#CCCCE1",
                    hover_color='#CCCCE1',
                    width=40,
                    height=40,
                    corner_radius=10,
                    command=lambda key = key : remove_card(key)
                )
                CloseButton.place(relx=0.98, rely=0.1, anchor="center")

                description = tk.Label(card_list[key],
                                       text="Description/Definition:",
                                       font=("Arial", 14),
                                       bg="#CCCCE1",
                                       fg="black",
                                       justify="left")
                description.grid(row=1, column=0, sticky="nsw", pady=(20, 0), padx=20)
                description_entry = ctk.CTkEntry(master=card_list[key],
                                                 width=500,
                                                 height=50,
                                                 corner_radius=6,
                                                 placeholder_text='Enter description',
                                                 bg_color='transparent',
                                                 fg_color='white',
                                                 text_color='black',
                                                 border_color='gray70',
                                                 border_width=1,
                                                 font=("Arial", 16)
                                                 )
                description_entry.grid(row=2, column=0, sticky="nsw", pady=(0, 20), padx=20)
                answer = tk.Label(card_list[key],
                                  text="Answer:",
                                  font=("Arial", 14),
                                  bg="#CCCCE1",
                                  fg="black",
                                  wraplength=1000,
                                  justify="left")
                answer.grid(row=3, column=0, sticky="nsw", padx=20)
                answer_entry = ctk.CTkEntry(master=card_list[key],
                                            width=600,
                                            height=50,
                                            corner_radius=6,
                                            placeholder_text='Enter correct answer here',
                                            bg_color='transparent',
                                            fg_color='white',
                                            text_color='black',
                                            border_color='gray70',
                                            border_width=1,
                                            font=("Arial", 16)

                                            )
                answer_entry.grid(row=4, column=0, sticky="nsw", pady=(0, 20), padx=20)
                last_index += 1

                # for i in range(len(card_list)):
                row=0
                for key, value in card_list.items():
                    value.grid(row=row, column=0, sticky="nsew", pady=20, padx=(0, 20))
                    row+=1
            def remove_card(key):
                nonlocal card_count, card_list, new_card_container
                if len(card_list) <= 1:
                    return
                card_count -= 1
                index = list(card_list.keys()).index(key)
                card_list.pop(key)
                new_card_container.winfo_children()[index].destroy()
                new_card_container.update()
            def save():
                nonlocal hour_entry, minute_entry, sec_entry
                name = name_entry.get()
                if(name == ''):
                    messagebox.showerror("Error", "Please enter flashcard title")
                    return
                hour = hour_entry.get() if hour_entry.get() != '' else 0
                min = minute_entry.get() if minute_entry.get() != '' else 0
                sec = sec_entry.get() if sec_entry.get() != '' else 0

                if hour == 0 and min == 0 and sec == 0:
                    messagebox.showerror("Error", "Please enter time limit")
                    return
                timeLimit = int(hour)*3600 + int(min)*60 + int(sec)
                cards = {}
                i = 0
                for key, value in card_list.items():
                    temp = {}
                    temp["desc"] = value.winfo_children()[3].get()
                    temp["ans"] = value.winfo_children()[5].get()
                    if temp["desc"] == '' or temp["ans"] == '':
                        messagebox.showerror("Error", "Please fill-up empty card")
                        return
                    cards[i] = temp
                    i+=1

                #database function
                create_flashcard(conn, cursor, userInfo["id"], name, cards, timeLimit)
                self.new_flashcard.grid_forget()
                show_main_component()

            ### TITLE

            self.new_flashcard = tk.Frame(self.main_frame, bg="white")
            self.new_flashcard.columnconfigure(0, weight=1)
            self.new_flashcard.grid(row=0, column=1, sticky="nsew")

            header = ctk.CTkFrame(self.new_flashcard, fg_color="#3026C5")
            header.grid(row=0, column=0, sticky="nsew", pady=20, padx=(0, 20))

            bg_label = tk.Label(header,
                                text="Flashcard Name:",
                                font=("Arial", 14),
                                bg="#3026C5",
                                fg="white",
                                wraplength=1000,
                                justify="left")
            bg_label.grid(row=0, column=0, sticky="nsw", pady=(50, 0), padx=20)

            SaveButton = ctk.CTkButton(
                master=header,
                text='Save',
                font=('Open Sans', 14, "bold"),
                text_color="white",
                fg_color="#D66ACE",
                hover_color='#D66ACE',
                width=60,
                height=40,
                corner_radius=10,
                command=save
            )
            SaveButton.place(relx=0.96, rely=0.3, anchor="center")
            name_entry = ctk.CTkEntry(master=header,
                                      width=800,
                                      height=50,
                                      corner_radius=6,
                                      placeholder_text='Enter flashcard name',
                                      bg_color='transparent',
                                      fg_color='white',
                                      text_color='black',
                                      border_color='gray70',
                                      border_width=1,
                                      font=("Arial", 16)

                                      )
            name_entry.grid(row=1, column=0, sticky="nsw", pady=(0, 20), padx=20)
            timeFrame = ctk.CTkFrame(header, fg_color="#3026C5")
            timeFrame.grid(row=3, column=0, sticky="nsew", pady=20, padx=(0, 20))

            hour_lbl = tk.Label(timeFrame,
                                text="Time Limit",
                                font=("Arial", 14),
                                bg="#3026C5",
                                fg="white",
                                wraplength=1000,
                                justify="left")
            hour_lbl.grid(row=0, column=0, sticky="nsw", pady=20, padx=20)

            hour_entry = ctk.CTkEntry(master=timeFrame,
                                      width=30,
                                      height=20,
                                      corner_radius=6,
                                      placeholder_text='0',
                                      bg_color='transparent',
                                      fg_color='white',
                                      text_color='black',
                                      border_color='gray70',
                                      border_width=1,
                                      font=("Arial", 16)

                                      )
            hour_entry.grid(row=0, column=1, sticky="nsw", pady=20, padx=4)
            minute_lbl = tk.Label(timeFrame,
                                text=":",
                                font=("Arial", 14),
                                bg="#3026C5",
                                fg="white",
                                wraplength=1000,
                                justify="left")
            minute_lbl.grid(row=0, column=2, sticky="nsw", pady=20, padx=4)

            minute_entry = ctk.CTkEntry(master=timeFrame,
                                      width=30,
                                      height=20,
                                      corner_radius=6,
                                      placeholder_text='0',
                                      bg_color='transparent',
                                      fg_color='white',
                                      text_color='black',
                                      border_color='gray70',
                                      border_width=1,
                                      font=("Arial", 16)

                                      )
            minute_entry.grid(row=0, column=3, sticky="nsw", pady=20, padx=4)
            sec_lbl = tk.Label(timeFrame,
                                  text=":",
                                  font=("Arial", 14),
                                  bg="#3026C5",
                                  fg="white",
                                  wraplength=1000,
                                  justify="left")
            sec_lbl.grid(row=0, column=4, sticky="nsw", pady=20, padx=4)

            sec_entry = ctk.CTkEntry(master=timeFrame,
                                        width=30,
                                        height=20,
                                        corner_radius=6,
                                        placeholder_text='0',
                                        bg_color='transparent',
                                        fg_color='white',
                                        text_color='black',
                                        border_color='gray70',
                                        border_width=1,
                                        font=("Arial", 16)

                                        )
            sec_entry.grid(row=0, column=5, sticky="nsw", pady=20, padx=4)
            #### CARDS

            self.new_flashcard.rowconfigure(1, weight=1)
            new_card_container = ctk.CTkScrollableFrame(self.new_flashcard,
                                                        fg_color="white",
                                                        scrollbar_fg_color="white",
                                                        scrollbar_button_color="#D66ACE",
                                                        scrollbar_button_hover_color="#D66ACE")
            new_card_container.columnconfigure(0, weight=1)
            new_card_container.grid(row=1, column=0, sticky="nsew", pady=(0, 50))

            add_card()

            AddCardButton = ctk.CTkButton(
                master=self.new_flashcard,
                text='Add more card',
                font=('Open Sans', 14, "bold"),
                text_color="white",
                fg_color="#D66ACE",
                hover_color='#D66ACE',
                width=60,
                height=40,
                corner_radius=10,
                command=add_card
            )
            AddCardButton.grid(row=2, column=0, sticky="nsew", padx=(0, 20), pady=20)

        def logout():
            # # nonlocal left_panel, right_panel
            # if hasattr(self, 'history'):
            #     self.history.grid_forget()
            # if hasattr(self, 'progress'):
            #     self.progress.grid_forget()
            # if hasattr(self, 'selected_flashcard'):
            #     self.selected_flashcard.grid_forget()
            # if hasattr(self, 'side_menu'):
            #     self.side_menu.grid_forget()
            # if hasattr(self, 'main_component'):
            #     self.main_component.grid_forget()
            if hasattr(self, 'timer_running'):
                self.timer_running = False
            self.main_frame.columnconfigure(0, weight=1)
            self.login()
        def show_side_menu():
            ##### LEFT PANEL
            self.main_frame.columnconfigure(0, weight=0)
            self.side_menu = tk.Frame(self.main_frame, bg="white", pady=20, padx=20)
            self.side_menu.rowconfigure(0, weight=1)
            self.side_menu.grid(row=0, column=0, rowspan=3, sticky="nsew")
            # Load and display the background image
            left_panel_frame = ctk.CTkFrame(self.side_menu, fg_color="#D4C3E1", width=self.side_panel_width)
            left_panel_frame.grid(row=0, column=0, sticky="nsew")

            bg_label = tk.Label(left_panel_frame,
                                text="PyCards",
                                font=("Arial", 26, "bold"),
                                bg="#D4C3E1",
                                fg="black")
            bg_label.grid(row=0, column=0, sticky="new", pady=20)
            MainScreenButton = ctk.CTkButton(
                master=left_panel_frame,
                text='Main Screen',
                font=('Open Sans', 18, 'bold'),
                text_color="black",
                fg_color="#D4C3E1",
                hover_color='#D66ACE',
                width=350,
                height=30,
                corner_radius=10,
                command=show_main_component
            )
            MainScreenButton.grid(row=1, column=0, sticky="new", padx=30)
            ProgressButton = ctk.CTkButton(
                master=left_panel_frame,
                text='Progress',
                font=('Open Sans', 18, 'bold'),
                text_color="black",
                fg_color="#D4C3E1",
                hover_color='#D66ACE',
                width=350,
                height=30,
                corner_radius=10,
                command=show_progress
            )
            ProgressButton.grid(row=2, column=0, sticky="new", padx=30)
            HistoryButton = ctk.CTkButton(
                master=left_panel_frame,
                text='History',
                font=('Open Sans', 18, 'bold'),
                text_color="black",
                fg_color="#D4C3E1",
                hover_color='#D66ACE',
                width=350,
                height=30,
                corner_radius=10,
                command=show_history
            )
            HistoryButton.grid(row=3, column=0, sticky="new", padx=30)

            LogoutButton = ctk.CTkButton(
                master=left_panel_frame,
                text='Logout',
                font=('Open Sans', 18, 'bold'),
                text_color="black",
                fg_color="#D4C3E1",
                hover_color='#D66ACE',
                width=350,
                height=30,
                corner_radius=10,
                command=logout
            )
            LogoutButton.place(relx=0.5, rely=0.95, anchor="center")

        show_side_menu()
        show_main_component()


if __name__ == "__main__":
    root = tk.Tk()
    # root.attributes('-fullscreen', True)
    # Adjust window size and center it
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1000
    window_height = 600
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    PyCards(root)

    root.mainloop()
