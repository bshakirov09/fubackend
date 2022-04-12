class PageChoices:
    RECIPE_CATEGORY = "recipe_category"
    RECIPE = "recipe"
    RECIPE_DETAIL = "recipe_detail"
    BLOG = "blog"
    WORKOUT = "workout"

    choices = (
        (RECIPE_CATEGORY, RECIPE_CATEGORY),
        (RECIPE, RECIPE),
        (BLOG, BLOG),
        (WORKOUT, WORKOUT),
        (RECIPE_DETAIL, RECIPE_DETAIL),
    )


class PermissionTags:
    PROGRESS = "progress"
    BLOG = "blog"
    WORKOUT = "workout"
    RECIPE = "recipe"
    PROFILE = "profile"
    TERMS = "terms"

    @staticmethod
    def get_unrestricted_tags():
        tags = [
            PermissionTags.PROFILE,
            PermissionTags.BLOG,
            PermissionTags.TERMS,
        ]
        return tags
