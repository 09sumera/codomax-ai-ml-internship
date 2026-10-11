"""Trip data operations (collection: trips). Every query is scoped to the owner."""

from datetime import datetime, timezone
from models import get_db, to_object_id
from services.image_service import get_destination_image


def _trips():
    return get_db()["trips"]


def ensure_indexes():
    _trips().create_index([("user_id", 1), ("created_at", -1)])


def serialize_trip(trip: dict, include_itinerary: bool = True) -> dict:
    created_at = trip.get("created_at")
    destination = trip.get("destination", "")
    image_url = trip.get("image_url") or get_destination_image(destination)
    
    # Calculate overview estimated total cost if available
    itinerary = trip.get("itinerary", {})
    estimated_total = None
    if isinstance(itinerary, dict):
        overview = itinerary.get("overview", {})
        if isinstance(overview, dict):
            cost_obj = overview.get("estimated_total_cost", {})
            if isinstance(cost_obj, dict):
                estimated_total = cost_obj.get("amount")

    data = {
        "id": str(trip["_id"]),
        "user_id": str(trip["user_id"]),
        "title": trip.get("title", ""),
        "destination": destination,
        "origin": trip.get("origin", ""),
        "days": trip.get("days"),
        "travelers": trip.get("travelers", 1),
        "budget": trip.get("budget"),
        "estimated_total_cost": estimated_total or trip.get("budget"),
        "currency": trip.get("currency", "INR"),
        "start_date": trip.get("start_date"),
        "end_date": trip.get("end_date"),
        "interests": trip.get("interests", []),
        "intermediate_destinations": trip.get("intermediate_destinations", []),
        "transport_preference": trip.get("transport_preference", "Any"),
        "accommodation_preference": trip.get("accommodation_preference", "Mid-range"),
        "food_preference": trip.get("food_preference", "Any"),
        "accessibility_requirements": trip.get("accessibility_requirements", "None"),
        "booking_status": trip.get("booking_status", "planned"),
        "image_url": image_url,
        "display_currency": trip.get("display_currency") or trip.get("currency", "INR"),
        "completed_activities": trip.get("completed_activities", []),
        "has_revision_history": bool(trip.get("itinerary_history")),
        "history_count": len(trip.get("itinerary_history", [])),
        "created_at": created_at.isoformat() if created_at else None,
    }
    
    if include_itinerary:
        data["itinerary"] = itinerary
    else:
        # Lightweight summary representation for high-speed dashboard loading
        overview_info = itinerary.get("overview", {}) if isinstance(itinerary, dict) else {}
        data["overview"] = overview_info
        
    return data


def create_trip(user_id: str, trip_data: dict) -> dict:
    """Save a trip for a user and return its serialized form."""
    destination = trip_data.get("destination", "")
    image_url = trip_data.get("image_url") or get_destination_image(destination)

    document = {
        "user_id": to_object_id(user_id),
        "title": trip_data.get("title"),
        "destination": destination,
        "origin": trip_data.get("origin", ""),
        "days": trip_data.get("days"),
        "travelers": trip_data.get("travelers", 1),
        "budget": trip_data.get("budget"),
        "currency": trip_data.get("currency", "INR"),
        "start_date": trip_data.get("start_date"),
        "end_date": trip_data.get("end_date"),
        "interests": trip_data.get("interests", []),
        "intermediate_destinations": trip_data.get("intermediate_destinations", []),
        "transport_preference": trip_data.get("transport_preference", "Any"),
        "accommodation_preference": trip_data.get("accommodation_preference", "Mid-range"),
        "food_preference": trip_data.get("food_preference", "Any"),
        "accessibility_requirements": trip_data.get("accessibility_requirements", "None"),
        "booking_status": trip_data.get("booking_status", "planned"),
        "image_url": image_url,
        "itinerary": trip_data.get("itinerary", {}),
        "created_at": datetime.now(timezone.utc),
    }
    result = _trips().insert_one(document)
    document["_id"] = result.inserted_id
    return serialize_trip(document)


def get_trips_by_user(user_id: str) -> list:
    """Full trip objects including complete itinerary."""
    owner = to_object_id(user_id)
    if owner is None:
        return []
    cursor = _trips().find({"user_id": owner}).sort("created_at", -1)
    return [serialize_trip(trip, include_itinerary=True) for trip in cursor]


