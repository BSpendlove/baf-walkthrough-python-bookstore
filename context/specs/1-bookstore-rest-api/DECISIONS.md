# Decisions: 1-bookstore-rest-api

## Accepted

### Search pagination inconsistency
- **Source:** Gemini
- **Severity:** HIGH
- **Resolution:** Added explicit `skip`, `limit`, and `q` parameters to the API Endpoints table for both list and search endpoints.

### ISBN normalization inconsistency in PUT
- **Source:** Gemini
- **Severity:** MEDIUM
- **Resolution:** Clarified in the ISBN-13 Validation section that the normalized ISBN (hyphens/spaces stripped) is the version stored in the database for both POST and PUT, ensuring the UNIQUE constraint works correctly.

### Search performance on large datasets
- **Source:** Gemini
- **Severity:** MEDIUM
- **Resolution:** Updated Search section to use SQLAlchemy `.ilike()` for correct case-insensitive matching. Added a note that FTS5 should replace LIKE for large datasets.

### Missing validation for `price` and `published_year`
- **Source:** Gemini
- **Severity:** MEDIUM
- **Resolution:** Updated the File Plan entry for `app/schemas.py` to include Pydantic `Field` constraints: `price=Field(gt=0)` and `published_year=Field(ge=1000, le=2100)`.

### Updated At timestamp logic
- **Source:** Gemini
- **Severity:** LOW
- **Resolution:** Updated Data Model table to note that `updated_at` must be explicitly set in application code on update, since SQLite does not support `onupdate` triggers natively via SQLAlchemy.

### ISBN-13 Check Digit Algorithm weights
- **Source:** Gemini
- **Severity:** LOW
- **Resolution:** Clarified the algorithm: weights (1, 3, 1, 3, ...) apply to the first 12 digits, and the 13th digit is the check digit validated via `(10 - (sum % 10)) % 10`.

## Rejected

*(none)*
