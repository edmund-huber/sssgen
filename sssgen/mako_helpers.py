import re

import mako.runtime

@mako.runtime.supports_caller
def collapse_html(context):
    html = mako.runtime.capture(context, context['caller'].body)
    collapsed_html = re.sub(">\s*<", "><", html)
    context.write(collapsed_html)
