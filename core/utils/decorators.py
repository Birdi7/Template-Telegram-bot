from core.configs import telegram


def admin(func):
    def wrapped(*args):
        if args[0].from_user.chat_id in telegram.ADMIN_IDS:
            func(*args)

    return wrapped
