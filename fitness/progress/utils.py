from random import randint

from django.conf import settings


def calculate_before_activity_level(gender, weight, height, age):
    out = (
        settings.RMR_WEIGHT * float(weight)
        + settings.RMR_HEIGHT * height
        - settings.RMR_AGE * age
    )
    if gender == "male":
        out += 5
    else:
        out -= 161
    return out


def find_activity_level(level):
    if level == "sedentary":
        level = settings.SEDENTARY
    elif level == "lightly_active":
        level = settings.LIGHTLY_ACTIVE
    elif level == "moderately_active":
        level = settings.MODERATELY_ACTIVE
    elif level == "very_active":
        level = settings.VERY_ACTIVE
    else:
        level = settings.EXTRA_ACTIVE
    return level


def calculate_rmr(data):
    return calculate_before_activity_level(
        data.get("gender"),
        data.get("weight"),
        data.get("height"),
        data.get("age"),
    ) * find_activity_level(data.get("activity_level"))


def calculate_macronutrients(rmr, weight):
    protein = float(weight) * 0.8
    fats = float(weight) * 0.35 - 0.45
    protein_calories = 4 * protein
    fats_calories = 4 * fats
    carbohydrates_calories = rmr - (protein_calories + fats_calories)
    carbs = carbohydrates_calories / 4
    return {
        "rmr": float("{:.2f}".format(rmr)),
        "protein": protein,
        "fats": fats,
        "carbohydrates": float("{:.2f}".format(carbohydrates_calories)),
        "carbs": float("{:.2f}".format(carbs)),
    }


def take_average(dc):
    value_list = list(dc.values())
    return sum(value_list) / len(value_list)


def find_percentage(avg_list, avg_calories):
    return float("{:.2f}".format((100 * (avg_list * 4) / avg_calories)))


def calculate_macronutrient_intake(data):
    calories_avg = take_average(data.get("calories"))
    protein_pc = find_percentage(
        take_average(data.get("protein")), calories_avg
    )
    carbohydrates_pc = find_percentage(
        take_average(data.get("carbohydrates")), calories_avg
    )
    fats_pc = find_percentage(take_average(data.get("fats")), calories_avg)
    if protein_pc < 20 or protein_pc > 30:
        protein_pc = float(randint(20, 30))
    if carbohydrates_pc < 40 or carbohydrates_pc > 50:
        carbohydrates_pc = float(randint(40, 50))
    if fats_pc < 20 or fats_pc > 30:
        fats_pc = float(randint(20, 30))

    return {
        "protein_pc": protein_pc,
        "carbohydrates_pc": carbohydrates_pc,
        "fats_pc": fats_pc,
    }
