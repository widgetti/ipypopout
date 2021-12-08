import re
import IPython
import traitlets
import ipyvuetify as v


def get_kernel_id():
    ipython = IPython.get_ipython()
    if not ipython:
        return ''
    kernel = ipython.kernel
    regex = '\\/kernel-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\\.json$'
    connection_file = kernel.config['IPKernelApp']['connection_file']
    return re.compile(regex).search(connection_file).group(1)


class PopoutButton(v.VuetifyTemplate):

    template_file = (__file__, "popout_button.vue")
    kernel_id = traitlets.Unicode('').tag(sync=True)
    target_model_id = traitlets.Unicode().tag(sync=True)

    # If a window with the same name is available it will be reused, otherwise a new window is created.
    # See https://developer.mozilla.org/en-US/docs/Web/API/Window/open
    window_name = traitlets.Unicode('').tag(sync=True)

    # See: https://developer.mozilla.org/en-US/docs/Web/API/Window/open#window_features
    window_features = traitlets.Unicode('popup').tag(sync=True)

    def __init__(self, target, **kwargs):
        self.kernel_id = get_kernel_id()
        self.target_model_id = target._model_id
        self.window_name = target._model_id
        super(PopoutButton, self).__init__(**kwargs)
