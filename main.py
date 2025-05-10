from tkinter import *
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as tkAgg
import datetime as dt
import json

def save_accounts():
    with open("accounts.json", "w") as file:
        json.dump(accounts, file)

def delete_transaction(transaction: str):
    split_transaction = transaction.split(" ")
    split_transaction.remove("category:")
    split_transaction.remove("amount:")
    split_transaction.remove("date:")
    split_transaction[1] = int(split_transaction[1][1:])
    print(split_transaction)

def account_view_transactions(account: tuple, win: Toplevel, items: list = []):
    win.title(f"{account[0]} transactions")
    win.geometry("500x600+910+100")
    listbox = Listbox(win, width=82, height=35)
    listbox.grid(row=0, column=0)
    for transaction in transactions_list:
        listbox.insert(END, f"category: {transaction[1]} amount: ${transaction[2]} date: {transaction[3]}")
    delete_button = Button(win, text="Delete", command=lambda: delete_transaction(listbox.get(ACTIVE)))
    delete_button.grid(row=1, column=0)

def account_modify(account: tuple, win: Frame, items: list):
    pass

def account_delete(account: tuple, win: Frame, items: list):
    accounts_keys = tuple(accounts.keys())
    for i in range(len(accounts)):
        if accounts_keys[i] == account[0]:
            accounts.pop(account[0])
            save_accounts()
            print_account_data(win, items)
            break

def add_account(win: Frame):
    pass

def print_account_data(win: Frame, items: list = []):
    if items is None:
        items = []
    for i in items:
        i.destroy()
    account_labels = []
    account_detail_btn = []
    account_transaction_btn = []
    account_del_btn = []
    i = 0
    for account in accounts.items():
        account_labels.append(ttk.Label(win, text=f"{account[0]}: ${account[1]}"))
        account_labels[i].grid(row=i + 1, column=0, padx=10, pady=10, sticky="w")
        account_detail_btn.append(ttk.Button(win, text="Transactions", command= lambda x=account: account_view_transactions(x, Toplevel(accounts_tab))))
        account_detail_btn[i].grid(row=i + 1, column=1, padx=10, pady=10, sticky="w")
        account_transaction_btn.append(ttk.Button(win, text="Modify"))
        account_transaction_btn[i].grid(row=i + 1, column=2, padx=10, pady=10, sticky="w")
        account_del_btn.append(
            ttk.Button(win, text="Delete",command=lambda x=account:
            account_delete(x, accounts_tab,account_labels + account_detail_btn + account_transaction_btn + account_del_btn)))
        account_del_btn[i].grid(row=i + 1, column=3, padx=10, pady=10, sticky="w")
        i += 1

with open("accounts.json", "r") as f:
    global accounts
    accounts = json.load(f)

global transactions, transactions_list
transactions = pd.read_csv("transactions.csv")
transactions = transactions[["id","account","category","amount","date"]]
transactions_list = transactions[["account","category","amount","date"]].values.tolist()

root = Tk()
root.title("Expenses Tracker")
root.geometry("800x600+100+100")
root.iconbitmap("assets/logo.ico")

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

print_account_data(accounts_tab)


root.mainloop()
