
# Arb Contract Formal Verification


This repository contains a formal verification model for a Solidity Arbitrage contract using Z3 SMT solver.
The `arb_verification.py` script is derived from the logic in the
[`Arb.sol`](https://github.com/achiko/arbSmartcontracts/blob/main/contracts/Arb.sol)
Solidity contract.

## Repository Overview

This project provides a minimal demonstration of how symbolic execution can be used to verify an arbitrage contract. The model defines token balances, allowances and profitability constraints in Python and leverages the Z3 solver to prove whether arbitrage is possible under generic conditions.

## Files

- `arb_verification.py`: Python script that models the arbitrage contract logic and verifies key safety and profitability properties.
- `requirements.txt`: Python dependencies.

## Setup

Install requirements:
```
pip install -r requirements.txt
```

## Run Verification

```
python arb_verification.py
```

If the contract logic is sound, the script will output:
```
✅ Arbitrage is feasible under these conditions!
```

Otherwise:
```
❌ Arbitrage is NOT feasible under these conditions.
```

## Key Properties Verified

- Ownership is immutable after deployment.
- Arbitrage only proceeds if token approvals are sufficient.
- Arbitrage guarantees profitability (including gas costs).
- Symbolic swap amounts are used, not actual Uniswap math.
