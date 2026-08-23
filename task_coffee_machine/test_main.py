"""Unit and End-to-End (E2E) Test Suite with Custom JSON Test Reporter.

This test suite covers:
- Retro CLI GUI renders (logo, boxed menu, brewing animation, shutdown animation).
- Resource sufficiency checks & coin processing.
- Transaction validation (exact payment, change calculation, insufficient funds).
- Resource deduction.
- Full E2E CLI interactions simulating user inputs with animation_delay=0.0.
- Custom JSON Test Runner exporting execution date, pass/fail ratios, and test details
  to `task_coffee_machine/test_results.json` for web dashboard visualization.
"""

from __future__ import annotations
import json
import os
import sys
import time
import unittest
from datetime import datetime, timezone
from typing import List, Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task_coffee_machine.main import (
    MENU,
    INITIAL_RESOURCES,
    COFFEE_LOGO,
    print_logo,
    print_menu,
    print_report,
    animate_alert,
    animate_brewing,
    animate_shutdown,
    is_resource_sufficient,
    process_coins,
    is_transaction_successful,
    make_coffee,
    run_coffee_machine,
)


# ==============================================================================
# CUSTOM JSON TEST RUNNER & RESULT LISTENER
# ==============================================================================

class JSONTestResult(unittest.TestResult):
    """Custom TestResult collector that prints live progress logs and exports formatted JSON."""

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.test_records: List[Dict[str, Any]] = []
        self.failed_records: List[Dict[str, Any]] = []
        self.start_time: float = 0.0
        self.test_start_time: float = 0.0

    def startTestRun(self):
        self.start_time = time.time()
        print("\n" + "=" * 70)
        print("          ☕ COFFEE MACHINE AUTOMATED TEST SUITE EXECUTION ☕")
        print("=" * 70)

    def startTest(self, test: unittest.TestCase):
        super().startTest(test)
        self.test_start_time = time.time()

    def addSuccess(self, test: unittest.TestCase):
        super().addSuccess(test)
        elapsed = round(time.time() - self.test_start_time, 4)
        tc_id = getattr(test, "_testMethodName", str(test))
        class_name = test.__class__.__name__
        log_msg = f"[EXEC] Running {class_name}.{tc_id}... [PASS] ({elapsed}s)"
        print(log_msg)

        self.test_records.append({
            "id": tc_id,
            "name": tc_id,
            "class_name": class_name,
            "status": "PASS",
            "duration_seconds": elapsed,
            "logs": log_msg
        })

    def addFailure(self, test: unittest.TestCase, err):
        super().addFailure(test, err)
        elapsed = round(time.time() - self.test_start_time, 4)
        tc_id = getattr(test, "_testMethodName", str(test))
        class_name = test.__class__.__name__
        err_msg = self._exc_info_to_string(err, test)
        log_msg = f"[EXEC] Running {class_name}.{tc_id}... [FAIL] ({elapsed}s)"
        print(log_msg)

        record = {
            "id": tc_id,
            "name": tc_id,
            "class_name": class_name,
            "status": "FAIL",
            "duration_seconds": elapsed,
            "error_message": str(err[1]),
            "traceback": err_msg,
            "logs": log_msg
        }
        self.test_records.append(record)
        self.failed_records.append(record)

    def addError(self, test: unittest.TestCase, err):
        super().addError(test, err)
        elapsed = round(time.time() - self.test_start_time, 4)
        tc_id = getattr(test, "_testMethodName", str(test))
        class_name = test.__class__.__name__
        err_msg = self._exc_info_to_string(err, test)
        log_msg = f"[EXEC] Running {class_name}.{tc_id}... [ERROR] ({elapsed}s)"
        print(log_msg)

        record = {
            "id": tc_id,
            "name": tc_id,
            "class_name": class_name,
            "status": "ERROR",
            "duration_seconds": elapsed,
            "error_message": str(err[1]),
            "traceback": err_msg,
            "logs": log_msg
        }
        self.test_records.append(record)
        self.failed_records.append(record)

    def generate_json_report(self, filepath: str) -> None:
        total_duration = round(time.time() - self.start_time, 4)
        total_tests = len(self.test_records)
        passed_count = sum(1 for t in self.test_records if t["status"] == "PASS")
        failed_count = sum(1 for t in self.test_records if t["status"] == "FAIL")
        error_count = sum(1 for t in self.test_records if t["status"] == "ERROR")
        skipped_count = len(self.skipped)

        success_rate = round((passed_count / total_tests * 100), 2) if total_tests > 0 else 0.0
        failure_rate = round(((failed_count + error_count) / total_tests * 100), 2) if total_tests > 0 else 0.0

        report_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_count,
                "failed": failed_count,
                "errors": error_count,
                "skipped": skipped_count,
                "success_rate_percent": success_rate,
                "failure_rate_percent": failure_rate,
                "duration_seconds": total_duration
            },
            "failed_test_cases": self.failed_records,
            "test_cases": self.test_records
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        print("-" * 70)
        print("📊 EXECUTION SUMMARY:")
        print(f"  - Date & Time: {report_data['timestamp']}")
        print(f"  - Total Tests: {total_tests} | Passed: {passed_count} | Failed: {failed_count} | Errors: {error_count}")
        print(f"  - Success Rate: {success_rate:.2f}% | Failure Rate: {failure_rate:.2f}%")
        print(f"  - Total Duration: {total_duration}s")
        print(f"  - JSON Report Exported: {filepath}")
        print("=" * 70 + "\n")


