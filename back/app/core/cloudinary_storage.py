from __future__ import annotations

import cloudinary
import cloudinary.uploader

from app.core.config import settings


def configure_cloudinary():
    
    if (
        not settings.cloudinary_cloud_name
        or not settings.cloudinary_api_key
        or not settings.cloudinary_api_secret
    ):
        raise RuntimeError(
            "Missing Cloudinary credentials: "
            "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET"
        )

    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    cfg = cloudinary.config()
    print("Cloudinary runtime config:")
    print("  cloud_name:", cfg.cloud_name)
    print("  api_key:", cfg.api_key)
    print("  api_secret set:", bool(cfg.api_secret))


def upload_image(
    local_path: str,
    folder: str = "cv2026",
    filename: str | None = None,
) -> dict:
    configure_cloudinary()

    upload_options = {
        "folder": folder,
        "resource_type": "image",
    }

    if filename:
        upload_options["public_id"] = filename

    result = cloudinary.uploader.upload(
        local_path,
        **upload_options,
    )

    return {
        "public_id": result["public_id"],
        "secure_url": result["secure_url"],
        "version": result.get("version"),
        "format": result.get("format"),
        "bytes": result.get("bytes"),
        "width": result.get("width"),
        "height": result.get("height"),
    }