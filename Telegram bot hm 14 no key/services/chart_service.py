from io import BytesIO
from typing import Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def build_charts(categories: Dict[str, float], title: str) -> Tuple[BytesIO, BytesIO]:
    data = categories or {}
    if not data:
        return None, None

    cats = list(data.keys())
    vals = [float(data[c]) for c in cats]

    bar_buf = BytesIO()
    plt.figure()
    plt.title(title)
    plt.bar(cats, vals)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(bar_buf, format="png", dpi=150)
    plt.close()
    bar_buf.seek(0)

    pie_buf = BytesIO()
    plt.figure()
    plt.title(title)
    plt.pie(vals, labels=cats, autopct="%1.1f%%")
    plt.tight_layout()
    plt.savefig(pie_buf, format="png", dpi=150)
    plt.close()
    pie_buf.seek(0)

    return bar_buf, pie_buf
