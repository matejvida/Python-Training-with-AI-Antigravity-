# Product Requirements Document (PRD): Coffee Machine Program

## 1. Overview & Objective
The Coffee Machine Program is a command-line interface (CLI) application that simulates an automated coffee vending machine. It manages internal resources (water, milk, coffee), handles user transactions via coin inputs, dispenses coffee drinks, calculates change, and keeps track of accumulated monetary profit.

---

## 2. Target Users
- **Customers**: Select drinks, insert coins, receive drinks and change.
- **Maintainers**: Inspect internal machine resources via secret reports and shut down the machine for maintenance.

---

## 3. Functional Requirements

### FR-1: User Prompt & Navigation Loop
- The machine prompts: `"What would you like? (espresso/latte/cappuccino): "`
- Actions repeat continuously after every operation (dispensing a drink, displaying a report, handling invalid input) until turned off.

### FR-2: Maintainer Control - Turn Off
- When input is `"off"`, the machine immediately terminates execution.

### FR-3: Maintainer Control - Print Report
- When input is `"report"`, print current resource levels and accumulated profit in the exact format:
  ```text
  Water: 100ml
  Milk: 50ml
  Coffee: 76g
  Money: $2.5
  ```

### FR-4: Resource Management & Availability Check
- **Initial Resources**:
  - Water: `300ml`
  - Milk: `200ml`
  - Coffee: `100g`
  - Money (Profit): `$0.0`
- **Drink Specifications**:
  - **Espresso**: Water `50ml`, Milk `0ml`, Coffee `18g`, Cost `$1.50`
  - **Latte**: Water `200ml`, Milk `150ml`, Coffee `24g`, Cost `$2.50`
  - **Cappuccino**: Water `250ml`, Milk `100ml`, Coffee `24g`, Cost `$3.00`
- **Sufficiency Check**: Before asking for coins, verify whether enough water, milk, and coffee exist for the chosen drink.
  - If resource is insufficient, print: `"Sorry there is not enough <resource>."` (e.g., `"Sorry there is not enough water."`) and return to the main prompt without deducting resources or requesting coins.

### FR-5: Coin Processing
- Prompt the user to enter coin counts:
  - Quarters (`$0.25`)
  - Dimes (`$0.10`)
  - Nickels (`$0.05`)
  - Pennies (`$0.01`)
- Calculate total inserted value:
  $$\text{Total} = (0.25 \times Q) + (0.10 \times D) + (0.05 \times N) + (0.01 \times P)$$

### FR-6: Financial Transaction Validation & Change
- Compare monetary value inserted against drink cost:
  - **Insufficient Funds**: Print `"Sorry that's not enough money. Money refunded."` (no resources deducted, money not added to machine profit).
  - **Exact Funds**: Add drink cost to machine profit, deduct ingredients, dispense drink.
  - **Excess Funds**: Calculate change $\text{Change} = \text{Inserted} - \text{Cost}$, rounded to 2 decimal places. Print `"Here is $<change> dollars in change."`, add drink cost to machine profit, deduct ingredients, dispense drink.

### FR-7: Drink Preparation & Resource Deduction
- Deduct recipe ingredients from current resources.
- Output: `"Here is your <drink>. Enjoy!"` (e.g., `"Here is your latte. Enjoy!"`).

---

## 4. Edge Cases & Error Handling
- **Depleted Resources**: Handle cases where multiple resources are missing by reporting the first missing resource.
- **Negative / Non-numeric Coin Input**: Treat invalid coin input gracefully (convert invalid entries to 0 or raise clear prompt retry).
- **Unknown Input**: Ignore unrecognized prompt options or notify user and re-prompt.

---

## 5. Revision History
- **v1.0 (2026-08-23)**: Initial PRD created based on course requirements.
