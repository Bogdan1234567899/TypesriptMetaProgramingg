from statistics import median
from typing import Dict, List, Tuple

def _split_amounts(records: List[Dict]) -> Tuple[List[float], List[float]]:
    incomes: List[float] = []
    expenses: List[float] = []
    for r in records:
        amt = float(r.get("amount") or 0)
        t = (r.get("type") or "").lower()
        is_income = (t == "income") or (amt > 0)
        if is_income:
            incomes.append(abs(amt))
        else:
            expenses.append(abs(amt))
    return incomes, expenses

def _summary(values: List[float]) -> Dict[str, float]:
    if not values:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "median": 0.0}
    s = float(sum(values))
    c = int(len(values))
    return {"count": c, "sum": s, "mean": s / c, "median": float(median(values))}

def build_stats(records: List[Dict]) -> Dict[str, Dict[str, float]]:
    incomes, expenses = _split_amounts(records)
    inc = _summary(incomes)
    exp = _summary(expenses)
    inc_sum = float(inc["sum"])
    exp_sum = float(exp["sum"])
    return {"income": inc, "expense": exp, "net": {"sum": inc_sum - exp_sum}}
