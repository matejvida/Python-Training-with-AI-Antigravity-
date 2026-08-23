# Product Requirements Document (PRD): Retro CLI GUI Coffee Machine Program

## 1. Overview & Objective
The Coffee Machine Program is a retro-styled command-line interface (CLI GUI) application that simulates an automated coffee vending machine. It features ASCII art visuals, step-by-step animations for drink preparation and coin processing, resource management (water, milk, coffee), monetary transaction handling, and maintainer reporting. Additionally, the project includes an automated test reporter exporting structured JSON metrics (`test_results.json`) for downstream web visualization.

---

## 2. Target Users
- **Customers**: View retro ASCII menu, select drinks, insert coins with visual feedback, watch brewing animations, receive drinks and change.
- **Maintainers**: Inspect internal machine resources via secret reports and shut down the machine with a retro animation sequence.
- **Developers / Web Dashboard Integrators**: Consume human-readable `test_results.json` reports to monitor test success ratios and graph execution analytics.

---

## 3. Functional Requirements

### FR-1: User Prompt & Navigation Loop
- Display retro ASCII Coffee Machine logo header at startup and before menu display.
- Present prompt: `"What would you like? (espresso/latte/cappuccino): "`
- Prompt loop repeats continuously after drink completion, report display, or invalid input.

### FR-2: Maintainer Control - Turn Off
- Input `"off"` triggers an animated retro shutdown sequence (`"SHUTTING DOWN...", "SAVING STATE...", "GOODBYE!"`) and ends execution.

### FR-3: Maintainer Control - Print Report
- Input `"report"` displays boxed ASCII resource report:
  ```text
  +--------------------------+
  |  COFFEE MACHINE REPORT   |
  +--------------------------+
  | Water:  100ml            |
  | Milk:   50ml             |
  | Coffee: 76g              |
  | Money:  $2.50            |
  +--------------------------+
  ```

### FR-4: Resource Management & Availability Check
- **Initial Resources**: Water `300ml`, Milk `200ml`, Coffee `100g`, Profit `$0.00`.
- **Recipes**:
  - Espresso: Water 50ml, Milk 0ml, Coffee 18g | Price: $1.50
  - Latte: Water 200ml, Milk 150ml, Coffee 24g | Price: $2.50
  - Cappuccino: Water 250ml, Milk 100ml, Coffee 24g | Price: $3.00
- If resources are insufficient, trigger alert animation: `"⚠️  SORRY: Not enough <resource>!"`.

### FR-5: Coin Processing & Insertion Animation
- Prompt user for Quarters ($0.25), Dimes ($0.10), Nickels ($0.05), Pennies ($0.01).
- Show step-by-step coin insertion tally animation as each coin type is entered.

### FR-6: Financial Transaction Validation & Change
- Compare inserted total against drink cost.
- **Insufficient Funds**: Trigger refund alert animation `"⚠️  SORRY: Not enough money. Refunded: $<amount>"`.
- **Exact / Excess Funds**: Display change alert `"💰  Change: $<amount>"` (rounded to 2 decimal places) and proceed to brewing.

### FR-7: Drink Preparation & Completion Animations
- Display multi-frame brewing animation:
  1. `[1/4] ⚙️  Grinding fresh coffee beans...`
  2. `[2/4] 💧  Heating water to optimal temperature...`
  3. `[3/4] 🥛  Steaming milk (if applicable)...`
  4. `[4/4] ☕  Brewing & dispensing drink...`
  5. Animated progress bar `[████████████████████] 100%`
- Output final ASCII cup: `"HERE IS YOUR <DRINK>! ENJOY! ☕"` and return to prompt loop.

---

## 4. Retro CLI GUI Design Specification
- **Logo Banner**: Top ASCII header rendered on startup and menu display.
- **Boxed Layouts**: Double-line or standard border boxes for menu choices, reports, and warnings.
- **Configurable Animation Delay**: All visual delay loops use `animation_delay` (default `0.1s` for CLI interactive mode; set to `0.0s` during automated test execution for instant performance).

---

## 5. JSON Test Reporting & Console Logging Specification
Automated test suite (`test_main.py`) exports `test_results.json` upon execution.

### JSON Schema Structure (`test_results.json`)
The `test_results.json` file contains a JSON array of historical execution runs:
```json
[
  {
    "execution_id": 1,
    "timestamp": "2026-08-23T10:38:54.935053+00:00",
    "summary": {
      "total_tests": 19,
      "passed": 19,
      "failed": 0,
      "errors": 0,
      "skipped": 0,
      "success_rate_percent": 100.0,
      "failure_rate_percent": 0.0,
      "duration_seconds": 0.0021
    },
    "failed_test_cases": [],
    "test_cases": [
      {
        "id": "test_print_report",
        "name": "test_print_report",
        "class_name": "TestCoffeeMachineUnit",
        "status": "PASS",
        "duration_seconds": 0.001,
        "logs": "[EXEC] Running TestCoffeeMachineUnit.test_print_report... [PASS] (0.001s)"
      }
    ]
  }
]
```

### Live Console Output Format
During `python3 task_coffee_machine/test_main.py` execution:
```text
======================================================================
           COFFEE MACHINE AUTOMATED TEST SUITE EXECUTION
======================================================================
[EXEC] Running TestCoffeeMachineUnit.test_print_report... [PASS] (0.001s)
[EXEC] Running TestCoffeeMachineUnit.test_is_resource_sufficient_true... [PASS] (0.001s)
...
----------------------------------------------------------------------
EXECUTION SUMMARY:
- Timestamp: 2026-08-23T12:00:00Z
- Total Tests: 18 | Passed: 18 | Failed: 0 | Errors: 0
- Success Rate: 100.00% | Failure Rate: 0.00%
- Report Saved: task_coffee_machine/test_results.json
======================================================================
```

---

## 6. Revision History
- **v1.0 (2026-08-23)**: Initial PRD created with core requirements.
- **v2.0 (2026-08-23)**: Expanded with Retro CLI GUI specification, brewing/coin animations, live console test logger, `test_results.json` schema, and root README integration.
