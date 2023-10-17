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
            try:
                import solara.server.kernel_context

                context = solara.server.kernel_context.get_current_context()
                return context.id
            except RuntimeError:
                pass
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
    target = traitlets.Instance(ipywidgets.Widget, allow_none=True)
    echo_available = traitlets.Bool(False).tag(sync=True)

    is_displayed = traitlets.Bool(False).tag(sync=True)
    open_window_on_display = traitlets.Bool(False).tag(sync=True)
    open_tab_on_display = traitlets.Bool(False).tag(sync=True)

    # If a window with the same name is available it will be reused, otherwise a new window is created.
    # See https://developer.mozilla.org/en-US/docs/Web/API/Window/open
    window_name = traitlets.Unicode('').tag(sync=True)

    # See: https://developer.mozilla.org/en-US/docs/Web/API/Window/open#window_features
    window_features = traitlets.Unicode('popup').tag(sync=True)

    def __init__(self, target=None, **kwargs):
        kwargs = kwargs.copy()

        if os.environ.get("JUPYTER_WIDGETS_ECHO") is None:
            ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO = True

        self.echo_available = ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO
        if target is not None:
            kwargs = {**kwargs, **{'target': target}}
        super(PopoutButton, self).__init__(**kwargs)

    @traitlets.observe('target')
    def _on_target_change(self, change):
        if change['new'] is not None:
            self.target_model_id = change['new']._model_id
            self.window_name = change['new']._model_id

    @traitlets.default("target_model_id")
    def _default_target_model_id(self):
        if self.target is not None:
            return self.target._model_id
        return ""

    @traitlets.default("window_name")
    def _default_window_name(self):
        return self.target_model_id or ""

    @traitlets.default("kernel_id")
    def _default_kernel_id(self):
        return get_kernel_id()


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
