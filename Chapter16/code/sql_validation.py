from __future__ import annotations

import re

WRITE_KEYWORDS = {"insert", "update", "delete", "drop", "alter", "create", "merge", "truncate"}


def validate_read_only_sql(sql: str, allowed_tables: set[str], prohibited_columns: set[str] | None = None) -> dict:
    text = sql.strip().lower()
    tokens = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text))
    prohibited_columns = {c.lower() for c in (prohibited_columns or set())}

    if not text.startswith("select"):
        return {"validated": False, "reason": "not_select"}
    if tokens & WRITE_KEYWORDS:
        return {"validated": False, "reason": "write_keyword_detected"}
    if prohibited_columns & tokens:
        return {"validated": False, "reason": "prohibited_column_detected"}

    mentioned_tables = set(re.findall(r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)|\bjoin\s+([a-zA-Z_][a-zA-Z0-9_]*)", text))
    mentioned_tables = {a or b for a, b in mentioned_tables}
    allowed = {t.lower() for t in allowed_tables}
    if not mentioned_tables.issubset(allowed):
        return {"validated": False, "reason": "unapproved_table", "tables": sorted(mentioned_tables - allowed)}

    return {"validated": True, "read_only": True, "allowed_tables": True}
