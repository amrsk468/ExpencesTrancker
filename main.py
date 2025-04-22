from tkinter import *
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as tkAgg
import datetime as dt

transactions = pd.read_csv("transactions.csv")

root = Tk()
root.title("Expenses Tracker")
root.geometry("800x600+300+100")
root.iconbitmap("images/logo.ico")

tab_manager = ttk.Notebook(root)
tab_manager.pack(expand=True, fill="both")
style = ttk.Style()
style.configure("TNotebook", background="gray")
style.configure("TNotebook.Tab", font=("Arial", 12, "bold"), padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "blue")], foreground=[("selected", "black")])

accounts_tab = ttk.Frame(tab_manager)
categories_tab = ttk.Frame(tab_manager)
transactions_tab = ttk.Frame(tab_manager)
statistics_tab = ttk.Frame(tab_manager)

tab_manager.add(accounts_tab, text="Accounts")
tab_manager.add(categories_tab, text="Categories")
tab_manager.add(transactions_tab, text="Transactions")
tab_manager.add(statistics_tab, text="statistics")
tab_manager.select(categories_tab)

accounts_tab_add_account_btn = ttk.Button(accounts_tab, text="Add Account")
accounts_tab_add_account_btn.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()
