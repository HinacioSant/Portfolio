import os
from django.core.exceptions import ValidationError

def validate_file_size(value):
    max_size = 20793818
    min_size = 7938

    size = value.size
    if size < min_size:
        raise ValidationError("Images should have at least 10kb")

    if size > max_size:
        raise ValidationError("Images should have at max 20mb")
