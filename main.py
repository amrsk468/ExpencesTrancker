from tkinter import *
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as tkAgg
import datetime as dt
import json

from typing_extensions import ReadOnly


def save_data():
    keys = {'account': [], 'category': [], 'amount': [], 'date': []}
    for i in transactions_list:
        keys['account'].append(i[0])
        keys['category'].append(i[1])
        keys['amount'].append(i[2])
        keys['date'].append(i[3])
    data = pd.DataFrame(keys)
    data.to_csv("transactions.csv", index=False)


def save_accounts():
    with open("accounts.json", "w") as file:
        json.dump(accounts, file)


def delete_transaction(transaction: str, listbox: Listbox, account = None):
    split_transaction = transaction.split(" ")
    split_transaction.remove("account:")
    split_transaction.remove("category:")
    split_transaction.remove("amount:")
    split_transaction.remove("date:")
    if type(accounts) is str:
        split_transaction = [account] + split_transaction
    split_transaction[2] = int(split_transaction[2][1:])
    for transaction in transactions_list:
        if split_transaction == transaction:
            listbox.delete(ACTIVE)
            transactions_list.remove(transaction)
            break


def account_view_transactions(account: tuple, win: Toplevel):
    win.title(f"{account[0]} transactions")
    win.geometry("500x600+910+100")
    listbox = Listbox(win, width=82, height=35)
    listbox.grid(row=0, column=0)
    for transaction in transactions_list:
        if transaction[0] == account[0]:
            listbox.insert(END, f"category: {transaction[1]} amount: ${transaction[2]} date: {transaction[3]}")
    delete_button = Button(win, text="Delete", command=lambda: delete_transaction(listbox.get(ACTIVE), listbox, account[0]))
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


def add_transaction_win(win: Toplevel, category: str):
    pass


# load data:

with open("categories.txt", "r") as file:
    global categories
    categories = file.readlines()
    for i in range(len(categories)):
        categories[i] = categories[i].replace("\n", "")

with open("accounts.json", "r") as f:
    global accounts
    accounts = json.load(f)

global transactions, transactions_list
transactions = pd.read_csv("transactions.csv")
transactions = transactions[["account","category","amount","date"]]
transactions_list = transactions[["account","category","amount","date"]].values.tolist()

# main win & tab manger:

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
add_transaction_tab = ttk.Frame(tab_manager)
transactions_tab = ttk.Frame(tab_manager)
statistics_tab = ttk.Frame(tab_manager)

tab_manager.add(accounts_tab, text="Accounts")
tab_manager.add(add_transaction_tab, text="Add Transaction")
tab_manager.add(transactions_tab, text="Transactions")
tab_manager.add(statistics_tab, text="statistics")
tab_manager.select(add_transaction_tab)

# account tab:

accounts_tab_add_account_btn = ttk.Button(accounts_tab, text="Add Account")
accounts_tab_add_account_btn.grid(row=0, column=0, padx=10, pady=10)

print_account_data(accounts_tab)

# add transactions tab:
categories_tab_account_lbl = Label(add_transaction_tab, text="Account:")
categories_tab_account_lbl.grid(row=0, column=0, padx=10, pady=10)
chosen_account = StringVar()
categories_tab_account = ttk.Combobox(add_transaction_tab, values=list(accounts.keys()), textvariable=chosen_account, state="readonly")
categories_tab_account.grid(row=0, column=1, padx=10, pady=10)
categories_tab_category_lbl = Label(add_transaction_tab, text="Category:")
categories_tab_category_lbl.grid(row=1, column=0, padx=10, pady=10)
chosen_category = StringVar()
categories_tab_category = ttk.Combobox(add_transaction_tab, textvariable=chosen_category, values=categories, state="readonly")
categories_tab_category.grid(row=1, column=1, padx=10, pady=10)
categories_tab_amount_lbl = Label(add_transaction_tab, text="Amount:")
categories_tab_amount_lbl.grid(row=2, column=0, padx=10, pady=10)
chosen_amount = StringVar()
categories_tab_amount = Entry(add_transaction_tab, textvariable=chosen_amount, width=23)
categories_tab_amount.grid(row=2, column=1, padx=10, pady=10)
categories_tab_date_lbl = Label(add_transaction_tab, text="Date:")
categories_tab_date_lbl.grid(row=3, column=0, padx=10, pady=10)
chosen_date = StringVar()
chosen_date.set(dt.datetime.now().strftime("%d/%m/%Y"))
categories_tab_date = Entry(add_transaction_tab, textvariable=chosen_date, width=23)
categories_tab_date.grid(row=3, column=1, padx=10, pady=10)
Label(add_transaction_tab, text="enter date at format: dd/mm/yyyy").grid(row=3, column=2, padx=10, pady=10)
categories_tab_add_transaction_btn = Button(add_transaction_tab, text="Add Transaction")
categories_tab_add_transaction_btn.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

# transactions tab:
listbox = Listbox(transactions_tab, width=120, height=35)
listbox.grid(row=0, column=0)
for transaction in transactions_list:
    listbox.insert(END, f"account: {transaction[0]} category: {transaction[1]} amount: ${transaction[2]} date: {transaction[3]}")
delete_button = Button(transactions_tab, text="Delete", command=lambda: delete_transaction(listbox.get(ACTIVE), listbox))
delete_button.grid(row=0, column=1, padx=10)

# statistics tab:


root.mainloop()

save_data()
