import config


def admin(func):
    def wrapped(*args):
        if args[0].from_user.chat_id in config.admin_ids:
            func(*args)

    return wrapped
