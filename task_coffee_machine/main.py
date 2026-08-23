"""Retro CLI GUI Coffee Machine Simulator.

This module simulates an automated coffee vending machine with a retro ASCII UI:
1. Retro ASCII Logo & Boxed Menu Choices.
2. Animated Coin Insertion Tally.
3. Multi-stage Brewing & Progress Bar Animation.
4. Animated Warning Alerts (insufficient funds / depleted resources).
5. Animated Shutdown Sequence.
6. Support for zero-delay mode (animation_delay=0.0) for automated tests.

Educational Concepts Covered:
- ASCII art rendering & boxed UI layout generation.
- Dynamic terminal animation timing control (`time.sleep` abstraction).
- Configurable animation delay for clean unit testing without blocking execution.
- Function decomposition and modular CLI component design.
"""

from __future__ import annotations
import time
from typing import Callable, Any, Dict

# ==============================================================================
# MENU & RESOURCE CONSTANTS
# ==============================================================================

COFFEE_LOGO: str = r"""
  ____ ___  _____ _____ _____ _____   __  __    _    ____ _   _ ___ _   _ _____ 
 / ___/ _ \|  ___|  ___| ____| ____| |  \/  |  / \  / ___| | | |_ _| \ | | ____|
| |  | | | | |_  | |_  |  _| |  _|   | |\/| | / _ \| |   | |_| || ||  \| |  _|  
| |__| |_| |  _| |  _| | |___| |___  | |  | |/ ___ \ |___|  _  || || |\  | |___ 
 \____\___/|_|   |_|   |_____|_____| |_|  |_/_/   \_\____|_| |_|___|_| \_|_____|
"""

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

INITIAL_RESOURCES: dict[str, int] = {
    "water": 300,  # in ml
    "milk": 200,   # in ml
    "coffee": 100, # in g
}

COIN_VALUES: dict[str, float] = {
    "quarters": 0.25,
    "dimes": 0.10,
    "nickels": 0.05,
    "pennies": 0.01,
}

# ==============================================================================
# RETRO CLI GUI RENDERERS & ANIMATIONS
# ==============================================================================

def print_logo(output_func: Callable[[str], None] = print) -> None:
    """Print retro ASCII Coffee Machine banner."""
    output_func(COFFEE_LOGO)


def print_menu(output_func: Callable[[str], None] = print) -> None:
    """Print retro boxed ASCII menu displaying drinks, ingredients, and prices."""
    output_func("╔══════════════════════════════════════════════════════════════╗")
    output_func("║                   ☕  RETRO MENU CHOICES  ☕                  ║")
    output_func("╠══════════════════════════════════════════════════════════════╣")
    output_func("║  1. Espresso   - $1.50  (Water: 50ml,  Milk: 0ml,   Coffee: 18g)║")
    output_func("║  2. Latte      - $2.50  (Water: 200ml, Milk: 150ml, Coffee: 24g)║")
    output_func("║  3. Cappuccino - $3.00  (Water: 250ml, Milk: 100ml, Coffee: 24g)║")
    output_func("╚══════════════════════════════════════════════════════════════╝")


def animate_alert(
    message: str,
    alert_type: str = "warning",
    output_func: Callable[[str], None] = print,
    delay: float = 0.1,
) -> None:
    """Display a boxed retro alert notification with optional animation delay."""
    icon = "⚠️ " if alert_type == "warning" else "ℹ️ "
    border_char = "!" if alert_type == "warning" else "*"
    width = max(len(message) + 8, 40)
    top_border = border_char * width
    
    output_func(top_border)
    output_func(f"{border_char} {icon} {message.center(width - 6)} {border_char}")
    output_func(top_border)
    
    if delay > 0:
        time.sleep(delay)


def animate_shutdown(output_func: Callable[[str], None] = print, delay: float = 0.1) -> None:
    """Render retro power-down animation sequence."""
    steps = [
        "🔌 SHUTTING DOWN COFFEE MACHINE...",
        "💾 SAVING RESOURCE STATE...",
        "💤 POWER OFF COMPLETE. GOODBYE!"
    ]
    for step in steps:
        output_func(step)
        if delay > 0:
            time.sleep(delay)


