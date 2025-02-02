import numpy as np
import pytest
import plotly.graph_objects as go

import main
import tax_visualizer


# ---------------------------
# Test get_tax_data() function using a flat 10% tax (mock)
# ---------------------------
def mock_calculate_tax(income, slabs):
    # Return a flat 10% tax for testing purposes
    return income * 0.1


@pytest.mark.parametrize("income", [0, 50_000, 100_000, 200_000])
def test_get_tax_data_single(income, monkeypatch):
    # Monkey-patch calculate_tax in tax_visualizer (the already-imported symbol)
    monkeypatch.setattr(tax_visualizer, "calculate_tax", mock_calculate_tax)

    incomes = np.array([income])
    # Dummy tax slabs (won't matter for flat 10% tax)
    slabs = [(250000, 0.1), (500000, 0.15)]

    raw_tax, tax_pct = tax_visualizer.get_tax_data(incomes, slabs)

    # Expect 10% tax
    expected_raw = income * 0.1
    expected_pct = (expected_raw / income) * 100 if income != 0 else 0

    np.testing.assert_allclose(raw_tax, np.array([expected_raw]))
    np.testing.assert_allclose(tax_pct, np.array([expected_pct]))


# ---------------------------
# Test get_tax_data() function using a flat 30% tax (lambda)
# ---------------------------
def test_get_tax_data_multiple(monkeypatch):
    # Use a lambda to return a flat 30% tax for testing
    monkeypatch.setattr(tax_visualizer, "calculate_tax", lambda inc, slabs: inc * 0.3)

    incomes = np.array([100000, 200000, 300000])
    slabs = [(250000, 0.1), (500000, 0.15)]

    raw_tax, tax_pct = tax_visualizer.get_tax_data(incomes, slabs)

    expected_raw = incomes * 0.3
    expected_pct = (expected_raw / incomes) * 100  # Should be constant 30%

    np.testing.assert_allclose(raw_tax, expected_raw)
    np.testing.assert_allclose(tax_pct, expected_pct)


# ---------------------------
# Test calculate_tax() function in main.py using known slabs
# ---------------------------
def test_calculate_tax():
    # For income = 400000 with slabs = [(250000, 0.1), (500000, 0.2)]
    # Calculation:
    #   - For first 250000: 250000 * 0.1 = 25000
    #   - Remaining 150000 taxed at 0.2: 150000 * 0.2 = 30000
    # Total expected = 25000 + 30000 = 55000.
    slabs = [(250000, 0.1), (500000, 0.2)]
    income = 400000
    expected_tax = 55000
    result_tax = main.calculate_tax(income, slabs)
    assert result_tax == pytest.approx(expected_tax)


# ---------------------------
# Test the plotting function in tax_visualizer.py
# ---------------------------
def test_plot_tax_vs_income(monkeypatch):
    captured = {}

    # Monkey-patch go.Figure.show to capture the figure instead of displaying it.
    def fake_show(self):
        captured["figure"] = self

    monkeypatch.setattr(go.Figure, "show", fake_show)

    # Use dummy tax slab file names.
    dummy_files = ["tax_slab_2024", "tax_slab_2025"]

    # Monkey-patch load_tax_slab to return predictable slabs.
    def fake_load_tax_slab(filename):
        return [(250000, 0.1), (500000, 0.2)]

    monkeypatch.setattr(main, "load_tax_slab", fake_load_tax_slab)

    # Monkey-patch calculate_tax to return a flat 5% tax.
    monkeypatch.setattr(tax_visualizer, "calculate_tax", lambda inc, slabs: inc * 0.05)

    # Call the plotting function. This should invoke our fake go.Figure.show.
    tax_visualizer.plot_tax_vs_income(dummy_files, theme="white")

    # Verify that a figure was captured.
    assert "figure" in captured
    fig = captured["figure"]

    # We expect 2 traces per tax slab file (one for raw tax and one for tax percentage).
    assert len(fig.data) == 4

    # Check that the title text contains the expected substring.
    assert "Comparison of Income vs Tax" in fig.layout.title.text

    # Verify that the x-axis has the correct tick prefix.
    assert fig.layout.xaxis.tickprefix == "₹"
