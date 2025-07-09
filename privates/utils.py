def get_private_media_view_name(app_label: str, model: str, field: str) -> str:
    return f"{app_label}_{model}_{field}"
