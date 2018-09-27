def is_params_passed(json: dict, required: list) -> bool:
    return all([json.get(r) for r in required])


def fill_navi_address_data(**kwargs):

    contacts = [{"type": "email", "value": kwargs.get("owner_email")}]
    if kwargs.get("web"):
        contacts.append({"type": "site", "value": kwargs.get("web")})

    return {
        "name": kwargs.get("name"),
        "description": kwargs.get("description"),
        "booking": kwargs.get("booking"),
        "naviaddress": kwargs.get("naviaddress"),
        "container": kwargs.get("container"),
        "point": kwargs.get("point"),
        "contacts": contacts,
        "event_start": kwargs.get("event_start"),
        "event_end": kwargs.get("event_end"),
        "address_description": kwargs.get("address_description"),
        "last_mile": kwargs.get("last_mile"),
        # "postal_address": kwargs.get("postal_address"),
        "cover": kwargs.get("cover"),
        "sharable_cover": kwargs.get("sharable_cover"),
        "working_hours": kwargs.get("working_hours"),
        "map_visibility": kwargs.get("map_visibility", False),
        "category": kwargs.get("category"),
        "default_lang": kwargs.get("default_lang", "ru"),
        "lang": kwargs.get("lang", "ru")
    }