def get_trip_summaries_by_user(user_id: str) -> list:
    """Lightweight trip summaries optimized for instant dashboard loading."""
    owner = to_object_id(user_id)
    if owner is None:
        return []
    # Project out the massive days array
    projection = {
        "itinerary.days": 0
    }
    cursor = _trips().find({"user_id": owner}, projection).sort("created_at", -1)
    return [serialize_trip(trip, include_itinerary=False) for trip in cursor]


def get_trip_by_id(user_id: str, trip_id: str):
    """Return the trip only if it belongs to the user; otherwise None."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None:
        return None
    trip = _trips().find_one({"_id": oid, "user_id": owner})
    return serialize_trip(trip, include_itinerary=True) if trip else None


def update_trip(user_id: str, trip_id: str, updates: dict):
    """Update allowed fields of a trip belonging to the user."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None:
        return None
    
    # Filter safe mutable fields
    allowed_fields = {
        "title", "origin", "destination", "budget", "currency", 
        "start_date", "end_date", "travelers", "days", "interests",
        "booking_status", "transport_preference", "accommodation_preference",
        "food_preference", "accessibility_requirements", "image_url",
        "display_currency"
    }
    clean_updates = {k: v for k, v in updates.items() if k in allowed_fields}
    
    # If destination changed, update image_url if not explicitly provided
    if "destination" in clean_updates and "image_url" not in clean_updates:
        clean_updates["image_url"] = get_destination_image(clean_updates["destination"])
        
    if clean_updates:
        clean_updates["updated_at"] = datetime.now(timezone.utc)
        _trips().update_one({"_id": oid, "user_id": owner}, {"$set": clean_updates})
        
    return get_trip_by_id(user_id, trip_id)


def push_itinerary_revision(user_id: str, trip_id: str, new_itinerary: dict, change_reason: str = "Optimization") -> dict | None:
    """Store current itinerary in history for undo capability and apply new itinerary."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None:
        return None
    trip = _trips().find_one({"_id": oid, "user_id": owner})
    if not trip:
        return None
        
    current_itinerary = trip.get("itinerary", {})
    history = trip.get("itinerary_history", [])
    history.append({
        "itinerary": current_itinerary,
        "reason": change_reason,
        "saved_at": datetime.now(timezone.utc).isoformat()
    })
    # Keep up to 10 historical snapshots
    if len(history) > 10:
        history = history[-10:]

    _trips().update_one(
        {"_id": oid, "user_id": owner},
        {
            "$set": {
                "itinerary": new_itinerary,
                "itinerary_history": history,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    return get_trip_by_id(user_id, trip_id)


def undo_itinerary_revision(user_id: str, trip_id: str) -> dict | None:
    """Revert itinerary to the most recent historical snapshot."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None:
        return None
    trip = _trips().find_one({"_id": oid, "user_id": owner})
    if not trip:
        return None
        
    history = trip.get("itinerary_history", [])
    if not history:
        return None
        
    last_revision = history.pop()
    restored_itinerary = last_revision.get("itinerary", {})

    _trips().update_one(
        {"_id": oid, "user_id": owner},
        {
            "$set": {
                "itinerary": restored_itinerary,
                "itinerary_history": history,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    return get_trip_by_id(user_id, trip_id)


def toggle_activity_completion(user_id: str, trip_id: str, activity_name: str, completed: bool = True) -> dict | None:
    """Track completed activities so replanning preserves them."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None or not activity_name:
        return None

    if completed:
        _trips().update_one(
            {"_id": oid, "user_id": owner},
            {
                "$addToSet": {"completed_activities": activity_name},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )
    else:
        _trips().update_one(
            {"_id": oid, "user_id": owner},
            {
                "$pull": {"completed_activities": activity_name},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )
    return get_trip_by_id(user_id, trip_id)


def set_trip_display_currency(user_id: str, trip_id: str, currency_code: str) -> dict | None:
    """Update preferred display currency without altering underlying expense records."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None or not currency_code:
        return None
    _trips().update_one(
        {"_id": oid, "user_id": owner},
        {
            "$set": {
                "display_currency": currency_code.upper().strip(),
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    return get_trip_by_id(user_id, trip_id)


def delete_trip(user_id: str, trip_id: str) -> bool:
    """Delete the trip only if it belongs to the user. Returns True if deleted."""
    owner, oid = to_object_id(user_id), to_object_id(trip_id)
    if owner is None or oid is None:
        return False
    return _trips().delete_one({"_id": oid, "user_id": owner}).deleted_count == 1