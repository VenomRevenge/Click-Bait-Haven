from django.core.exceptions import ValidationError
from datetime import date

def validate_image_size(image):
    # 1 MB = 1024 KB
    MAX_SIZE = 25 * 1024 
    if image.size > MAX_SIZE * 1024:
        raise ValidationError(f"Maximum image size is {MAX_SIZE} MB.")
    

def validate_date_of_birth(value):
    MIN_DATE = date(1950, 1, 1)
    MAX_DATE = date(2024, 1, 1)
    if not MAX_DATE >= value >= MIN_DATE:
        raise ValidationError(
            f"Date of birth must be between {MIN_DATE} and {MAX_DATE}."
        )