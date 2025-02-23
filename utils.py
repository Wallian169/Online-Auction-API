import uuid


def get_unique_image_name(
    filename: str,
) -> str:
    name, ext = filename.split(".")
    unique_filename = f"{name}-{uuid.uuid4().hex[:10]}.{ext}"
    return f"{unique_filename}"
