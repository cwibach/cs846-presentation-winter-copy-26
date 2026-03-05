"""
Backend API for user display and lookup, used by the dashboard service.

Rewritten with FastAPI + SQLite.
Runs on port 5000.
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import database

app = FastAPI(title="User Helpers API", version="1.0.0")


# ── Pydantic models ──────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str


class UserDisplayOut(BaseModel):
    name: str
    email: str


class HeaderOut(BaseModel):
    display: str


class LookupOut(BaseModel):
    user_id: Optional[int] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/users/{user_id}/display", response_model=UserDisplayOut)
def get_user_display(user_id: int):
    """
    Return name and email for the given user_id.
    """
    conn = database.get_db_connection()
    row = conn.execute(
        "SELECT name, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return UserDisplayOut(name=row["name"], email=row["email"])


@app.get("/users", response_model=list[UserOut])
def get_user_list(role: Optional[str] = Query(default=None)):
    """
    Fetch list of users. Optional role filter (e.g. admin, support).
    """
    conn = database.get_db_connection()

    if role:
        rows = conn.execute(
            "SELECT id, name, email, role FROM users WHERE role = ?", (role,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, email, role FROM users"
        ).fetchall()

    conn.close()

    return [
        UserOut(id=r["id"], name=r["name"], email=r["email"], role=r["role"])
        for r in rows
    ]


@app.get("/users/{user_id}/header", response_model=HeaderOut)
def format_user_for_header(user_id: int):
    """
    Return a short display string for the dashboard header, e.g.:
      - "Jane Doe"
      - "Jane Doe (admin)"
    Single DB query – no redundant calls.
    """
    conn = database.get_db_connection()
    row = conn.execute(
        "SELECT name, role FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    name = row["name"]
    role = row["role"]

    if role and role != "user":
        return HeaderOut(display=f"{name} ({role})")

    return HeaderOut(display=name)


@app.get("/users/lookup", response_model=LookupOut)
def lookup_by_email(email: str = Query(...)):
    """
    Find user id for a given email.
    Used by the internal support tool (backend-only).
    """
    conn = database.get_db_connection()
    row = conn.execute(
        "SELECT id FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if not row:
        return LookupOut(user_id=None)

    return LookupOut(user_id=row["id"])


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("user_helpers:app", host="0.0.0.0", port=5000, reload=True)