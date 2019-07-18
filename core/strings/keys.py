from .scripts import i18n

# no f-strings here!


def _(string, cache_enable=False):
    """
    why the cache enable parameters is needed:
    after starting the script, every var here will be
    a LazyProxy object. When .value will be invoked, without cache_enable=True
    it will be cache for the object after the first calling. As a result,
    the text for the locale with which the first calling was called will be for this object

    Example:

    i18n.set_ctx_locale('ru')
    bot.send_msg(..., start_cmd) # here the string will be russian
    i18n.set_ctx_locale('en')
    bot.send_msg(..., start_cmd) # here the string will still be russian because of cache value

    :param string:
    :param cache_enable:
    :return:
    """
    # why the cache enable parameters is needed:
    # after starting the script, every var here will be
    #
    return i18n.lazy_gettext(string, cache_enable=cache_enable)


start_cmd = _("start_cmd_text")
help_cmd = _("help_command_text, formats: {name}")
drop_cmd = _("drop_cmd_text")
feedback_command = _('feedback_command')
feedback_response = _('Developer answered:\n{text}')

language_choice = _('choose lang')
language_set = _('Language set!')

got = _('got')


cancel = _('cancelled')
mailing_everyone = _('mailing_everyone')


