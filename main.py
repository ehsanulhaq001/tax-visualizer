from babel.numbers import format_currency
import sys
from tabulate import tabulate
from termcolor import colored
import importlib


def load_tax_slab(file_name):
    """Dynamically import the specified tax slab module."""
    try:
        module = importlib.import_module(file_name)
        return module.TAX_SLABS
    except ModuleNotFoundError:
        print(colored(f"Error: Tax slab file '{file_name}' not found.", "red"))
        print("Ensure the file exists and is correctly named.")
        sys.exit(1)


def calculate_tax(income, tax_slabs):
    """
    Calculate the total tax based on the given income and predefined tax slabs.
    """
    tax = 0
    prev_limit = 0

    for limit, rate in tax_slabs:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            break
    return tax


def format_currency_inr(amount):
    """Formats the given amount as INR currency."""
    return format_currency(amount, "INR", locale="en_IN")


def main(income, tax_slab_file):
    """
    Main function to calculate tax, display results in a tabular format, and apply color coding.
    """
    tax_slabs = load_tax_slab(tax_slab_file)
    tax = calculate_tax(income, tax_slabs)
    after_tax_income = income - tax

    formatted_tax = format_currency_inr(tax)
    formatted_after_tax_income = format_currency_inr(after_tax_income)
    formatted_income = format_currency_inr(income)

    # Prepare data for tabulation
    table_data = [
        [colored("Total Income", "cyan"), colored(formatted_income, "cyan")],
        [colored("Total Tax", "red"), colored(formatted_tax, "red")],
        [
            colored("Income After Tax", "green"),
            colored(formatted_after_tax_income, "green"),
        ],
    ]

    # Print tabulated results
    print(tabulate(table_data, headers=["Description", "Amount"], tablefmt="grid"))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(colored("Usage: python main.py <income> <tax_slab_file>", "yellow"))
        print("Example: python main.py 1200000 tax_slab_2024")
        sys.exit(1)

    try:
        income = float(sys.argv[1])
        tax_slab_file = sys.argv[2]
    except ValueError:
        print(colored("Error: Income must be a valid number.", "red"))
        sys.exit(1)

    main(income, tax_slab_file)
