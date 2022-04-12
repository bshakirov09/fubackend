class IntensityRate:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    choices = ((LOW, LOW), (MEDIUM, MEDIUM), (HIGH, HIGH))


class Mood:
    BAD = "bad"
    SAD = "sad"
    OKAY = "okay"
    GOOD = "good"
    AMAZING = "amazing"

    choices = (
        (BAD, BAD),
        (SAD, SAD),
        (OKAY, OKAY),
        (GOOD, GOOD),
        (AMAZING, AMAZING),
    )


class Digestion:
    BAD = "bad"
    SAD = "sad"
    OKAY = "okay"
    GOOD = "good"
    AMAZING = "amazing"

    choices = (
        (BAD, BAD),
        (SAD, SAD),
        (OKAY, OKAY),
        (GOOD, GOOD),
        (AMAZING, AMAZING),
    )


class Direction:
    BACK = "back"
    NEXT = "next"

    choices = ((BACK, BACK), (NEXT, NEXT))


class ActivityLevel:
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTRA_ACTIVE = "extra_active"

    choices = (
        (SEDENTARY, SEDENTARY),
        (LIGHTLY_ACTIVE, LIGHTLY_ACTIVE),
        (MODERATELY_ACTIVE, MODERATELY_ACTIVE),
        (VERY_ACTIVE, VERY_ACTIVE),
        (EXTRA_ACTIVE, EXTRA_ACTIVE),
    )
