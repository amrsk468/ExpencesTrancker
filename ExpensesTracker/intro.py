from tkinter import *


def to_main(win: Tk):
    loading_lbl = Label(win, text="Loading...", font=("Arial", 20))
    loading_lbl.pack()
    win.update()
    items = [intro_label, intro_label2, to_main_btn, loading_lbl, intro_label3]
    from ExpensesTracker import start
    win.after(100, lambda: start(win, items))


intro_win = Tk()
intro_win.title("Expenses Tracker")
intro_win.geometry("800x600+100+100")
intro_win.iconbitmap("ExpensesTracker/assets/images/logo.ico")
intro_win.resizable(False, False)

intro_label = Label(intro_win, text="Expenses Tracker", font=("Arial Bold", 40))
intro_label.pack(pady=40)
intro_label2 = Label(intro_win, text="Amit Zakar", font=("Arial", 15))
intro_label2.pack(pady=10)
intro_label3 = Label(intro_win, text="2025", font=("Arial", 15))
intro_label3.pack(pady=10)

to_main_btn = Button(intro_win, text="Continue", command=lambda: to_main(intro_win), font=("Arial Bold", 20))
to_main_btn.pack(pady=40, anchor="center")

intro_win.mainloop()