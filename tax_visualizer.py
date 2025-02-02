import plotly.graph_objects as go
import numpy as np
import sys

from main import calculate_tax, load_tax_slab
from theme_config import THEMES

# Define a custom color palette so that Tax and Tax(%) for the same slab share the same color
colors = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
]


def get_tax_data(incomes: np.ndarray, tax_slabs) -> tuple[np.ndarray, np.ndarray]:
    """Compute raw tax and tax percentage arrays (vectorized) for a given set of incomes."""
    raw_tax = np.array([calculate_tax(inc, tax_slabs) for inc in incomes], dtype=float)
    tax_pct = (
        np.divide(raw_tax, incomes, out=np.zeros_like(raw_tax), where=incomes != 0)
        * 100
    )
    return raw_tax, tax_pct


def plot_tax_vs_income(tax_slab_files, limit=2500000, theme="white"):
    """
    Compare Income vs Tax (raw) on the left axis and Tax (%) on the right axis using Plotly, with matching colors.
    Theme can be chosen from theme_config.py (e.g., 'white' or 'dark').

    This version uses a helper function and vectorized NumPy operations
    to make the code more concise and efficient.
    """
    # Pull in the chosen theme's config or default to 'white' if not found
    theme_config = THEMES.get(theme, THEMES["white"])

    # Define income range as a NumPy array
    incomes = np.arange(0, limit, 50000)

    # Prepare containers for final traces
    raw_tax_traces = []
    tax_pct_traces = []

    for i, tax_slab_file in enumerate(tax_slab_files):
        tax_slabs = load_tax_slab(tax_slab_file)
        raw_tax_vals, tax_pct_vals = get_tax_data(incomes, tax_slabs)

        # Choose a color for this slab
        color = colors[i % len(colors)]

        # Raw tax trace
        raw_tax_trace = go.Scatter(
            x=incomes,
            y=raw_tax_vals,
            mode="lines",
            name=f"Tax (INR) - {tax_slab_file}",
            line=dict(width=3, color=color),
            hovertemplate=("<b>Income</b>: ₹%{x:,.0f}<br><b>Tax</b>: ₹%{y:,.0f}"),
        )
        raw_tax_traces.append(raw_tax_trace)

        # Tax percentage trace
        tax_pct_trace = go.Scatter(
            x=incomes,
            y=tax_pct_vals,
            mode="lines",
            name=f"Tax (%) - {tax_slab_file}",
            line=dict(width=3, dash="dash", color=color),
            yaxis="y2",
            hovertemplate=("<b>Income</b>: ₹%{x:,.0f}<br><b>Tax %</b>: %{y:.1f}%"),
        )
        tax_pct_traces.append(tax_pct_trace)

    # Layout
    layout = go.Layout(
        template=theme_config["template"],
        title={
            "text": "Comparison of Income vs Tax (INR) and Tax (%)",
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis=dict(
            title="Total Income (INR)",
            tickprefix="₹",
            tickformat=".,0f",
            showline=True,
            linewidth=1,
            linecolor=theme_config["xaxis_linecolor"],
            gridcolor=theme_config["xaxis_gridcolor"],
        ),
        yaxis=dict(
            title="Tax Amount (INR)",
            side="left",
            showgrid=True,
            gridcolor=theme_config["yaxis_gridcolor"],
            tickprefix="₹",
            tickformat=".,0f",
            showline=True,
            linewidth=1,
            linecolor=theme_config["yaxis_linecolor"],
        ),
        yaxis2=dict(
            title="Tax as % of Income",
            side="right",
            overlaying="y",
            showgrid=False,
            tickformat=".1f",
            showline=True,
            linewidth=1,
            linecolor=theme_config["yaxis2_linecolor"],
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            y=1.02,
            xanchor="center",
            yanchor="bottom",
            bgcolor=theme_config["legend_bgcolor"],
            bordercolor=theme_config["legend_bordercolor"],
            borderwidth=1,
        ),
        margin=dict(l=60, r=60, b=60, t=100),
    )

    fig = go.Figure(data=raw_tax_traces + tax_pct_traces, layout=layout)
    fig.show()


if __name__ == "__main__":
    # usage: python tax_visualizer.py <tax_slab_file> ... [--theme=dark]
    theme = "white"  # default theme
    limit = 2500000  # default limit
    tax_slab_files = []

    for arg in sys.argv[1:]:
        if arg.startswith("--theme="):
            theme = arg.split("=")[1]
        elif arg.startswith("--limit="):
            limit = int(arg.split("=")[1])
        else:
            tax_slab_files.append(arg)

    if len(tax_slab_files) < 1:
        print(
            "Usage: python tax_visualizer.py <tax_slab_file1> [<tax_slab_file2> ...] [--theme=<white|dark>]"
        )
        print(
            "Example: python tax_visualizer.py tax_slab_2024 tax_slab_2025 --theme=dark"
        )
        sys.exit(1)

    plot_tax_vs_income(tax_slab_files, limit=limit, theme=theme)
