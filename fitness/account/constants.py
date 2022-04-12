class DeviceType:
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"

    choices = ((WEB, WEB), (IOS, IOS), (ANDROID, ANDROID))


class GENDER:
    MALE = "male"
    FEMALE = "female"

    choices = ((MALE, MALE), (FEMALE, FEMALE))


class AuthType:
    SOCIAL = "social"
    EMAIL = "email"

    choices = ((SOCIAL, SOCIAL), (EMAIL, EMAIL))
