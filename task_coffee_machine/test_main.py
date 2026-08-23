"""Unit and End-to-End (E2E) Test Suite for Coffee Machine Program.

This test suite covers:
- Resource checking functions.
- Coin processing logic.
- Financial transaction calculations (exact payment, change calculation, insufficient funds).
- Resource deduction.
- Full E2E CLI interactions simulating user inputs and inspecting output streams.
"""

from __future__ import annotations
import unittest
from typing import List
from task_coffee_machine.main import (
    MENU,
    INITIAL_RESOURCES,
    print_report,
    is_resource_sufficient,
    process_coins,
    is_transaction_successful,
    make_coffee,
    run_coffee_machine,
)


class TestCoffeeMachineUnit(unittest.TestCase):
    """Unit tests for individual Coffee Machine helper functions."""

    def test_print_report(self) -> None:
        """Verify print_report formats output correctly with resource levels and profit."""
        output_lines: List[str] = []
        sample_resources = {"water": 100, "milk": 50, "coffee": 76}
        sample_profit = 2.5

        print_report(sample_resources, sample_profit, output_func=output_lines.append)

        expected_lines = [
            "Water: 100ml",
            "Milk: 50ml",
            "Coffee: 76g",
            "Money: $2.5",
        ]
        self.assertEqual(output_lines, expected_lines)

    def test_is_resource_sufficient_true(self) -> None:
        """Verify is_resource_sufficient returns True when resources exceed recipe needs."""
        latte_ingredients = MENU["latte"]["ingredients"]
        current_resources = {"water": 300, "milk": 200, "coffee": 100}

        sufficient, missing = is_resource_sufficient(latte_ingredients, current_resources)
        self.assertTrue(sufficient)
        self.assertIsNone(missing)

    def test_is_resource_sufficient_false_water(self) -> None:
        """Verify is_resource_sufficient returns False and missing resource name when water is low."""
        latte_ingredients = MENU["latte"]["ingredients"]  # Requires 200ml water
        current_resources = {"water": 100, "milk": 200, "coffee": 100}

        sufficient, missing = is_resource_sufficient(latte_ingredients, current_resources)
        self.assertFalse(sufficient)
        self.assertEqual(missing, "water")

    def test_is_resource_sufficient_false_milk(self) -> None:
        """Verify is_resource_sufficient returns False when milk is low."""
        cappuccino_ingredients = MENU["cappuccino"]["ingredients"]  # Requires 100ml milk
        current_resources = {"water": 300, "milk": 50, "coffee": 100}

        sufficient, missing = is_resource_sufficient(cappuccino_ingredients, current_resources)
        self.assertFalse(sufficient)
        self.assertEqual(missing, "milk")

    def test_is_resource_sufficient_false_coffee(self) -> None:
        """Verify is_resource_sufficient returns False when coffee is low."""
        espresso_ingredients = MENU["espresso"]["ingredients"]  # Requires 18g coffee
        current_resources = {"water": 300, "milk": 200, "coffee": 10}

        sufficient, missing = is_resource_sufficient(espresso_ingredients, current_resources)
        self.assertFalse(sufficient)
        self.assertEqual(missing, "coffee")

    def test_process_coins_valid(self) -> None:
        """Verify process_coins accurately calculates monetary total for valid coin counts."""
        # Insert: 1 quarter (0.25), 2 dimes (0.20), 1 nickel (0.05), 2 pennies (0.02) = 0.52
        inputs = iter(["1", "2", "1", "2"])
        output_lines: List[str] = []

        total = process_coins(input_func=lambda _: next(inputs), output_func=output_lines.append)
        self.assertEqual(total, 0.52)

    def test_process_coins_retry_negative(self) -> None:
        """Verify process_coins prompts retry when negative or invalid number is entered."""
        # Quarters: "-1", then "1" (0.25). Dimes: "0", Nickels: "0", Pennies: "0"
        inputs = iter(["-1", "1", "0", "0", "0"])
        output_lines: List[str] = []

        total = process_coins(input_func=lambda _: next(inputs), output_func=output_lines.append)
        self.assertEqual(total, 0.25)
        self.assertIn("Coin count cannot be negative. Please enter a valid number.", output_lines)

    def test_is_transaction_successful_exact(self) -> None:
        """Verify exact payment returns success=True and change=0.0."""
        success, change = is_transaction_successful(2.50, 2.50)
        self.assertTrue(success)
        self.assertEqual(change, 0.0)

    def test_is_transaction_successful_excess(self) -> None:
        """Verify excess payment returns success=True and correct rounded change."""
        # $3.00 inserted for $2.50 drink -> $0.50 change
        success, change = is_transaction_successful(3.00, 2.50)
        self.assertTrue(success)
        self.assertEqual(change, 0.50)

    def test_is_transaction_successful_insufficient(self) -> None:
        """Verify insufficient payment returns success=False and change=0.0."""
        # $0.52 inserted for $2.50 drink -> failed
        success, change = is_transaction_successful(0.52, 2.50)
        self.assertFalse(success)
        self.assertEqual(change, 0.0)

    def test_make_coffee(self) -> None:
        """Verify make_coffee correctly deducts ingredients from current resources."""
        current_resources = {"water": 300, "milk": 200, "coffee": 100}
        latte_ingredients = {"water": 200, "milk": 150, "coffee": 24}

        make_coffee("latte", latte_ingredients, current_resources)

        self.assertEqual(current_resources["water"], 100)
        self.assertEqual(current_resources["milk"], 50)
        self.assertEqual(current_resources["coffee"], 76)


