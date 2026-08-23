# Test Case Specification: Coffee Machine Program

This document details all test scenarios designed to validate the functional requirements and edge cases of the Coffee Machine program. Each test case is directly mapped to its implementation in [`test_main.py`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py).

---

## 1. Unit Test Scenarios

### TC-U01: Report Formatting
- **Goal**: Verify that resource inventory and profit values are formatted correctly.
- **Inputs**: Resources = `Water: 100, Milk: 50, Coffee: 76`, Profit = `$2.5`.
- **Expected Outcome**: Output matches the exact 4 lines specified in requirement FR-3.
- **Code Reference**: [`TestCoffeeMachineUnit.test_print_report`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U02: Resource Sufficiency - All Available
- **Goal**: Confirm `is_resource_sufficient` returns `(True, None)` when resources exceed recipe needs.
- **Inputs**: Latte recipe (200ml water, 150ml milk, 24g coffee) vs. Initial resources (300ml water, 200ml milk, 100g coffee).
- **Expected Outcome**: `(True, None)`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_true`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U03: Resource Sufficiency - Insufficient Water
- **Goal**: Confirm `is_resource_sufficient` detects water shortage.
- **Inputs**: Latte recipe (200ml water) vs. Resources (100ml water).
- **Expected Outcome**: `(False, "water")`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_false_water`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U04: Resource Sufficiency - Insufficient Milk
- **Goal**: Confirm `is_resource_sufficient` detects milk shortage.
- **Inputs**: Cappuccino recipe (100ml milk) vs. Resources (50ml milk).
- **Expected Outcome**: `(False, "milk")`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_false_milk`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U05: Resource Sufficiency - Insufficient Coffee
- **Goal**: Confirm `is_resource_sufficient` detects coffee shortage.
- **Inputs**: Espresso recipe (18g coffee) vs. Resources (10g coffee).
- **Expected Outcome**: `(False, "coffee")`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_resource_sufficient_false_coffee`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U06: Coin Total Calculation
- **Goal**: Calculate accurate total USD value from inserted coins.
- **Inputs**: 1 quarter ($0.25), 2 dimes ($0.20), 1 nickel ($0.05), 2 pennies ($0.02).
- **Expected Outcome**: `$0.52`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_process_coins_valid`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U07: Negative Coin Input Validation
- **Goal**: Prompt user to retry when entering a negative coin count.
- **Inputs**: `-1` quarters followed by `1` quarter, `0` dimes/nickels/pennies.
- **Expected Outcome**: Error warning displayed, retry succeeds with total `$0.25`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_process_coins_retry_negative`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U08: Financial Validation - Exact Payment
- **Goal**: Validate exact payment ($2.50 inserted for $2.50 drink).
- **Expected Outcome**: `(True, 0.0)`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_transaction_successful_exact`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U09: Financial Validation - Excess Payment
- **Goal**: Validate excess payment ($3.00 inserted for $2.50 drink).
- **Expected Outcome**: `(True, 0.50)` change calculated.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_transaction_successful_excess`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U10: Financial Validation - Insufficient Payment
- **Goal**: Validate insufficient payment ($0.52 inserted for $2.50 drink).
- **Expected Outcome**: `(False, 0.0)`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_is_transaction_successful_insufficient`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-U11: Resource Deduction
- **Goal**: Ensure ingredients are deducted from current machine resources after making coffee.
- **Inputs**: Latte recipe (200ml water, 150ml milk, 24g coffee) vs. Resources (300ml water, 200ml milk, 100g coffee).
- **Expected Outcome**: Remaining resources = `100ml water, 50ml milk, 76g coffee`.
- **Code Reference**: [`TestCoffeeMachineUnit.test_make_coffee`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

---

## 2. End-to-End (E2E) Test Scenarios

### TC-E01: Successful Latte Purchase Workflow
- **Goal**: Full customer transaction flow purchasing a Latte.
- **Sequence**:
  1. User selects `"latte"`.
  2. Inserts 10 quarters ($2.50).
  3. Machine dispenses `"Here is your latte. Enjoy!"`.
  4. User triggers `"report"` -> verifies updated inventory (`Water: 100ml, Milk: 50ml, Coffee: 76g, Money: $2.5`).
  5. User inputs `"off"` -> machine terminates cleanly.
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_successful_latte_purchase`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-E02: Insufficient Money Refund Workflow
- **Goal**: Verify refund message and un-altered inventory when coins are insufficient.
- **Sequence**:
  1. User selects `"latte"`.
  2. Inserts $0.52.
  3. Machine prints `"Sorry that's not enough money. Money refunded."`.
  4. `"report"` confirms zero resources deducted and `$0.0` profit.
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_insufficient_funds_latte`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-E03: Resource Depletion Refusal Workflow
- **Goal**: Verify machine refuses second order after resources are depleted.
- **Sequence**:
  1. User orders 1st Cappuccino (uses 250ml water out of 300ml). Successful.
  2. User orders 2nd Cappuccino (requires 250ml, only 50ml left).
  3. Machine prints `"Sorry there is not enough water."` without requesting coins.
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_insufficient_resource_depletion`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)

### TC-E04: Report & Shutdown Workflow
- **Goal**: Verify maintainer actions (`report`, `off`).
- **Code Reference**: [`TestCoffeeMachineE2E.test_e2e_report_and_off`](file:///Users/vida/Documents/Development/PythonUdemy/task_coffee_machine/test_main.py)