class JSONTestRunner:
    """Runner class that executes test suite and outputs test_results.json."""

    def __init__(self, report_filename: str = "test_results.json"):
        self.report_filepath = os.path.join(os.path.dirname(__file__), report_filename)

    def run(self, test_suite: unittest.TestSuite) -> JSONTestResult:
        result = JSONTestResult()
        result.startTestRun()
        test_suite.run(result)
        result.generate_json_report(self.report_filepath)
        return result


# ==============================================================================
# TEST CASES
# ==============================================================================

class TestCoffeeMachineUnit(unittest.TestCase):
    """Unit tests for individual Coffee Machine helper and GUI functions."""

    def test_print_logo(self) -> None:
        """Verify print_logo renders the ASCII banner."""
        output_lines: List[str] = []
        print_logo(output_func=output_lines.append)
        self.assertIn(COFFEE_LOGO, output_lines)

    def test_print_menu(self) -> None:
        """Verify print_menu renders boxed retro menu choices."""
        output_lines: List[str] = []
        print_menu(output_func=output_lines.append)
        menu_text = "\n".join(output_lines)
        self.assertIn("RETRO MENU CHOICES", menu_text)
        self.assertIn("Espresso", menu_text)
        self.assertIn("Latte", menu_text)
        self.assertIn("Cappuccino", menu_text)

    def test_print_report(self) -> None:
        """Verify print_report formats output in a retro ASCII box."""
        output_lines: List[str] = []
        sample_resources = {"water": 100, "milk": 50, "coffee": 76}
        sample_profit = 2.5

        print_report(sample_resources, sample_profit, output_func=output_lines.append)
        report_text = "\n".join(output_lines)
        self.assertIn("COFFEE MACHINE REPORT", report_text)
        self.assertIn("Water:  100ml", report_text)
        self.assertIn("Milk:   50ml", report_text)
        self.assertIn("Coffee: 76g", report_text)
        self.assertIn("Money:  $2.50", report_text)

    def test_animate_alert(self) -> None:
        """Verify animate_alert renders boxed alert messages."""
        output_lines: List[str] = []
        animate_alert("Test Alert", "warning", output_func=output_lines.append, delay=0.0)
        alert_text = "\n".join(output_lines)
        self.assertIn("Test Alert", alert_text)

    def test_animate_brewing(self) -> None:
        """Verify animate_brewing renders multi-stage progress and ASCII cup."""
        output_lines: List[str] = []
        animate_brewing("latte", output_func=output_lines.append, delay=0.0)
        brew_text = "\n".join(output_lines)
        self.assertIn("STARTING PREPARATION FOR: LATTE", brew_text)
        self.assertIn("Grinding fresh coffee beans", brew_text)
        self.assertIn("RETRO COFFEE", brew_text)

    def test_animate_shutdown(self) -> None:
        """Verify animate_shutdown renders power-off sequence."""
        output_lines: List[str] = []
        animate_shutdown(output_func=output_lines.append, delay=0.0)
        shutdown_text = "\n".join(output_lines)
        self.assertIn("SHUTTING DOWN COFFEE MACHINE", shutdown_text)
        self.assertIn("POWER OFF COMPLETE", shutdown_text)

    def test_is_resource_sufficient_true(self) -> None:
        """Verify is_resource_sufficient returns True when resources are sufficient."""
        latte_ingredients = MENU["latte"]["ingredients"]
        current_resources = {"water": 300, "milk": 200, "coffee": 100}

        sufficient, missing = is_resource_sufficient(latte_ingredients, current_resources)
        self.assertTrue(sufficient)
        self.assertIsNone(missing)

    def test_is_resource_sufficient_false_water(self) -> None:
        """Verify is_resource_sufficient returns False when water is low."""
        latte_ingredients = MENU["latte"]["ingredients"]
        current_resources = {"water": 100, "milk": 200, "coffee": 100}

        sufficient, missing = is_resource_sufficient(latte_ingredients, current_resources)
        self.assertFalse(sufficient)
        self.assertEqual(missing, "water")

    def test_is_resource_sufficient_false_milk(self) -> None:
        """Verify is_resource_sufficient returns False when milk is low."""
        cappuccino_ingredients = MENU["cappuccino"]["ingredients"]
        current_resources = {"water": 300, "milk": 50, "coffee": 100}

        sufficient, missing = is_resource_sufficient(cappuccino_ingredients, current_resources)
        self.assertFalse(sufficient)
        self.assertEqual(missing, "milk")

    def test_is_resource_sufficient_false_coffee(self) -> None:
        """Verify is_resource_sufficient returns False when coffee is low."""
        espresso_ingredients = MENU["espresso"]["ingredients"]
        current_resources = {"water": 300, "milk": 200, "coffee": 10}

        sufficient, missing = is_resource_sufficient(espresso_ingredients, current_resources)
        self.assertFalse(sufficient)
        self.assertEqual(missing, "coffee")

    def test_process_coins_valid(self) -> None:
        """Verify process_coins accurately calculates monetary total."""
        inputs = iter(["1", "2", "1", "2"])
        output_lines: List[str] = []

        total = process_coins(input_func=lambda _: next(inputs), output_func=output_lines.append, delay=0.0)
        self.assertEqual(total, 0.52)

    def test_process_coins_retry_negative(self) -> None:
        """Verify process_coins handles negative number inputs."""
        inputs = iter(["-1", "1", "0", "0", "0"])
        output_lines: List[str] = []

        total = process_coins(input_func=lambda _: next(inputs), output_func=output_lines.append, delay=0.0)
        self.assertEqual(total, 0.25)
        text = "\n".join(output_lines)
        self.assertIn("Coin count cannot be negative", text)

    def test_is_transaction_successful_exact(self) -> None:
        """Verify exact payment returns success=True and change=0.0."""
        success, change = is_transaction_successful(2.50, 2.50)
        self.assertTrue(success)
        self.assertEqual(change, 0.0)

    def test_is_transaction_successful_excess(self) -> None:
        """Verify excess payment returns success=True and correct change."""
        success, change = is_transaction_successful(3.00, 2.50)
        self.assertTrue(success)
        self.assertEqual(change, 0.50)

    def test_is_transaction_successful_insufficient(self) -> None:
        """Verify insufficient payment returns success=False."""
        success, change = is_transaction_successful(0.52, 2.50)
        self.assertFalse(success)
        self.assertEqual(change, 0.0)

    def test_make_coffee(self) -> None:
        """Verify make_coffee deducts ingredients correctly."""
        current_resources = {"water": 300, "milk": 200, "coffee": 100}
        latte_ingredients = {"water": 200, "milk": 150, "coffee": 24}

        make_coffee("latte", latte_ingredients, current_resources)

        self.assertEqual(current_resources["water"], 100)
        self.assertEqual(current_resources["milk"], 50)
        self.assertEqual(current_resources["coffee"], 76)