class TestCoffeeMachineE2E(unittest.TestCase):
    """End-to-End simulation tests for the Coffee Machine CLI application."""

    def test_e2e_successful_latte_purchase(self) -> None:
        """Simulate buying a Latte with 10 quarters ($2.50), checking drink output and report update."""
        # Inputs:
        # 1. "latte"
        # 2. Quarters: 10 ($2.50), Dimes: 0, Nickels: 0, Pennies: 0
        # 3. "report"
        # 4. "off"
        user_inputs = iter([
            "latte",
            "10", "0", "0", "0",
            "report",
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append)

        self.assertIn("Here is your latte. Enjoy!", output_lines)
        self.assertIn("Water: 100ml", output_lines)
        self.assertIn("Milk: 50ml", output_lines)
        self.assertIn("Coffee: 76g", output_lines)
        self.assertIn("Money: $2.5", output_lines)

    def test_e2e_insufficient_funds_latte(self) -> None:
        """Simulate buying a Latte with only $0.52 inserted, verifying refund and unchanged report."""
        # Inputs:
        # 1. "latte"
        # 2. Quarters: 1, Dimes: 2, Nickels: 1, Pennies: 2 ($0.52)
        # 3. "report"
        # 4. "off"
        user_inputs = iter([
            "latte",
            "1", "2", "1", "2",
            "report",
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append)

        self.assertIn("Sorry that's not enough money. Money refunded.", output_lines)
        self.assertIn("Water: 300ml", output_lines)
        self.assertIn("Milk: 200ml", output_lines)
        self.assertIn("Coffee: 100g", output_lines)
        self.assertIn("Money: $0.0", output_lines)

    def test_e2e_insufficient_resource_depletion(self) -> None:
        """Simulate ordering two Cappuccinos to deplete water/milk and verify refusal on 2nd order."""
        # Initial: Water 300ml, Milk 200ml
        # Cappuccino #1 requires 250ml water, 100ml milk ($3.00) -> Remaining: Water 50ml, Milk 100ml
        # Cappuccino #2 requires 250ml water -> Insufficient water!
        user_inputs = iter([
            "cappuccino",
            "12", "0", "0", "0",  # 12 quarters = $3.00
            "cappuccino",         # Should fail due to water
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append)

        self.assertIn("Here is your cappuccino. Enjoy!", output_lines)
        self.assertIn("Sorry there is not enough water.", output_lines)

    def test_e2e_report_and_off(self) -> None:
        """Verify prompt handles report immediately and shuts down cleanly on 'off'."""
        user_inputs = iter([
            "report",
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append)

        self.assertIn("Water: 300ml", output_lines)
        self.assertIn("Milk: 200ml", output_lines)
        self.assertIn("Coffee: 100g", output_lines)
        self.assertIn("Money: $0.0", output_lines)


if __name__ == "__main__":
    unittest.main()
