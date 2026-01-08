from datetime import datetime, timezone
from typing import Dict, List

import plotly.graph_objects as go

def _agg_by_category(records: List[Dict], typ: str) -> Dict[str, float]:
    data: Dict[str, float] = {}
    for r in records:
        t = (r.get("type") or "").lower()
        amt = float(r.get("amount") or 0)
        is_income = (t == "income") or (amt > 0)
        if typ == "expense" and is_income:
            continue
        if typ == "income" and not is_income:
            continue
        cat = str(r.get("category") or "Other").strip() or "Other"
        data[cat] = data.get(cat, 0.0) + abs(amt)
    return dict(sorted(data.items(), key=lambda x: (-x[1], x[0].lower())))

def build_plotly_html(records: List[Dict], title_prefix: str = "") -> str:
    exp = _agg_by_category(records, "expense")
    inc = _agg_by_category(records, "income")

    figs = []

    if exp:
        fig1 = go.Figure(data=[go.Bar(x=list(exp.keys()), y=list(exp.values()))])
        fig1.update_layout(title=f"{title_prefix}Expenses by Category", xaxis_title="Category", yaxis_title="Amount")
        fig2 = go.Figure(data=[go.Pie(labels=list(exp.keys()), values=list(exp.values()))])
        fig2.update_layout(title=f"{title_prefix}Expenses Share")
        figs.append(fig1)
        figs.append(fig2)

    if inc:
        fig3 = go.Figure(data=[go.Bar(x=list(inc.keys()), y=list(inc.values()))])
        fig3.update_layout(title=f"{title_prefix}Income by Category", xaxis_title="Category", yaxis_title="Amount")
        fig4 = go.Figure(data=[go.Pie(labels=list(inc.keys()), values=list(inc.values()))])
        fig4.update_layout(title=f"{title_prefix}Income Share")
        figs.append(fig3)
        figs.append(fig4)

    generated = []
    for i, fig in enumerate(figs):
        generated.append(fig.to_html(full_html=False, include_plotlyjs="cdn" if i == 0 else False))

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    body = "\n<hr/>\n".join(generated) if generated else "<p>No data</p>"
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>Charts</title>
</head>
<body>
<h2>{title_prefix}Charts ({ts})</h2>
{body}
</body>
</html>"""
