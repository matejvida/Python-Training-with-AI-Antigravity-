"""Coffee Machine Simulator.

This module simulates an automated coffee vending machine. It handles:
1. User drink selection (espresso, latte, cappuccino).
2. Secret maintainer commands ('off' to shut down, 'report' for resource levels).
3. Resource sufficiency checking (water, milk, coffee).
4. Coin processing (quarters, dimes, nickels, pennies).
5. Financial transaction verification and change calculation.
6. Resource inventory deduction and drink dispensing.

Educational Concepts Covered:
- Nested dictionary data structures.
- Function design with type hint annotations (Python 3.10+ syntax).
- Helper function decomposition for single-responsibility logic.
- Input validation and floating-point rounding.
"""

from __future__ import annotations
from typing import Callable, Any

# ==============================================================================
# MENU & RESOURCE CONSTANTS
# ==============================================================================

# Nested dictionary holding drink recipes (ingredients) and prices in USD ($).
MENU: dict[str, dict[str, Any]] = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk": 0,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    },
}

# Initial quantities of ingredients available in the machine.
INITIAL_RESOURCES: dict[str, int] = {
    "water": 300,  # in milliliters (ml)
    "milk": 200,   # in milliliters (ml)
    "coffee": 100, # in grams (g)
}

# Coin values in USD ($)
COIN_VALUES: dict[str, float] = {
    "quarters": 0.25,
    "dimes": 0.10,
    "nickels": 0.05,
    "pennies": 0.01,
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_report(resources: dict[str, int], profit: float, output_func: Callable[[str], None] = print) -> None:
    """Print the current resource levels and total monetary profit.

    Args:
        resources: Dictionary containing current amounts of 'water', 'milk', and 'coffee'.
        profit: Total money accumulated by the machine in USD ($).
        output_func: Callable function used for printing output (defaults to built-in print).
    """
    output_func(f"Water: {resources['water']}ml")
    output_func(f"Milk: {resources['milk']}ml")
    output_func(f"Coffee: {resources['coffee']}g")
    output_func(f"Money: ${profit}")


def is_resource_sufficient(order_ingredients: dict[str, int], current_resources: dict[str, int]) -> tuple[bool, str | None]:
    """Check if the machine has enough resources to fulfill a drink order.

    Args:
        order_ingredients: Dict of ingredient amounts required for the drink.
        current_resources: Dict of currently available ingredient amounts in the machine.

    Returns:
        A tuple of (is_sufficient: bool, missing_ingredient_name: str | None).
        If sufficient, returns (True, None).
        If insufficient, returns (False, missing_item_name).
    """
    for item, required_amount in order_ingredients.items():
        if required_amount > current_resources.get(item, 0):
            return False, item
    return True, None


def process_coins(input_func: Callable[[str], str] = input, output_func: Callable[[str], None] = print) -> float:
    """Prompt user to insert coins and calculate total monetary value inserted.

    Args:
        input_func: Function used to gather input (defaults to standard input).
        output_func: Function used for displaying messages (defaults to standard print).

    Returns:
        Total value of coins inserted in USD ($), rounded to 2 decimal places.
    """
    output_func("Please insert coins.")
    total = 0.0
    
    for coin_name, coin_value in COIN_VALUES.items():
        while True:
            raw_val = input_func(f"How many {coin_name}?: ").strip()
            try:
                count = int(raw_val)
                if count < 0:
                    output_func("Coin count cannot be negative. Please enter a valid number.")
                    continue
                total += count * coin_value
                break
            except ValueError:
                output_func("Invalid entry. Please enter a whole number.")

    return round(total, 2)


def is_transaction_successful(money_received: float, drink_cost: float) -> tuple[bool, float]:
    """Check if inserted money covers the drink cost and compute change.

    Args:
        money_received: Total monetary value inserted by user ($).
        drink_cost: Price of the selected drink ($).

    Returns:
        A tuple of (success: bool, change: float).
        If money is insufficient, change is 0.0 and success is False.
        If money is sufficient/excess, change is calculated and success is True.
    """
    if money_received < drink_cost:
        return False, 0.0
    
    change = round(money_received - drink_cost, 2)
    return True, change


def make_coffee(drink_name: str, order_ingredients: dict[str, int], current_resources: dict[str, int]) -> None:
    """Deduct required ingredients from current machine resources.

    Args:
        drink_name: Name of the drink being prepared.
        order_ingredients: Ingredients required for the drink.
        current_resources: Dict of current resources to be updated in-place.
    """
    for item, amount in order_ingredients.items():
        current_resources[item] -= amount


# ==============================================================================
# MAIN PROGRAM LOOP
# ==============================================================================

def run_coffee_machine(input_func: Callable[[str], str] = input, output_func: Callable[[str], None] = print) -> None:
    """Run the main coffee machine interactive prompt loop.

    Args:
        input_func: Callable for user input.
        output_func: Callable for program output.
    """
    resources = INITIAL_RESOURCES.copy()
    profit = 0.0
    is_on = True

    while is_on:
        user_choice = input_func("What would you like? (espresso/latte/cappuccino): ").strip().lower()

        if user_choice == "off":
            is_on = False
        elif user_choice == "report":
            print_report(resources, profit, output_func)
        elif user_choice in MENU:
            drink = MENU[user_choice]
            ingredients = drink["ingredients"]
            cost = drink["cost"]

            # Step 1: Check resource sufficiency
            sufficient, missing_resource = is_resource_sufficient(ingredients, resources)
            if not sufficient:
                output_func(f"Sorry there is not enough {missing_resource}.")
                continue

            # Step 2: Collect coins
            payment = process_coins(input_func, output_func)

            # Step 3: Check transaction success
            success, change = is_transaction_successful(payment, cost)
            if not success:
                output_func("Sorry that's not enough money. Money refunded.")
                continue

            # Step 4: Process transaction & dispense coffee
            profit += cost
            if change > 0:
                output_func(f"Here is ${change:.2f} dollars in change.")
            
            make_coffee(user_choice, ingredients, resources)
            output_func(f"Here is your {user_choice}. Enjoy!")
        else:
            output_func("Invalid choice. Please select 'espresso', 'latte', 'cappuccino', 'report', or 'off'.")


if __name__ == "__main__":
    run_coffee_machine()
