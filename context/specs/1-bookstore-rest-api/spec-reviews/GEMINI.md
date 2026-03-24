# Spec Review: 1-bookstore-rest-api

**Agent:** Gemini
**Date:** 2026-03-24

## Summary
The implementation spec for the Bookstore REST API is well-structured and covers the core requirements. It leverages FastAPI and SQLAlchemy effectively. However, there are some inconsistencies in the search endpoint's pagination and potential race conditions/performance issues with the proposed ISBN validation and search implementation that should be addressed.

## Findings

### Search pagination inconsistency
- **Severity:** HIGH
- **Description:** The "API Endpoints" table describes `GET /books/search?q=` but does not explicitly list `skip` and `limit` as parameters, whereas the "Search" section mentions it "Returns paginated results using the same skip/limit parameters." Furthermore, the "API Endpoints" table lists `GET /books` as paginated but doesn't show the parameters there either.
- **Suggested Resolution:** Update the "API Endpoints" table to explicitly include `skip` and `limit` query parameters for both the list and search endpoints to ensure consistent implementation.

### ISBN normalization inconsistency in PUT
- **Severity:** MEDIUM
- **Description:** The "ISBN-13 Validation" section mentions normalization (stripping hyphens/spaces) happens on `POST` and `PUT`. However, if the ISBN is modified during a `PUT` request, the spec doesn't explicitly state if the normalized version should be stored or if the validation only checks the format.
- **Suggested Resolution:** Clarify that the ISBN must be normalized *before* being stored in the database for both `POST` and `PUT` operations to ensure data consistency and that the `UNIQUE` constraint works correctly against different formats of the same ISBN.

### Search performance on large datasets
- **Severity:** MEDIUM
- **Description:** The spec proposes using a case-insensitive `LIKE` search across `title` and `author`. While sufficient for a prototype, `LIKE '%query%'` prevents the use of standard database indexes in SQLite.
- **Suggested Resolution:** For a production-ready spec, consider mentioning that as the dataset grows, this approach may need to be replaced with Full Text Search (FTS) in SQLite. For now, ensure the implementation at least uses SQLAlchemy's `.ilike()` or similar to handle case-insensitivity correctly across different database backends if they were to change.

### Missing validation for `price` and `published_year`
- **Severity:** MEDIUM
- **Description:** The data model specifies `price > 0` and `published_year` as an integer. However, the "ISBN-13 Validation" is the only custom validation mentioned. Standard Pydantic validation handles types, but range validation (e.g., price cannot be negative, year should be realistic) isn't explicitly detailed in the `schemas.py` plan.
- **Suggested Resolution:** Explicitly state in the "Schemas" section that `BookCreate` and `BookUpdate` should include Pydantic `Field` constraints for `price > 0` and `published_year` (e.g., between 1000 and 2100).

### Updated At timestamp logic
- **Severity:** LOW
- **Description:** The spec mentions `updated_at` has `onupdate=now`. In some SQLAlchemy configurations with SQLite, this requires explicit handling or a trigger if not managed by the application layer.
- **Suggested Resolution:** Ensure the implementation in `models.py` uses a mechanism that works with SQLite (like a default value and manual update in the route, or a specific SQLAlchemy `datetime.utcnow` default).

### ISBN-13 Check Digit Algorithm weights
- **Severity:** LOW
- **Description:** The spec correctly identifies alternating weights of 1 and 3, but it's worth noting the starting weight to avoid off-by-one implementation errors.
- **Suggested Resolution:** Clarify that the weights (1, 3, 1, 3, ...) are applied to the first 12 digits, and the 13th digit is the check digit.
