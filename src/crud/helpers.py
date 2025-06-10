import re

from sqlalchemy.exc import IntegrityError


def find_unique_constraint_violator(error: IntegrityError):
    """Extract field name from unique violation error."""
    if not hasattr(error, 'orig'):
        return None

    error_msg = str(error.orig)

    # Pattern for PostgreSQL DETAIL message
    detail_pattern = r'DETAIL:\s+Key\s+\(([^)]+)\)\s*=\s*\([^)]+\)\s+already exists\.'
    detail_match = re.search(detail_pattern, error_msg, re.IGNORECASE)

    if detail_match:
        return detail_match.group(1)

    return None
