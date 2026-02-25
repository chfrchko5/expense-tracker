import csv
from csv import reader
import typer
from typing import Annotated
import datetime
import os
from tabulate import tabulate
import pandas

expenses_app = typer.Typer(help='Application to track your expenses')

csv_file = 'expenses.csv'
csv_headers = ['ID', 'Date', 'Description', 'Amount']

class Expense:
    def add_expense(self, desc:str, amount:int):
        self.desc = desc
        self.amount = amount

        # if file doesnt exist create and add fields into it
        if not os.path.exists(csv_file):
            with open(csv_file, 'w') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(csv_headers)

        # if file exists but empty, add fields into it
        if os.stat(csv_file).st_size == 0:
            with open(csv_file, 'w') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(csv_headers)

        # auto id increment
        # gets all values from ID column in csv file
        # based on the max value calculates the next ID
        ids = []
        with open(csv_file) as f:
            cf = csv.DictReader(f)
            for row in cf:
                ids.append(row['ID'])

        if len(ids) != 0:
            last_id = max(ids)
            next_id = int(last_id) + 1
        elif len(ids) == 0:
            next_id = 1
        
        rows = [next_id, str(datetime.datetime.now().strftime("%m-%d-%Y")), self.desc, self.amount]

        with open(csv_file, 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(rows)

    def delete_expense(self, id:int):
        # add the ting if ID specified not in the csv file

        df = pandas.read_csv(csv_file)
        df = df[df['ID'] != id]
        df.to_csv(csv_file, index=False)


    def list_expenses(self):
        # opens and reads file, then pretty prints the output from csv
        if not os.path.exists(csv_file):
            print(f'File "{csv_file}" currently does not exist.')
            print('Please add an expense to create the file.')
        
        if os.stat(csv_file).st_size == 0:
            print(f'File "{csv_file}" is empty.')
            print('Please add an expense.', end='')

        with open(csv_file, newline='') as f:
            csv_pretty_print = csv.reader(f)
            print(tabulate(csv_pretty_print, headers='firstrow', tablefmt='pipe', numalign='left'))

    def expense_summary(self):
        # sums up all of the expense amounts
        amounts = []
        with open(csv_file) as f:
            cf = csv.DictReader(f)
            for row in cf:
                amounts.append(row['Amount'])
            
        if len(amounts) != 0:
            total = [int(x) for x in amounts]
            summary = sum(total)
        elif len(amounts) == 0:
            summary = 0

        print(f'Total expenses: ${summary}')

# 'add' command to add an expense
@expenses_app.command(help='Add a new expense')
def add(
    description: Annotated[str, typer.Option(help='Description of the expense')],
    amount: Annotated[int, typer.Option(help='Amount for the expense')]
):
    new_expense = Expense()
    new_expense.add_expense(description, amount)

# 'delete' command to delete an existing expense
@expenses_app.command(help='Delete an expense')
def delete(
    id: Annotated[int, typer.Option(help='ID of an expense to delete')]
):
    delete_expense = Expense()
    delete_expense.delete_expense(id)


# 'list' command, lists all expenses
@expenses_app.command(help='List expenses')
def list():
    list_expenses = Expense()
    list_expenses.list_expenses()

# 'summary' command, prints out sum of all expenses
@expenses_app.command(help='List total amount for the expenses')
def summary():
    sum_expenses = Expense()
    sum_expenses.expense_summary()

if __name__ == "__main__":
    expenses_app()


"""
ADD LIKE A FUNCTION OR SOMETHING TO MAKE CODE MORE CONCISE,
INSTEAD OF REPEATING THE SAME CHECK FILE AND CHECK FILE SIZE IN EVERY CLASS METHOD;

THINKING EITHER A TING WITH A FUNCTION FOR EVERY TYPER COMMAND
OR IDK SOME SHIT TO HAVE IT CHECK ONCE AT THE BEGINNING AND NOT EVERY TIME
"""
