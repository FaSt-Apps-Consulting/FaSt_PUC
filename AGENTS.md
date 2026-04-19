# Agent Guide: FaSt_PUC

## Development Commands
- **Test:** `uv run pytest` (uses `pytest`)
- **Lint:** `uv run ruff check .`
- **Format:** `uv run ruff format .`
- **Build:** `uv build`
- **Environment:** Project uses `uv` for dependency management.

## Core Architecture
- **Entrypoint:** `fast_puc.puc` (aliased in `fast_puc/__init__.py`).
- **Logic:** Main SI conversion logic is in `fast_puc/fast_puc.py`.
- **SI Prefixes:** Defined in `SI_PREFIXES` constant as `(threshold, multiplier, symbol)`.

## High-Signal Context
- **Dynamic Precision:** The `precision` argument to `puc()` can be a NumPy array. If so, precision is automatically calculated based on the minimum non-zero difference between array elements.
- **Unit Modifiers:**
    - Space (` `) or underscore (`_`) in the `unit` string automatically becomes the separator.
    - Exclamation mark (`!`) in the `unit` string enables `filecompatible` mode.
- **Special Units:** `dB` and `%` have hardcoded specialized formatting logic.
- **Filename Safety:** `filecompatible=True` replaces `µ -> u`, `. -> p`, `/ -> p`, and ` -> _`.
- **Rounding Quirk:** Uses `np.round`, which follows "round half to even" (e.g., `np.round(2.5)` is `2.0`).
- **Precision 4/5 Special Case:** If `int(precision)` is 4 or 5, the exponent is adjusted by -3 (e.g., prefers `1032.1 nm` over `1.0321 µm`).
- **Input Types:** While `puc()` accepts NumPy arrays for `value`, it currently formats only the *first* element of the array into a single string.
- **Scientific Notation:** The retry logic for increasing precision is triggered for any scientific notation (both `e+` and `e-`).

## Verification Checklist
- [ ] Run `uv run ruff check .` to ensure no linting regressions.
- [ ] Run `uv run pytest` to verify unit conversion edge cases.
