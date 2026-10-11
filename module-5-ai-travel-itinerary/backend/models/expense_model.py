"""
Expense and budget tracking data operations (collection: expenses).
Guarantees ownership validation and precision mathematical budget analytics.
"""

from datetime import datetime, timezone
from models import get_db, to_object_id


def _expenses():
    return get_db()["expenses"]


def ensure_indexes():
    _expenses().create_index([("trip_id", 1), ("user_id", 1), ("date", -1)])


def serialize_expense(exp: dict) -> dict:
    created_at = exp.get("created_at")
    return {
        "id": str(exp["_id"]),
        "trip_id": str(exp["trip_id"]),
        "user_id": str(exp["user_id"]),
        "category": exp.get("category", "miscellaneous"),
        "amount": round(float(exp.get("amount", 0.0)), 2),
        "currency": exp.get("currency", "INR"),
        "date": exp.get("date"),
        "payment_status": exp.get("payment_status", "paid"),  # paid, pending, refunded, cancelled
        "description": exp.get("description", ""),
        "booking_reference": exp.get("booking_reference", ""),
        "created_at": created_at.isoformat() if created_at else None,
    }


def create_expense(user_id: str, trip_id: str, data: dict) -> dict:
    owner, tid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or tid is None:
        raise ValueError("Invalid user_id or trip_id")

    amount = round(float(data.get("amount", 0.0)), 2)
    doc = {
        "trip_id": tid,
        "user_id": owner,
        "category": (data.get("category") or "miscellaneous").lower().strip(),
        "amount": amount,
        "currency": (data.get("currency") or "INR").upper().strip(),
        "date": data.get("date") or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "payment_status": (data.get("payment_status") or "paid").lower().strip(),
        "description": (data.get("description") or "").strip(),
        "booking_reference": (data.get("booking_reference") or "").strip(),
        "created_at": datetime.now(timezone.utc),
    }
    result = _expenses().insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_expense(doc)


def get_expenses_by_trip(user_id: str, trip_id: str) -> list:
    owner, tid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or tid is None:
        return []
    cursor = _expenses().find({"user_id": owner, "trip_id": tid}).sort("date", -1)
    return [serialize_expense(e) for e in cursor]


def get_expense_by_id(user_id: str, expense_id: str):
    owner, eid = to_object_id(user_id), to_object_id(expense_id)
    if owner is None or eid is None:
        return None
    doc = _expenses().find_one({"_id": eid, "user_id": owner})
    return serialize_expense(doc) if doc else None


def update_expense(user_id: str, expense_id: str, data: dict):
    owner, eid = to_object_id(user_id), to_object_id(expense_id)
    if owner is None or eid is None:
        return None

    allowed = {"category", "amount", "currency", "date", "payment_status", "description", "booking_reference"}
    updates = {}
    for k in allowed:
        if k in data:
            if k == "amount":
                updates[k] = round(float(data[k]), 2)
            elif k in ("category", "payment_status"):
                updates[k] = str(data[k]).lower().strip()
            elif k == "currency":
                updates[k] = str(data[k]).upper().strip()
            else:
                updates[k] = str(data[k]).strip()

    if updates:
        updates["updated_at"] = datetime.now(timezone.utc)
        _expenses().update_one({"_id": eid, "user_id": owner}, {"$set": updates})

    return get_expense_by_id(user_id, expense_id)


def delete_expense(user_id: str, expense_id: str) -> bool:
    owner, eid = to_object_id(user_id), to_object_id(expense_id)
    if owner is None or eid is None:
        return False
    return _expenses().delete_one({"_id": eid, "user_id": owner}).deleted_count == 1


def compute_budget_analytics(expenses: list, trip_data: dict) -> dict:
    """
    Computes exact budget analytics from an in-memory list of expenses and trip dict.
    Formulas:
      - remaining_budget = total_budget - actual_paid_expenses
      - budget_used_percentage = (actual_paid_expenses / total_budget) * 100
      - is_over_budget = actual_paid_expenses > total_budget
      - overrun_amount = actual_paid_expenses - total_budget
    """
    total_budget = round(float(trip_data.get("budget") or 0.0), 2)
    estimated_total = round(float(trip_data.get("estimated_total_cost") or total_budget), 2)
    currency = trip_data.get("currency", "INR")

    actual_paid = 0.0
    pending_payments = 0.0
    refunded_amount = 0.0
    cancelled_amount = 0.0

    category_breakdown = {}

    for exp in expenses:
        amt = float(exp.get("amount", 0.0))
        status = str(exp.get("payment_status", "paid")).lower()
        cat = str(exp.get("category", "other")).lower()

        if cat not in category_breakdown:
            category_breakdown[cat] = {"total_paid": 0.0, "percentage_of_budget": 0.0, "count": 0}

        category_breakdown[cat]["count"] += 1

        if status == "paid":
            actual_paid += amt
            category_breakdown[cat]["total_paid"] += amt
        elif status == "pending":
            pending_payments += amt
        elif status == "refunded":
            refunded_amount += amt
        elif status == "cancelled":
            cancelled_amount += amt

    actual_paid = round(actual_paid, 2)
    pending_payments = round(pending_payments, 2)
    refunded_amount = round(refunded_amount, 2)

    # Core mathematical formula required by specifications:
    # remaining_budget = total_budget - actual_paid_expenses
    remaining_budget = round(total_budget - actual_paid, 2)
    if remaining_budget < 0:
        display_remaining = 0.0
    else:
        display_remaining = remaining_budget

    # budget_used_percentage = (actual_paid_expenses / total_budget) * 100
    if total_budget > 0:
        budget_used_percentage = round((actual_paid / total_budget) * 100, 1)
        for cat, data in category_breakdown.items():
            data["percentage_of_budget"] = round((data["total_paid"] / total_budget) * 100, 1)
            data["total_paid"] = round(data["total_paid"], 2)
    else:
        budget_used_percentage = 0.0

    is_overrun = actual_paid > total_budget if total_budget > 0 else False
    overrun_amount = round(actual_paid - total_budget, 2) if is_overrun else 0.0
    potential_remaining = round(display_remaining - pending_payments, 2)

    return {
        "total_budget": total_budget,
        "estimated_total_cost": estimated_total,
        "currency": currency,
        "actual_paid_expenses": actual_paid,
        "remaining_budget": display_remaining,
        "exact_remaining": remaining_budget,
        "budget_used_percentage": budget_used_percentage,
        "pending_payments": pending_payments,
        "pending_commitments": pending_payments,
        "potential_remaining_budget": potential_remaining,
        "refunded_amount": refunded_amount,
        "cancelled_amount": cancelled_amount,
        "is_overrun": is_overrun,
        "is_over_budget": is_overrun,
        "overrun_amount": overrun_amount,
        "category_spending": {k: round(v["total_paid"], 2) for k, v in category_breakdown.items()},
        "category_breakdown": category_breakdown,
        "total_expense_count": len(expenses),
        "expense_count": len(expenses),
    }


def get_trip_budget_analytics(user_id: str, trip_id: str, trip_data: dict) -> dict:
    """
    Computes exact budget analytics for a user trip.
    """
    owner, tid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or tid is None:
        return {}

    expenses = get_expenses_by_trip(user_id, trip_id)
    return compute_budget_analytics(expenses, trip_data)
