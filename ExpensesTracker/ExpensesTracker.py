from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as tkAgg
from datetime import datetime
import json

global categories, accounts, transactions, transactions_list


def start(win: Tk, items: list):
    load_data()
    for i in items:
        i.destroy()
    main(win)


def on_closing(win: Tk):
    save_data()
    plt.close('all')
    win.destroy()


def save_data():
    global transactions_list
    transactions_list = sorted(transactions_list, key=lambda x: datetime.strptime(x[3], "%d/%m/%Y"), reverse=True)
    keys = {'account': [], 'category': [], 'amount': [], 'date': []}
    for i in transactions_list:
        keys['account'].append(i[0])
        keys['category'].append(i[1])
        keys['amount'].append(i[2])
        keys['date'].append(i[3])
    data = pd.DataFrame(keys)
    data.to_csv("ExpensesTracker/assets/data/transactions.csv", index=False)
    with open("ExpensesTracker/assets/data/categories.json", "w") as file:
        json.dump(categories, file)
    with open("ExpensesTracker/assets/data/accounts.json", "w") as file:
        json.dump(accounts, file)


def delete_transaction(transaction: str, listbox: Listbox, account = None):
    split_transaction = transaction.split(" ")
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


def account_delete(account: tuple, win: Frame, items: list):
    accounts_keys = tuple(accounts.keys())
    for i in range(len(accounts)):
        if accounts_keys[i] == account[0]:
            accounts.pop(account[0])
            print_account_data(win, items)
            save_data()
            break


def add_account(win: Frame):
    for widget in win.winfo_children():
        widget.destroy()
    name_lbl = Label(win, text="Account Name:")
    name_lbl.grid(row=0, column=0, padx=10, pady=10)
    name = StringVar()
    name_entry = Entry(win, textvariable=name, width=23)
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    balance_lbl = Label(win, text="Account Balance:")
    balance_lbl.grid(row=1, column=0, padx=10, pady=10)
    balance = StringVar()
    balance_entry = Entry(win, textvariable=balance, width=23)
    balance_entry.grid(row=1, column=1, padx=10, pady=10)
    add_btn = Button(win, text="Add Account", command=lambda: add_account_after(name, balance, win))
    add_btn.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
    cancel_btn = Button(win, text="Cancel", command=lambda: add_account_after(cancel=True, win=win))
    cancel_btn.grid(row=3, column=0, padx=10, pady=10, columnspan=2)


def add_account_after(name: StringVar = None, balance: StringVar = None, win: Frame = None, cancel: bool = False):
    if not cancel:
        if name.get() == "" or balance.get() == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            balance = int(balance.get())
        except ValueError:
            messagebox.showerror("Error", "Balance must be a number")
            return
        if name.get() in accounts:
            override = messagebox.askyesno(title="Error", message="Account already exists\ndo you want to override?")
            if not override:
                return
        add = messagebox.askyesno("Add Account", f"Are you sure you want to add this account?\nName: {name.get()}\nBalance: ${balance}")
        if add:
            accounts[name.get()] = balance
            save_data()
        else:
            messagebox.showinfo("Add Account", "Account voided")
    for widget in win.winfo_children():
        widget.destroy()
    accounts_tab_add_account_btn = ttk.Button(win, text="Add Account",
                                                  command=lambda: add_account(win))
    accounts_tab_add_account_btn.grid(row=0, column=0, padx=10, pady=10)
    print_account_data(win, [])


def print_account_data(win: Frame, items: list = []):
    for i in items:
        i.destroy()
    account_labels = []
    account_detail_btn = []
    account_del_btn = []
    i = 0
    for account in accounts.items():
        account_labels.append(ttk.Label(win, text=f"{account[0]}: ${account[1]}"))
        account_labels[i].grid(row=i + 1, column=0, padx=10, pady=10, sticky="w")
        account_detail_btn.append(ttk.Button(win, text="Transactions", command= lambda x=account: account_view_transactions(x, Toplevel(win))))
        account_detail_btn[i].grid(row=i + 1, column=1, padx=10, pady=10, sticky="w")
        account_del_btn.append(
            ttk.Button(win, text="Delete",command=lambda x=account:
            account_delete(x, win,account_labels + account_detail_btn + account_del_btn)))
        account_del_btn[i].grid(row=i + 1, column=3, padx=10, pady=10, sticky="w")
        i += 1

