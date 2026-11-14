# Copilot instructions for tdd-ostoskori

## Project overview
This repository is a small Python TDD exercise for a shopping cart domain. The implementation is intentionally compact and centered on a few classes under `src/`:

- `src/tuote.py`: defines `Tuote`, a product value object with a name and a price.
- `src/ostos.py`: defines `Ostos`, a line-item record that keeps track of a product and its quantity.
- `src/ostoskori.py`: defines `Ostoskori`, the cart API that should support adding/removing products and calculating totals.
- `src/tests/ostoskori_test.py`: the existing regression tests for basket behavior, using `unittest.TestCase`.

The project is structured as a learning exercise: behavior is specified in tests first, and the implementation is expected to evolve around the small domain model instead of a larger app architecture.

## Build, test, and validation commands
The project targets Python 3.14 (`.python-version`), and tests are executed with `uv run pytest` in this repository.

Install dependencies and run the full suite:

```bash
uv run pytest -q
```

Run a single test file:

```bash
uv run pytest src/tests/ostoskori_test.py -q
```

Run one specific test:

```bash
uv run pytest src/tests/ostoskori_test.py::TestOstoskori::test_ostoskorin_hinta_ja_tavaroiden_maara_alussa -q
```

There is no linting, formatting, or build tool configured in the repository beyond pytest.

## High-level architecture
The application is deliberately simple and domain-driven:

- `Tuote` represents a product with a name and price and exposes read-only accessors (`nimi()`, `hinta()`).
- `Ostos` represents one product instance in a cart, including quantity and total line value (`lukumaara()`, `hinta()`).
- `Ostoskori` is the aggregate/root object that should keep track of cart contents and compute the total price.
- Tests validate the public behavior of the cart rather than internal implementation details.

This codebase does not have a web layer, service layer, or database; the important “big picture” is the shopping-cart domain model and its test expectations.

## Key conventions
- Use the existing Finnish domain vocabulary rather than introducing English names for the core model (`Tuote`, `Ostos`, `Ostoskori`, `lisaa_tuote`, `poista_tuote`, `tyhjenna`, `ostokset`, `hinta`).
- Keep the project small and procedural/object-oriented: the codebase favors straightforward classes and simple stateful methods over abstraction layers.
- Tests use `unittest` style assertions (`self.assertEqual(...)`) rather than pytest-specific features.
- Preserve the public method names already used by the tests and by the domain model so the TDD flow remains consistent.
- Keep changes in the `src/` tree aligned with the existing domain model; avoid introducing a different project structure unless the task clearly requires it.
- `src/ostos.py` and `src/tuote.py` are part of the fixed domain model and must not be changed.
- Tests should not be edited unless the user explicitly asks for test changes.
- Implement the absolutely minimal code needed to make the current tests pass; do not add speculative features, refactors, or extra abstractions.
