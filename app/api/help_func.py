def is_params_passed(json: dict, required: list) -> bool:
    return all([json.get(r) for r in required])
