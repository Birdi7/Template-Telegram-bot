from .scripts import i18n

# no f-strings here!


def _(string, cache_enable=False):
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


