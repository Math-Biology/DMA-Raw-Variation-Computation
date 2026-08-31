# Oscillation Percentage — Formula

## Purpose

Measures the spread of raw percentage variations across markers for each anatomical point, within a single visit. No corrective rules are applied to the input.

---

## Formula

```
δ = max(column) − min_nonzero(column)
```

Where:
- `column` = raw percentage variations for a given anatomical point (`percentage_variation` values grouped by visit and point)
- `max(column)` = maximum value of the series
- `min_nonzero(column)` = strictly positive minimum value (≠ 0) of the series

δ is expressed in **percentage points**. Returns 0 if fewer than two strictly positive values are present.

---

## References

| Source | Row / Section |
|---|---|
| `Elaborazione_v4_c.py` | rows 288–289 |
| TechDoc SR&TS Rev 00.01 | Section Stage 3 — FANE, line 533: *"delta shall be computed as max(column) − min_nonzero(column)"* |
| TechDoc SR&TS Rev 00.01 | Spec FANE Trigger Condition |
