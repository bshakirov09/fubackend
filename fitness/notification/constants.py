class NotificationType:
    ACHIEVEMENT = "achievement"
    JOURNAL = "journal"
    PROGRESS = "progress"
    SUBSCRIPTION = "subscription"
    BLOG = "blog"

    choices = (
        (ACHIEVEMENT, ACHIEVEMENT),
        (JOURNAL, JOURNAL),
        (PROGRESS, PROGRESS),
        (SUBSCRIPTION, SUBSCRIPTION),
        (BLOG, BLOG),
    )

    @staticmethod
    def get_constant_types():
        types = [
            NotificationType.SUBSCRIPTION,
        ]
        return types

    @staticmethod
    def get_changeable_types():
        types = [
            NotificationType.ACHIEVEMENT,
            NotificationType.JOURNAL,
            NotificationType.PROGRESS,
            NotificationType.BLOG,
        ]
        return types

    @staticmethod
    def get_default_types():
        return list(dict(NotificationType.choices))
