from datetime import date
from rest_framework.exceptions import ValidationError

def validate_age_from_token(auth_payload):
   
    if not auth_payload:
        raise ValidationError("Не передан токен.")

    birthdate_str = auth_payload.get("birthdate")

    if not birthdate_str or birthdate_str == "None":
        raise ValidationError("Укажите дату рождения.")

    try:
        birthdate = date.fromisoformat(birthdate_str)
    except (ValueError, TypeError):
        raise ValidationError("Некорректный формат .")

    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет.")