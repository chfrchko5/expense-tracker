import csv
import typer
from typing import Annotated, Optional
import datetime
import os
from tabulate import tabulate
import pandas
import sys

expenses_app = typer.Typer(help='Application to track your expenses')

csv_file = 'expenses.csv'
csv_headers = ['ID', 'Date', 'Description', 'Amount']

def check_file(file):
    if not os.path.exists(file):
        return False
    elif os.stat(file).st_size == 0:
        return 0
    else:
        return True

class Expense:
    def add_expense(self, desc:str, amount:int):
        self.desc = desc
        self.amount = amount

        if check_file(csv_file) == False:
            with open(csv_file, 'w') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(csv_headers)
        elif check_file(csv_file) == 0:   
            with open(csv_file, 'w') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(csv_headers)  
        elif check_file(csv_file) == True:
            pass
        else:
            print()
            sys.exit(1)
            
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
        if check_file(csv_file) == False or check_file(csv_file) == 0:
            print("There are no available expense records to delete")
        else:
            ids = []
            with open(csv_file) as f:
                cf = csv.DictReader(f)
                for row in cf:
                    ids.append(row['ID'])
            if str(id) not in ids:
                print('ID specified does not exist')
            elif str(id) in ids:
                df = pandas.read_csv(csv_file)
                df = df[df['ID'] != id]
                df.to_csv(csv_file, index=False)


    def list_expenses(self):
        # opens and reads file, then pretty prints the output from csv
        if check_file(csv_file) == False or check_file(csv_file) == 0:
            print(f'File "{csv_file}" currently does not exist or is empty.')
            print('Please add an expense to create/fill the file.')
        else:
            with open(csv_file, newline='') as f:
                csv_pretty_print = csv.reader(f)
                print(tabulate(csv_pretty_print, headers='firstrow', tablefmt='pipe', numalign='left'))

    def expense_summary(self, month=None):
        if check_file(csv_file) == False or check_file(csv_file) == 0:
            print(f'File "{csv_file}" currently does not exist or is empty.')
        else:
        # sums up all of the expense amounts
            if month == None:
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
            elif 1 <= month <= 12:
                with open(csv_file) as f:
                    amounts = []
                    cf = csv.DictReader(f)
                    for row in cf:
                        date = datetime.datetime.strptime(row['Date'], "%m-%d-%Y")
                        if date.month == month:
                            amounts.append(row['Amount'])
                            if len(amounts) != 0:
                                total = [int(x) for x in amounts]
                                summary = sum(total)
                            elif len(amounts) == 0:
                                summary = 0
                        elif date.month != month:
                            print('No summaries for this month')
                            sys.exit(1)

                    match month:
                        case 1:
                            print(f"Summary for month January is ${summary}")
                        case 2:
                            print(f"Summary for month February is ${summary}")
                        case 3:
                            print(f"Summary for month March is ${summary}")
                        case 4:
                            print(f"Summary for month April is ${summary}")
                        case 5:
                            print(f"Summary for month May is ${summary}")
                        case 6:
                            print(f"Summary for month June is ${summary}")
                        case 7:
                            print(f"Summary for month July is ${summary}")
                        case 8:
                            print(f"Summary for month August is ${summary}")
                        case 9:
                            print(f"Summary for month September is ${summary}")
                        case 10:
                            print(f"Summary for month October is ${summary}")
                        case 11:
                            print(f"Summary for month November is ${summary}")
                        case 12:
                            print(f"Summary for month December is ${summary}")
                                    
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
def summary(
    month: Annotated[Optional[int], typer.Option(help="provide a number of the month to display summary for that month only")] = None
):
    if month is None:
        sum_expenses = Expense()
        sum_expenses.expense_summary(month)
    elif 1 <= month <= 12:
        sum_expenses = Expense()
        sum_expenses.expense_summary(month)
    else:
        print('Please provide a valid month number (e.g., 1 for january, 2 for february, etc.)')
        return

if __name__ == "__main__":
    expenses_app()