def add_transaction(account: StringVar, category: StringVar, amount: StringVar, date: StringVar):
    if account.get() == "" or category.get() == "" or amount.get() == "" or date.get() == "":
        messagebox.showerror("Error", "Please fill all fields")
        return
    try:
        amount = int(amount.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return
    else:
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0")
            return
        if amount > accounts[account.get()] and category.get() != "salary":
            messagebox.showerror("Error", "In expense amount must be less than or equal to account balance")
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
        transactions_list.insert(0, [account.get(), category.get(), amount, formated_date.strftime("%d/%m/%Y")])
        messagebox.showinfo("Add Transaction", "Transaction added successfully")
    else:
        messagebox.showinfo("Add Transaction", "Transaction voided")


def add_category(name: StringVar, type: StringVar):
    if name.get() == "" or type.get() == "Select Type" or type.get() == "":
        messagebox.showerror("Error", "Please fill all fields")
        return
    if name.get() in categories:
        override = messagebox.askyesno(title="Error", message="Category already exists\ndo you want to override?")
        if not override:
            return
    add = messagebox.askyesno("Add Category", f"Are you sure you want to add this category?\nName: {name.get()}\nType: {type.get()}")
    if add:
        categories[name.get()] = type.get()
        messagebox.showinfo("Add Category", "Category added successfully")
    else:
        messagebox.showinfo("Add Category", "Category voided")


def load_data():
    global categories, accounts, transactions, transactions_list

    with open("ExpensesTracker/assets/data/categories.json", "r") as file:
        categories = json.load(file)

    with open("ExpensesTracker/assets/data/accounts.json", "r") as file:
        accounts = json.load(file)

    transactions = pd.read_csv("ExpensesTracker/assets/data/transactions.csv")
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

    accounts_tab_add_account_btn = ttk.Button(accounts_tab, text="Add Account", command=lambda: add_account(accounts_tab))
    accounts_tab_add_account_btn.grid(row=0, column=0, padx=10, pady=10)

    print_account_data(accounts_tab)

    # add transactions tab:
    add_transaction_tab_account_lbl = Label(add_transaction_tab, text="Add Transaction", font=("Arial", 16, "bold"))
    add_transaction_tab_account_lbl.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="w")
    add_transactions_tab_account_lbl = Label(add_transaction_tab, text="Account:")
    add_transactions_tab_account_lbl.grid(row=1, column=0, padx=10, pady=10)
    chosen_account = StringVar()
    add_transactions_tab_account = ttk.Combobox(add_transaction_tab, values=list(accounts.keys()),
                                                textvariable=chosen_account, state="readonly")
    add_transactions_tab_account.grid(row=1, column=1, padx=10, pady=10)
    add_transactions_tab_category_lbl = Label(add_transaction_tab, text="Category:")
    add_transactions_tab_category_lbl.grid(row=2, column=0, padx=10, pady=10)
    chosen_category = StringVar()
    add_transactions_tab_category = ttk.Combobox(add_transaction_tab, textvariable=chosen_category, values=list(categories.keys()),
                                                 state="readonly")
    add_transactions_tab_category.grid(row=2, column=1, padx=10, pady=10)
    add_transactions_tab_category.set("Select Category")
    add_transactions_tab_amount_lbl = Label(add_transaction_tab, text="Amount:")
    add_transactions_tab_amount_lbl.grid(row=3, column=0, padx=10, pady=10)
    chosen_amount = StringVar()
    add_transactions_tab_amount = Entry(add_transaction_tab, textvariable=chosen_amount, width=23)
    add_transactions_tab_amount.grid(row=3, column=1, padx=10, pady=10)
    add_transactions_tab_date_lbl = Label(add_transaction_tab, text="Date:")
    add_transactions_tab_date_lbl.grid(row=4, column=0, padx=10, pady=10)
    chosen_date = StringVar()
    chosen_date.set(datetime.now().strftime("%d/%m/%Y"))
    add_transactions_tab_date = Entry(add_transaction_tab, textvariable=chosen_date, width=23)
    add_transactions_tab_date.grid(row=4, column=1, padx=10, pady=10)
    Label(add_transaction_tab, text="enter date at format: dd/mm/yyyy").grid(row=4, column=2, padx=10, pady=10)
    add_transactions_tab_add_transaction_btn = Button(add_transaction_tab, text="Add Transaction",
                                                      command=lambda: add_transaction(
                                                                                      chosen_account, chosen_category,
                                                                                      chosen_amount, chosen_date))
    add_transactions_tab_add_transaction_btn.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
    add_transaction_tab_categories_lbl = Label(add_transaction_tab, text="Add Category", font=("Arial", 16, "bold"))
    add_transaction_tab_categories_lbl.grid(row=6, column=0, padx=10, pady=10, columnspan=2, sticky="w")
    add_transaction_tab_name_lbl = Label(add_transaction_tab, text="Category Name:")
    add_transaction_tab_name_lbl.grid(row=7, column=0, padx=10, pady=10)
    category_name = StringVar()
    add_transaction_tab_name = Entry(add_transaction_tab, width=23, textvariable=category_name)
    add_transaction_tab_name.grid(row=7, column=1, padx=10, pady=10)
    add_transaction_tab_type_lbl = Label(add_transaction_tab, text="Category Type:")
    add_transaction_tab_type_lbl.grid(row=8, column=0, padx=10, pady=10)
    category_type = StringVar()
    add_transaction_tab_type = ttk.Combobox(add_transaction_tab, textvariable=category_type,
                                             values=["Income", "Expense"], state="readonly")
    add_transaction_tab_type.grid(row=8, column=1, padx=10, pady=10)
    add_transaction_tab_type.set("Select Type")
    add_transaction_tab_add_category_btn = Button(add_transaction_tab, text="Add Category",
                                                  command=lambda: add_category(category_name, category_type))
    add_transaction_tab_add_category_btn.grid(row=9, column=0, padx=10, pady=10, columnspan=2)

    # transactions tab:
    def update_transactions_listbox(listbox: Listbox):
        for transaction in transactions_list:
            listbox.insert(END,
                           f"account: {transaction[0]} category: {transaction[1]} amount: ${transaction[2]} date: {transaction[3]}")

    listbox = Listbox(transactions_tab, width=120, height=35)
    listbox.grid(row=0, column=0, rowspan=2)
    update_transactions_listbox(listbox)
    delete_button = Button(transactions_tab, text="Delete", command=lambda: delete_transaction(listbox.get(ACTIVE), listbox))
    delete_button.grid(row=0, column=1, padx=10, sticky="S", pady=10)
    refresh_button = Button(transactions_tab, text="Refresh", command=lambda: update_transactions_listbox(listbox))
    refresh_button.grid(row=1, column=1, padx=10, sticky="N", pady=10)

    # statistics tab:
    canvas = Canvas(statistics_tab)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(statistics_tab, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = ttk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda event: canvas.itemconfig(window_id, width=event.width))

    chose_date_lbl = Label(scrollable_frame, text="Choose Month and Year for Statistics:")
    chose_date_lbl.grid(row=0, column=0, padx=10, pady=10)
    month_var = StringVar()
    months = ["All", "January", "February", "March", "April", "May", "June"," July", "August", "September", "October", "November", "December"]
    month_combobox = ttk.Combobox(scrollable_frame, textvariable=month_var, state="readonly", values=months)
    month_combobox.grid(row=0, column=1, padx=10, pady=10)
    current_month = datetime.now().strftime("%B")
    month_combobox.set(current_month)
    year_var = StringVar()
    current_year = datetime.now().year
    year_combobox = ttk.Combobox(scrollable_frame, textvariable=year_var, state="readonly", values=["All"] + list(range(current_year, current_year - 100, -1)))
    year_combobox.grid(row=0, column=2, padx=10, pady=10)
    year_combobox.set(current_year)
    show_statistics_btn = Button(scrollable_frame, text="Show Statistics", command=lambda: show_statistics(month_var, year_var))
    show_statistics_btn.grid(row=0, column=3, padx=10, pady=10)


    def show_statistics(month: StringVar, year: StringVar):
        if not transactions_list:
            return
        data = pd.DataFrame(transactions_list, columns=["account", "category", "amount", "date"])
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

        if month.get() != "All":
            month_number = months.index(month.get()) + 1
            data = data[data["date"].dt.month == month_number]

        if year.get() != "All":
            selected_year = int(year.get())
            data = data[data["date"].dt.year == selected_year]

        if data.empty:
            messagebox.showinfo("Statistics", "No transactions found for the selected month and year.")
            return

        expense_data = data[data["category"] != "salary"].copy()
        expense_data.loc[:, "amount"] = -expense_data["amount"]

        sns.set_theme(style="whitegrid")

        plt.figure(figsize=(8, 5))
        sns.barplot(x="category", y="amount", data=expense_data, estimator=sum, errorbar=None)
        plt.title("Total Expense by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount (USD)")
        plt.tight_layout()
        expense_by_category_fig = plt.gcf()
        expense_by_category_canvas = tkAgg(expense_by_category_fig, master=scrollable_frame)
        expense_by_category_canvas.get_tk_widget().grid(column=0, row=1, sticky="nsew", columnspan=4)
        expense_by_category_canvas.draw()

        plt.figure(figsize=(8, 5))
        plt.pie(expense_data["category"].value_counts(), labels=expense_data["category"].value_counts().index, autopct='%1.1f%%', startangle=140)
        plt.title("Category Distribution")
        plt.tight_layout()
        category_distribution_fig = plt.gcf()
        category_distribution_canvas = tkAgg(category_distribution_fig, master=scrollable_frame)
        category_distribution_canvas.get_tk_widget().grid(column=0, row=2, sticky="nsew", columnspan=4)
        category_distribution_canvas.draw()

        plt.figure(figsize=(8, 5))
        income = data[data["amount"] > 0]["amount"].sum()
        expense = data[data["amount"] < 0]["amount"].sum()
        if pd.isna(income):
            income = 0
        if pd.isna(expense):
            expense = 0
        plt.pie([income, abs(expense)], labels=["Income", "Expense"], autopct='%1.1f%%', startangle=140)
        plt.title("Income vs Expense")
        plt.tight_layout()
        income_vs_expense_fig = plt.gcf()
        income_vs_expense_canvas = tkAgg(income_vs_expense_fig, master=scrollable_frame)
        income_vs_expense_canvas.get_tk_widget().grid(column=0, row=3, sticky="nsew", columnspan=4)
        income_vs_expense_canvas.draw()


    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

