from z3 import *

# Contract Constants
MAX_INT = 2**256 - 1

# Contract State
owner = String('owner')  # owner of the contract
caller = String('caller')  # who is calling the function (msg.sender)

# Tokens and Routers
token1 = String('token1')
token2 = String('token2')
router1 = String('router1')
router2 = String('router2')

# Amount and Balances
amount = Int('amount')
amountReceived1 = Int('amountReceived1')
amountReceived2 = Int('amountReceived2')

# Gas Variables
gasOnStart = Int('gasOnStart')
gasLeft = Int('gasLeft')
gasSpent = gasOnStart - gasLeft

# ERC20 Balances and Allowances (functions - they act like mappings)
balances = Function('balances', StringSort(), StringSort(), IntSort())  # balances[token][account]
allowances = Function('allowances', StringSort(), StringSort(), StringSort(), IntSort())  # allowances[token][owner][spender]

# Initial Owner for invariant check
initial_owner = String('initial_owner')

# Z3 Solver
s = Solver()

# Initialization - Owner is set at deployment
s.add(owner == initial_owner)

# --- Ownership Modifier (onlyOwner) ---
onlyOwner = (caller == owner)

# --- Approvals ---
# Allowance check for token1 on router1
allowance1_ok = Or(
    allowances(token1, StringVal("contract"), router1) >= amount,
    allowances(token1, StringVal("contract"), router1) == MAX_INT  # approve infinite if needed
)

# Allowance check for token2 on router2 (needs to cover double received amount for safety)
allowance2_ok = Or(
    allowances(token2, StringVal("contract"), router2) >= amountReceived1 * 2,
    allowances(token2, StringVal("contract"), router2) == MAX_INT
)

# --- Swaps ---
# Abstract swaps - we don't model actual pool math, just symbolic return amounts
amountReceived1 = Int('swap_amount1')
amountReceived2 = Int('swap_amount2')

# --- Gas Handling ---
gasConstraint = (gasSpent == gasOnStart - gasLeft)

# --- Profitability Constraint (Key Check) ---
profitConstraint = (amountReceived2 - gasSpent > amount)

# --- Safety Invariant: Owner Never Changes After Initialization ---
s.add(owner == initial_owner)

# --- Add All Functional Constraints ---
s.add(allowance1_ok)
s.add(allowance2_ok)
s.add(gasConstraint)
s.add(profitConstraint)

# --- Check Feasibility ---
if s.check() == sat:
    print("✅ Arbitrage is feasible under these conditions!")
    print(s.model())
else:
    print("❌ Arbitrage is NOT feasible under these conditions.")
