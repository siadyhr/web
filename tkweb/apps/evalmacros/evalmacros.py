import markdown
import random
import re
import shlex
from django.template.loader import render_to_string
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
import tkweb.apps.tkbrand.templatetags.tkbrand as tkbrand
from constance import config

METHODS = [
    'begin_hide', 'end_hide',
    'TK', 'TKAA', 'TKET', 'TKETAA', 'TKETs', 'TKETsAA', 'TKETS', 'TKETSAA',
    'tk_prefix', 'tk_kprefix', 'tk_postfix', 'tk_prepostfix', 'tk_email',
]


class EvalMacroExtension(markdown.Extension):
    """Macro plugin markdown extension for django-wiki."""
    def extendMarkdown(self, md, md_globals):
        """ Insert MacroPreprocessor before ReferencePreprocessor. """
        md.preprocessors.add(
            'dw-macros', EvalMacroPreprocessor(md), '>html_block')


class EvalMacroPreprocessor(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        pattern = (
            # Start by matching one of the names in METHODS.
            r"\[(?P<macro>%s)" % '|'.join(
                re.escape(method_name) for method_name in METHODS) +
            # Then match optional arguments of at most 300 characters.
            r"(?:\s+(?P<args>[^]\n]{0,300}))?\]"
        )

        def repl(mo):
            macro = mo.group('macro')
            try:
                macro = macro.strip()
                method = getattr(self, macro)
                args_str = mo.group('args')
                args = shlex.split(args_str) if args_str else ()
                return method(*args)
            except Exception as exn:
                return '(%s.%s %r)' % (self.__class__.__name__, macro, exn)

        return [re.sub(pattern, repl, line) for line in lines]

    def get_user_groups(self):
        try:
            return self._cached_user_groups
        except AttributeError:
            self._cached_user_groups = list(
                self.markdown.user.groups.values_list('name', flat=True))
            return self._cached_user_groups

    def begin_hide(self, title='BEST'):
        expanded = any(t.lower() == title.lower()
                       for t in self.get_user_groups())
        html = render_to_string(
            "evalmacros/begin_hide.html",
            context={
                'title': title,
                'id': title+'-'+str(random.randrange(9999)),
                'expanded': expanded,
            })
        return self.markdown.htmlStash.store(html, safe=False)

    def end_hide(self):
        html = render_to_string("evalmacros/end_hide.html")
        return self.markdown.htmlStash.store(html, safe=False)

    begin_hide.meta = {
        'short_description': 'Skjul en sektion',
        'help_text': ('Skjuler en sektion der kun er relevant for nogle ' +
                      'grupper eller personer. Andre kan stadig se ' +
                      'sektionen ved at trykke på en knap.'),
        'example_code': ('[begin_hide KASS]\nNoget der er ' +
                         'skjult for alle andre end KASS.\n[end_hide]'),
        'args': {
            'title': 'Personen eller gruppen indholdet ikke er skjult for.',
        },
    }

    _TKBRANDFUNCS = [tkbrand.TK, tkbrand.TKAA, tkbrand.TKET, tkbrand.TKETAA,
                     tkbrand.TKETs, tkbrand.TKETsAA, tkbrand.TKETS,
                     tkbrand.TKETSAA]

    def TK(self):
        return tkbrand.TK()

    def TKAA(self):
        return tkbrand.TKAA()

    def TKET(self):
        return tkbrand.TKET()

    def TKETAA(self):
        return tkbrand.TKETAA()

    def TKETs(self):
        return tkbrand.TKETs()

    def TKETsAA(self):
        return tkbrand.TKETsAA()

    def TKETS(self):
        return tkbrand.TKETS()

    def TKETSAA(self):
        return tkbrand.TKETSAA()

    TK.meta = {
        'short_description': '%s og venner' % tkbrand.TKET(),
        'help_text': (
            ('Brug følgende makroer til at skrive %s og ligendene med ' +
             'hoppe-danseskrift.') % tkbrand.TKET() +
            '<table class="table table-condensed">' +
            ''.join(['<tr><td>[%s]</td><td>%s</td></tr>'
                     % (f.__name__, f()) for f in _TKBRANDFUNCS]) +
            '</table>'),
    }

    def _get_year(self, year):
        if year in (None, ''):
            return config.GFYEAR
        year = int(year)
        if year < 56:
            year += 2000
        elif year < 100:
            year += 1900
        return year

    def tk_prefix(self, year=None, title=''):
        return tkbrand.tk_prefix((title, self._get_year(year)))

    def tk_kprefix(self, year=None, title=''):
        return tkbrand.tk_kprefix((title, self._get_year(year)))

    def tk_postfix(self, year=None, title=''):
        return tkbrand.tk_postfix((title, self._get_year(year)))

    def tk_prepostfix(self, title, year=None):
        return tkbrand.tk_prepostfix((title, self._get_year(year)))

    def tk_email(self, title, year=None):
        return tkbrand.tk_email((title, self._get_year(year)))


class EvalMacroPlugin(BasePlugin):
    # TODO: settings.SLUG
    slug = "evalmacros"

    markdown_extensions = [EvalMacroExtension()]


registry.register(EvalMacroPlugin)
