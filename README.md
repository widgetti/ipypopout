# Ipypopout

[![Version](https://img.shields.io/pypi/v/ipypopout.svg)](https://pypi.python.org/project/ipypopout)

Use Ipypopout to display parts of your ipywidgets or solara app in separate browser windows.
This is especially useful for those working with multiple screens.

Works with:

   * Jupyter notebook
   * Jupyter lab
   * Voila (`version<0.5`)
   * [Solara](https://github.com/widgetti/solara/) (`version>=1.22`)

## Usage

### With ipywidgets

```python
import ipywidgets as widgets
from ipypopout import PopoutButton

main = widgets.VBox()

# see https://developer.mozilla.org/en-US/docs/Web/API/Window/open#window_features
# for window_features
popout_button = PopoutButton(main, window_features='popup,width=400,height=600')

slider1 = widgets.IntSlider(value=1)
slider2 = widgets.IntSlider(value=2)
result = widgets.Label()
def update_result(_ignore=None):
    result.value = value=f"Sum of {slider1.value} and {slider2.value} = {slider1.value + slider2.value}"
update_result()

main.children = (slider1, slider2, result, popout_button)
slider1.observe(update_result, "value")
slider2.observe(update_result, "value")

display(main)
```

https://github.com/widgetti/ipypopout/assets/1765949/61091b71-309c-472f-8814-184ea2012b82


### With Solara

```python
import solara
import plotly.express as px
import numpy as np
from ipypopout import PopoutButton


freq = solara.reactive(1)
damping = solara.reactive(0.5)

t = np.arange(0, 100, 0.1)/10

@solara.component
def Page():
    target_model_id = solara.use_reactive("")

    y = np.sin(t * 2 * np.pi * freq.value) * np.exp(-t*damping.value)

    with solara.Column():
        with solara.Card("Controls") as control:
            solara.SliderFloat("Freq", value=freq, min=1, max=10)
            solara.SliderFloat("zeta", value=damping, min=0, max=2)
            if target_model_id.value:
                PopoutButton.element(target_model_id=target_model_id.value, window_features='popup,width=400,height=300')
        fig = px.line(x=t, y=y)
        solara.FigurePlotly(fig)
    # with solara we have to use use_effect + get_widget to get the widget id
    solara.use_effect(lambda: target_model_id.set(solara.get_widget(control)._model_id))
display(Page())
```

Because Solara creates elements instead of widgets, we have to use the `use_effect`/`get_widget` trick to feed the widget ID to the PopoutButton.


https://github.com/widgetti/ipypopout/assets/1765949/430cae12-2527-404b-9861-610565ac1471


## Installation

```
$ pip install ipypopout
```

## API

 * PopoutButton
   * constructor arguments:
     * `target - ipywidgets.Widget | None`: The widget that will be shown in the popout window.
     * `target_model_id - str`: The widget id (defaults to `target._model_id`)
     * `window_name - str`: If a window with the same name is available it will be reused, otherwise a new window is created (defaults to `target_model_id`).
        See [https://developer.mozilla.org/en-US/docs/Web/API/Window/open](https://developer.mozilla.org/en-US/docs/Web/API/Window/open) for more details.
     * `window_features - str`: See: [https://developer.mozilla.org/en-US/docs/Web/API/Window/open#window_features](https://developer.mozilla.org/en-US/docs/Web/API/Window/open#window_features)