def animate_brewing(
    drink_name: str,
    output_func: Callable[[str], None] = print,
    delay: float = 0.1,
) -> None:
    """Render multi-stage brewing animation and progress bar."""
    output_func(f"\n⚙️  STARTING PREPARATION FOR: {drink_name.upper()}")
    
    stages = [
        "[1/4] ⚙️  Grinding fresh coffee beans...",
        "[2/4] 💧  Heating water to optimal temperature...",
        "[3/4] 🥛  Steaming & frothing milk...",
        "[4/4] ☕  Brewing espresso shot & assembling drink..."
    ]
    
    for stage in stages:
        output_func(stage)
        if delay > 0:
            time.sleep(delay)

    # Progress bar animation
    progress_bar_length = 20
    for i in range(1, progress_bar_length + 1):
        percent = int((i / progress_bar_length) * 100)
        bar = "█" * i + "░" * (progress_bar_length - i)
        output_func(f"[{bar}] {percent}%")
        if delay > 0:
            time.sleep(delay / 5)

    ascii_cup = r"""
        (  )   (   )  )
         ) (   )  (  (
        ( )  (    ) )
        _____________
       |             |___
       |  RETRO COFFEE  |_
       |   ENJOY! ☕   | |
       |_____________|___|
        \___________/
    """
    output_func(ascii_cup)


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_report(
    resources: dict[str, int],
    profit: float,
    output_func: Callable[[str], None] = print,
) -> None:
    """Print the current resource levels and profit inside a retro ASCII box."""
    output_func("┌────────────────────────────────────────┐")
    output_func("│        COFFEE MACHINE REPORT           │")
    output_func("├────────────────────────────────────────┤")
    output_func(f"│  Water:  {str(resources['water']) + 'ml':<28} │")
    output_func(f"│  Milk:   {str(resources['milk']) + 'ml':<28} │")
    output_func(f"│  Coffee: {str(resources['coffee']) + 'g':<28} │")
    output_func(f"│  Money:  {'$' + f'{profit:.2f}':<28} │")
    output_func("└────────────────────────────────────────┘")


def is_resource_sufficient(
    order_ingredients: dict[str, int],
    current_resources: dict[str, int],
) -> tuple[bool, str | None]:
    """Check if the machine has enough resources for an order."""
    for item, required_amount in order_ingredients.items():
        if required_amount > current_resources.get(item, 0):
            return False, item
    return True, None


def process_coins(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    delay: float = 0.1,
) -> float:
    """Prompt user to insert coins with animated feedback tally."""
    output_func("\n🪙  PLEASE INSERT COINS")
    total = 0.0
    
    for coin_name, coin_value in COIN_VALUES.items():
        while True:
            raw_val = input_func(f"How many {coin_name}?: ").strip()
            try:
                count = int(raw_val)
                if count < 0:
                    animate_alert("Coin count cannot be negative.", "warning", output_func, delay)
                    continue
                added_val = count * coin_value
                total += added_val
                if count > 0:
                    output_func(f"  ➜ Added {count} {coin_name} (+${added_val:.2f}) | Running Total: ${total:.2f}")
                    if delay > 0:
                        time.sleep(delay / 2)
                break
            except ValueError:
                animate_alert("Invalid entry. Please enter a whole number.", "warning", output_func, delay)

    total_rounded = round(total, 2)
    output_func(f"💰 Total Coins Inserted: ${total_rounded:.2f}\n")
    return total_rounded


def is_transaction_successful(money_received: float, drink_cost: float) -> tuple[bool, float]:
    """Check if inserted money covers the drink cost and compute change."""
    if money_received < drink_cost:
        return False, 0.0
    
    change = round(money_received - drink_cost, 2)
    return True, change


def make_coffee(
    drink_name: str,
    order_ingredients: dict[str, int],
    current_resources: dict[str, int],
) -> None:
    """Deduct required ingredients from current machine resources."""
    for item, amount in order_ingredients.items():
        current_resources[item] -= amount


# ==============================================================================
# MAIN PROGRAM LOOP
# ==============================================================================

def run_coffee_machine(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    animation_delay: float = 0.1,
) -> None:
    """Run the retro CLI GUI coffee machine interactive prompt loop.

    Args:
        input_func: Callable for user input.
        output_func: Callable for program output.
        animation_delay: Time delay in seconds for animations (set to 0.0 for automated testing).
    """
    resources = INITIAL_RESOURCES.copy()
    profit = 0.0
    is_on = True

    print_logo(output_func)

    while is_on:
        print_menu(output_func)
        user_choice = input_func("\nWhat would you like? (espresso/latte/cappuccino): ").strip().lower()

        if user_choice == "off":
            animate_shutdown(output_func, animation_delay)
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
                animate_alert(f"Sorry there is not enough {missing_resource}.", "warning", output_func, animation_delay)
                continue

            # Step 2: Collect coins with animation
            payment = process_coins(input_func, output_func, animation_delay)

            # Step 3: Check transaction success
            success, change = is_transaction_successful(payment, cost)
            if not success:
                animate_alert("Sorry that's not enough money. Money refunded.", "warning", output_func, animation_delay)
                continue

            # Step 4: Process transaction, animate brewing & dispense drink
            profit += cost
            if change > 0:
                output_func(f"💵 Here is ${change:.2f} dollars in change.")
            
            make_coffee(user_choice, ingredients, resources)
            animate_brewing(user_choice, output_func, animation_delay)
            output_func(f"\n✨ Here is your {user_choice}. Enjoy!\n")
        else:
            animate_alert("Invalid choice. Select 'espresso', 'latte', 'cappuccino', 'report', or 'off'.", "warning", output_func, animation_delay)


if __name__ == "__main__":
    run_coffee_machine()