class TestCoffeeMachineE2E(unittest.TestCase):
    """End-to-End simulation tests for the Retro CLI Coffee Machine application."""

    def test_e2e_successful_latte_purchase(self) -> None:
        """Simulate buying a Latte with $2.50, checking brewing animation and report update."""
        user_inputs = iter([
            "latte",
            "10", "0", "0", "0",
            "report",
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append, animation_delay=0.0)

        full_output = "\n".join(output_lines)
        self.assertIn("Here is your latte. Enjoy!", full_output)
        self.assertIn("Water:  100ml", full_output)
        self.assertIn("Milk:   50ml", full_output)
        self.assertIn("Coffee: 76g", full_output)
        self.assertIn("Money:  $2.50", full_output)

    def test_e2e_insufficient_funds_latte(self) -> None:
        """Simulate buying a Latte with $0.52, verifying refund warning and un-altered inventory."""
        user_inputs = iter([
            "latte",
            "1", "2", "1", "2",
            "report",
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append, animation_delay=0.0)

        full_output = "\n".join(output_lines)
        self.assertIn("Sorry that's not enough money. Money refunded.", full_output)
        self.assertIn("Water:  300ml", full_output)
        self.assertIn("Milk:   200ml", full_output)
        self.assertIn("Coffee: 100g", full_output)
        self.assertIn("Money:  $0.00", full_output)

    def test_e2e_insufficient_resource_depletion(self) -> None:
        """Simulate ordering two Cappuccinos to deplete water and verify refusal on 2nd order."""
        user_inputs = iter([
            "cappuccino",
            "12", "0", "0", "0",
            "cappuccino",
            "off"
        ])
        output_lines: List[str] = []

        run_coffee_machine(input_func=lambda _: next(user_inputs), output_func=output_lines.append, animation_delay=0.0)

        full_output = "\n".join(output_lines)
        self.assertIn("Here is your cappuccino. Enjoy!", full_output)
        self.assertIn("Sorry there is not enough water.", full_output)


# ==============================================================================
# MAIN TEST EXECUTION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = JSONTestRunner(report_filename="test_results.json")
    runner.run(suite)
