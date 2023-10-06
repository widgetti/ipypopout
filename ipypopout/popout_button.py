import os
import re
import IPython
import traitlets
import ipywidgets
import ipyvuetify as v
import sys


def get_kernel_id():
    if "solara" in sys.modules:
        import solara
        if solara._using_solara_server():
            import solara.server.kernel_context

            context = solara.server.kernel_context.get_current_context()
            return context.id
    ipython = IPython.get_ipython()
    if not ipython or not hasattr(ipython, 'kernel'):
        return ''
    try:
        kernel = ipython.kernel
        regex = r'[\\/]kernel-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.json$'
        connection_file = kernel.config['IPKernelApp']['connection_file']
        return re.compile(regex).search(connection_file).group(1)
    except Exception:
        return ''


class PopoutButton(v.VuetifyTemplate):

    template_file = (__file__, "popout_button.vue")
    kernel_id = traitlets.Unicode('').tag(sync=True)
    target_model_id = traitlets.Unicode().tag(sync=True)
    echo_available = traitlets.Bool(False).tag(sync=True)

    is_displayed = traitlets.Bool(False).tag(sync=True)
    open_window_on_display = traitlets.Bool(False).tag(sync=True)
    open_tab_on_display = traitlets.Bool(False).tag(sync=True)

    # If a window with the same name is available it will be reused, otherwise a new window is created.
    # See https://developer.mozilla.org/en-US/docs/Web/API/Window/open
    window_name = traitlets.Unicode('').tag(sync=True)

    # See: https://developer.mozilla.org/en-US/docs/Web/API/Window/open#window_features
    window_features = traitlets.Unicode('popup').tag(sync=True)

    def __init__(self, target, **kwargs):
        self.kernel_id = get_kernel_id()
        self.target_model_id = target._model_id
        self.window_name = target._model_id

        if os.environ.get("JUPYTER_WIDGETS_ECHO") is None:
            ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO = True

        self.echo_available = ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO
        super(PopoutButton, self).__init__(**kwargs)

    def open_window(self):
        if self.is_displayed:
            self.send({
                'method': 'open_window',
            })
        else:
            self.open_window_on_display = True
            display(v.Html(tag="div", children=[self], style_="display: none"))

    def open_tab(self):
        if self.is_displayed:
            self.send({
                'method': 'open_tab',
            })
        else:
            self.open_tab_on_display = True
            display(v.Html(tag="div", children=[self], style_="display: none"))
