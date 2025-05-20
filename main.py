from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as tkAgg
from datetime import datetime
import json


def save_data():
    keys = {'account': [], 'category': [], 'amount': [], 'date': []}
    for i in transactions_list:
        keys['account'].append(i[0])
        keys['category'].append(i[1])
        keys['amount'].append(i[2])
        keys['date'].append(i[3])
    data = pd.DataFrame(keys)
    data.to_csv("assets/data/transactions.csv", index=False)


def save_accounts():
    with open("assets/data/accounts.json", "w") as file:
        json.dump(accounts, file)


def delete_transaction(transaction: str, listbox: Listbox, account = None):
    print(transaction)
    split_transaction = transaction.split(" ")
    print(split_transaction)
    split_transaction.remove("category:")
    split_transaction.remove("amount:")
    split_transaction.remove("date:")
    if type(account) is str:
        split_transaction = [account] + split_transaction
    else:
        split_transaction.remove("account:")
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
        account_detail_btn.append(ttk.Button(win, text="Transactions", command= lambda x=account: account_view_transactions(x, Toplevel(win))))
        account_detail_btn[i].grid(row=i + 1, column=1, padx=10, pady=10, sticky="w")
        account_transaction_btn.append(ttk.Button(win, text="Modify"))
        account_transaction_btn[i].grid(row=i + 1, column=2, padx=10, pady=10, sticky="w")
        account_del_btn.append(
            ttk.Button(win, text="Delete",command=lambda x=account:
            account_delete(x, win,account_labels + account_detail_btn + account_transaction_btn + account_del_btn)))
        account_del_btn[i].grid(row=i + 1, column=3, padx=10, pady=10, sticky="w")
        i += 1

def add_transaction(win: Frame, account: StringVar, category: StringVar, amount: StringVar, date: StringVar):
    if account.get() == "" or category.get() == "" or amount.get() == "" or date.get() == "":
        messagebox.showerror("Error", "Please fill all fields")
        return
    try:
        amount = int(amount.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return
    try:
        formated_date = datetime.strptime(date.get(), "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Error", "Date must be in format dd/mm/yyyy")
        return
    if formated_date > datetime.now():
        messagebox.showerror("Error", "Date must be in the past or present")
        return
    want_to_add = messagebox.askyesno("Add Transaction", f"Are you sure you want to add this transaction?\nAccount: {account.get()}\nCategory: {category.get()}\nAmount: ${amount}\nDate: {formated_date.strftime('%d/%m/%Y')}")
    if want_to_add:
        transactions_list.append([account.get(), category.get(), amount, formated_date.strftime("%d/%m/%Y")])
        messagebox.showinfo("Add Transaction", "Transaction added successfully")
    else:
        messagebox.showinfo("Add Transaction", "Transaction voided")


def load_data():
    with open("assets/data/categories.txt", "r") as file:
        global categories
        categories = file.readlines()
        for i in range(len(categories)):
            categories[i] = categories[i].replace("\n", "")

    with open("assets/data/accounts.json", "r") as f:
        global accounts
        accounts = json.load(f)

    global transactions, transactions_list
    transactions = pd.read_csv("assets/data/transactions.csv")
    transactions = transactions[["account","category","amount","date"]]
    transactions_list = transactions[["account","category","amount","date"]].values.tolist()



def main(root: Tk):
    # main window & tab manger:

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
    add_transactions_tab_account_lbl = Label(add_transaction_tab, text="Account:")
    add_transactions_tab_account_lbl.grid(row=0, column=0, padx=10, pady=10)
    chosen_account = StringVar()
    add_transactions_tab_account = ttk.Combobox(add_transaction_tab, values=list(accounts.keys()),
                                                textvariable=chosen_account, state="readonly")
    add_transactions_tab_account.grid(row=0, column=1, padx=10, pady=10)
    add_transactions_tab_category_lbl = Label(add_transaction_tab, text="Category:")
    add_transactions_tab_category_lbl.grid(row=1, column=0, padx=10, pady=10)
    chosen_category = StringVar()
    add_transactions_tab_category = ttk.Combobox(add_transaction_tab, textvariable=chosen_category, values=categories,
                                                 state="readonly")
    add_transactions_tab_category.grid(row=1, column=1, padx=10, pady=10)
    add_transactions_tab_amount_lbl = Label(add_transaction_tab, text="Amount:")
    add_transactions_tab_amount_lbl.grid(row=2, column=0, padx=10, pady=10)
    chosen_amount = StringVar()
    add_transactions_tab_amount = Entry(add_transaction_tab, textvariable=chosen_amount, width=23)
    add_transactions_tab_amount.grid(row=2, column=1, padx=10, pady=10)
    add_transactions_tab_date_lbl = Label(add_transaction_tab, text="Date:")
    add_transactions_tab_date_lbl.grid(row=3, column=0, padx=10, pady=10)
    chosen_date = StringVar()
    chosen_date.set(datetime.now().strftime("%d/%m/%Y"))
    add_transactions_tab_date = Entry(add_transaction_tab, textvariable=chosen_date, width=23)
    add_transactions_tab_date.grid(row=3, column=1, padx=10, pady=10)
    Label(add_transaction_tab, text="enter date at format: dd/mm/yyyy").grid(row=3, column=2, padx=10, pady=10)
    add_transactions_tab_add_transaction_btn = Button(add_transaction_tab, text="Add Transaction",
                                                      command=lambda: add_transaction(add_transaction_tab,
                                                                                      chosen_account, chosen_category,
                                                                                      chosen_amount, chosen_date))
    add_transactions_tab_add_transaction_btn.grid(row=4, column=0, padx=10, pady=10, columnspan=2)
    output_var = StringVar()
    add_transactions_tab_output = Label(add_transaction_tab, textvariable=output_var)
    add_transactions_tab_output.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

    # transactions tab:
    listbox = Listbox(transactions_tab, width=120, height=35)
    listbox.grid(row=0, column=0)
    for transaction in transactions_list:
        listbox.insert(END,
                       f"account: {transaction[0]} category: {transaction[1]} amount: ${transaction[2]} date: {transaction[3]}")
    delete_button = Button(transactions_tab, text="Delete",
                           command=lambda: delete_transaction(listbox.get(ACTIVE), listbox))
    delete_button.grid(row=0, column=1, padx=10)

    # statistics tab:

    root.mainloop()

    save_data()
    save_accounts()

def start(win: Tk, items: list):
    load_data()
    for i in items:
        i.destroy()
    main(win)