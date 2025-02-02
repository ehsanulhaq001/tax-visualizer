# tax_slab_usa.py

TAX_SLABS_IN_DOLLAR = [
    (11000, 0.10),
    (44725, 0.12),
    (95375, 0.22),
    (182100, 0.24),
    (231250, 0.32),
    (578125, 0.35),
    (100000000, 0.37),
]

puchase_parity_multiplier = 23

TAX_SLABS = [
    (limit * puchase_parity_multiplier, rate) for limit, rate in TAX_SLABS_IN_DOLLAR
]
