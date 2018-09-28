def is_params_passed(json: dict, required: list) -> bool:
    return all([json.get(r) for r in required])


def fill_navi_address_data(**kwargs):
    contacts = [{"type": "email", "value": kwargs.get("owner_email")}]
    if kwargs.get("web"):
        contacts.append({"type": "site", "value": kwargs.get("web")})

    return {
        "name": kwargs.get("name"),
        "description": kwargs.get("description") or None,
        "booking": kwargs.get("booking") or None,
        "naviaddress": kwargs.get("naviaddress") or None,
        "container": kwargs.get("container") or None,
        "point": kwargs.get("point") or None,
        "contacts": contacts,
        "event_start": kwargs.get("event_start")[:-1] + ".000Z",
        "event_end": kwargs.get("event_end")[:-1] + ".000Z",
        "address_description": kwargs.get("address_description") or None,
        "last_mile": kwargs.get("last_mile") or None,
        # "postal_address": kwargs.get("postal_address"),
        "cover": kwargs.get("cover") or None,
        "sharable_cover": kwargs.get("sharable_cover") or None,
        "working_hours": kwargs.get("working_hours") or None,
        "map_visibility": kwargs.get("map_visibility", False),
        "category": kwargs.get("category") or None,
        "default_lang": kwargs.get("default_lang") or "ru",
        "lang": kwargs.get("lang") or "ru"
    }
