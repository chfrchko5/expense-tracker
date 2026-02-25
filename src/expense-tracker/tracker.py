import csv
from csv import reader
import typer
from typing import Annotated
import datetime
import os
from tabulate import tabulate

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

    def list_expenses(self):
        with open(csv_file, 'r') as f:
            csv_pretty_print = csv.reader(f)
            print(tabulate(csv_pretty_print, headers='firstrow', tablefmt='pipe'))
            
# temporary arguments and stuff
# change adjust later
@expenses_app.command(help='Add a new expense')
def add(
    description: Annotated[str, typer.Option(help='Description of the expense')],
    amount: Annotated[int, typer.Option(help='Amount for the expense')]
):
    new_expense = Expense()
    new_expense.add_expense(description, amount)

@expenses_app.command(help='List expenses')
def list():
    list_expenses = Expense()
    list_expenses.list_expenses()

if __name__ == "__main__":
    expenses_app()





# Strategy B – Scan all IDs and find max

# Read all rows

# Extract ID column

# Convert to integers

# Use something like max(...)

# Add 1

# This is safer if:

# Rows might get deleted

# The file might not be sorted

# You want robustness