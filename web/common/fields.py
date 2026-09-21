import base64
import hashlib
import os

from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet, InvalidToken


def _fernet():
    raw = os.environ.get("SSN_ENCRYPTION_KEY") or settings.SECRET_KEY or "dev"
    digest = hashlib.sha256(raw.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


class EncryptedCharField(models.CharField):
    """Fernet-at-rest CharField. Legacy plaintext values decrypt as-is."""

    def from_db_value(self, value, expression, connection):
        return self._decrypt(value)

    def to_python(self, value):
        return self._decrypt(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self._encrypt(value)

    def _decrypt(self, value):
        if value in (None, ""):
            return value
        try:
            return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")
        except (InvalidToken, ValueError, TypeError):
            return value

    def _encrypt(self, value):
        if value in (None, ""):
            return value
        try:
            _fernet().decrypt(value.encode("utf-8"))
            return value
        except (InvalidToken, ValueError, TypeError):
            return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")
