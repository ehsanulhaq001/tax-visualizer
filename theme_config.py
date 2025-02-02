# theme_config.py

"""
Stores theme-specific configuration for the tax_visualizer_Plotly script.
Add or customize themes here.
"""

THEMES = {
    "white": {
        "template": "plotly_white",
        "xaxis_linecolor": "black",
        "xaxis_gridcolor": "lightgrey",
        "yaxis_linecolor": "black",
        "yaxis_gridcolor": "lightgrey",
        "yaxis2_linecolor": "black",
        "legend_bgcolor": "rgba(255,255,255,0.6)",
        "legend_bordercolor": "gray",
    },
    "dark": {
        "template": "plotly_dark",
        "xaxis_linecolor": "white",
        "xaxis_gridcolor": "rgba(255,255,255,0.2)",
        "yaxis_linecolor": "white",
        "yaxis_gridcolor": "rgba(255,255,255,0.2)",
        "yaxis2_linecolor": "white",
        "legend_bgcolor": "rgba(0,0,0,0.2)",
        "legend_bordercolor": "white",
    },
}
