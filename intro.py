from tkinter import *


def to_main(win: Tk):
    loading_lbl = Label(win, text="Loading...")
    loading_lbl.pack()
    win.update()
    items = [intro_label, intro_label2, to_main_btn, loading_lbl]
    from main import start
    win.after(100, lambda: start(win, items))


intro_win = Tk()
intro_win.title("Expenses Tracker")
intro_win.geometry("800x600+100+100")
intro_win.iconbitmap("assets/images/logo.ico")
intro_win.resizable(False, False)

intro_label = Label(intro_win, text="Expenses Tracker", font=("Arial Bold", 30))
intro_label.pack(pady=40)
intro_label2 = Label(intro_win, text="by: Amit Zakar", font=("Arial", 12))
intro_label2.pack(anchor="w")

to_main_btn = Button(intro_win, text="Continue", command=lambda: to_main(intro_win))
to_main_btn.pack(pady=20)

intro_win.mainloop()