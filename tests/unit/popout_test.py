import ipypopout
import ipywidgets as widgets


def test_create_target():
    box = widgets.VBox()
    button = ipypopout.PopoutButton(target=box)
    assert button.target_model_id == box._model_id
    assert button.window_name == box._model_id

    box2 = widgets.VBox()
    button.target = box2
    assert button.target_model_id == box2._model_id
    assert button.window_name == box2._model_id

