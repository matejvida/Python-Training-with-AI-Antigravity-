# Test Case Specification: Retro CLI GUI Coffee Machine

This document details all test scenarios designed to validate the retro CLI GUI interface, functional requirements, coin processing, animations, and JSON test report generation. Each test case maps directly to [`test_main.py`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py).

---

## 1. Retro GUI & UI Unit Test Scenarios

### TC-U01: Retro Logo Banner Rendering
- **Goal**: Verify `print_logo` renders the ASCII Coffee Machine header banner.
- **Code Reference**: [`TestCoffeeMachineUnit.test_print_logo`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U02: Boxed Retro Menu Choices Rendering
- **Goal**: Confirm `print_menu` renders the boxed retro drink selection table with prices and recipes.
- **Code Reference**: [`TestCoffeeMachineUnit.test_print_menu`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U03: Boxed Maintainer Report Rendering
- **Goal**: Confirm `print_report` formats resource inventory and total profit inside a retro ASCII box.
- **Code Reference**: [`TestCoffeeMachineUnit.test_print_report`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U04: Animated Warning Alerts
- **Goal**: Verify `animate_alert` produces boxed alert messages for warnings and refunds.
- **Code Reference**: [`TestCoffeeMachineUnit.test_animate_alert`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U05: Multi-Stage Brewing & Progress Bar Animation
- **Goal**: Confirm `animate_brewing` outputs brewing stages (`Grinding`, `Heating water`, `Steaming milk`, `Brewing`), progress bar, and final ASCII coffee cup.
- **Code Reference**: [`TestCoffeeMachineUnit.test_animate_brewing`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U06: Shutdown Sequence Animation
- **Goal**: Confirm `animate_shutdown` renders the multi-step power-down sequence upon receiving the `"off"` command.
- **Code Reference**: [`TestCoffeeMachineUnit.test_animate_shutdown`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

---

## 2. Functional & Transaction Unit Scenarios

### TC-U07: Resource Sufficiency - All Available
- **Goal**: Confirm `is_resource_sufficient` returns `(True, None)` when resources exceed recipe needs.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_true`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U08: Resource Sufficiency - Insufficient Water
- **Goal**: Confirm `is_resource_sufficient` detects water shortage.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_false_water`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U09: Resource Sufficiency - Insufficient Milk
- **Goal**: Confirm `is_resource_sufficient` detects milk shortage.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_false_milk`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U10: Resource Sufficiency - Insufficient Coffee
- **Goal**: Confirm `is_resource_sufficient` detects coffee shortage.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_false_coffee`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U11: Coin Total Calculation with Animation Tally
- **Goal**: Calculate accurate monetary sum from inserted coins.
- **Code Reference**: [`TestCoffeeMachineUnit.test_process_coins_valid`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U12: Negative Coin Input Validation
- **Goal**: Prompt user retry alert when entering a negative coin count.
- **Code Reference**: [`TestCoffeeMachineUnit.test_process_coins_retry_negative`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U13: Financial Validation - Exact Payment
- **Goal**: Validate exact payment ($2.50 inserted for $2.50 drink).
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_transaction_successful_exact`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U14: Financial Validation - Excess Payment
- **Goal**: Validate excess payment ($3.00 inserted for $2.50 drink) and change calculation.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_transaction_successful_excess`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U15: Financial Validation - Insufficient Payment
- **Goal**: Validate insufficient payment ($0.52 inserted for $2.50 drink).
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_transaction_successful_insufficient`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U16: Resource Deduction
- **Goal**: Ensure ingredients are deducted from current machine resources after making coffee.
- **Code Reference**: [`TestCoffeeMachineUnit.test_make_coffee`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

---

## 3. End-to-End (E2E) Simulation Scenarios

### TC-E01: Successful Latte Purchase Workflow
- **Goal**: Full customer interaction purchasing a Latte with change, brewing animation, report update, and shutdown.
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_successful_latte_purchase`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-E02: Insufficient Money Refund Workflow
- **Goal**: Verify refund warning alert and un-altered inventory when coins are insufficient.
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_insufficient_funds_latte`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-E03: Resource Depletion Refusal Workflow
- **Goal**: Verify machine refuses second order after resources are depleted.
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_insufficient_resource_depletion`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

---

## 4. Automated JSON Report Verification

When executing `python3 task_coffee_machine/test_main.py`, the `JSONTestRunner` generates [`test_results.json`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_results.json):
- Verify ISO-8601 execution timestamp.
- Verify summary pass/fail percentages (`success_rate_percent`, `failure_rate_percent`).
- Verify individual test records include logs, test class names, and execution durations.
