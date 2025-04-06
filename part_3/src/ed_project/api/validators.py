from django.core.exceptions import ValidationError

def range_validate(value):
    """
    Валидатор для проверки диапазона значений.

    Args:
        value (int): Значение для проверки.

    Raises:
        ValidationError: Если значение не находится в диапазоне от 1 до 5.
    """
    if value < 1 or value > 5:
        raise ValidationError("Поле должно быть от 1 до 5")

def friendliness_text_validate(value):
    """
    Валидатор для проверки текста дружелюбности.

    Args:
        value (str): Значение для проверки.

    Raises:
        ValidationError: Если значение не является одним из допустимых вариантов.
    """
    if value not in ["Tiny", "Small", "Medium", "Large"]:
        raise ValidationError(
            "Поле должно быть только 'Tiny', 'Small', 'Medium', 'Large'"
        )
