from django.core.exceptions import ValidationError


def range_validate(value):
    if value < 1 or value > 5:
        raise ValidationError("Поле должно быть от 1 до 5")


def friendliness_text_validate(value):
    if value not in ["Tiny", "Small", "Medium", "Large"]:
        raise ValidationError(
            "Поле должно быть только 'Tiny', 'Small', 'Medium', 'Large'"
        )
