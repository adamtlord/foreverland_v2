import os
import uuid

RECEIPT_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp"}
RECEIPT_MAX_BYTES = 10 * 1024 * 1024


def receipt_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in RECEIPT_EXTENSIONS:
        ext = ".bin"
    return "receipts/%s%s" % (uuid.uuid4().hex, ext)


def staff_receipt_url(file_field):
    """Staff-only URL for a receipt/settlement FileField."""
    from django.urls import reverse

    name = getattr(file_field, "name", "") or str(file_field)
    if name.startswith("receipts/"):
        name = name[len("receipts/") :]
    return reverse("private_receipt", kwargs={"filename": name})


def validate_receipt_file(uploaded):
    """Return an error string or None."""
    if not uploaded:
        return None
    name = getattr(uploaded, "name", "")
    ext = os.path.splitext(name)[1].lower()
    if ext not in RECEIPT_EXTENSIONS:
        return "Receipts must be an image or PDF."
    size = getattr(uploaded, "size", 0) or 0
    if size > RECEIPT_MAX_BYTES:
        return "Receipts must be 10 MB or smaller."
    return None
