from django.core.exceptions import ValidationError

def validate_image_size(image):
    # 1 MB = 1024 KB
    MAX_SIZE = 15 * 1024 
    if image.size > MAX_SIZE * 1024:
        raise ValidationError(f"Maximum image size is {MAX_SIZE} MB.")