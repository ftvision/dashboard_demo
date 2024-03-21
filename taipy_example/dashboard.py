"""A demo taipy app."""

import taipy.gui.builder as tgb
from taipy.gui import Gui

from data import model, templates

with tgb.Page() as page:
    tgb.text("Getting started with Taipy GUI", class_name="h1")
    with tgb.layout(columns="1 2"):
        name, param1, param2, param3, param4 = "", "", "", "", ""
        with tgb.part():  # params
            # after multiple attempts, I didn't find a way to dynamically generate this part
            tgb.input(value="{name}", label="name", class_name="fullwidth")
            tgb.input(value="{param1}", label="param1", class_name="fullwidth")
            tgb.input(value="{param2}", label="param2", class_name="fullwidth")
            tgb.input(value="{param3}", label="param3", class_name="fullwidth")
            tgb.input(value="{param4}", label="param4", class_name="fullwidth")

        tmp_choice = "template1"
        template = templates.templates[tmp_choice]
        annotated_render_text = ""
        render_text = ""
        with tgb.part():  # rendering templates

            def retrieve_tmp(state):
                state.template = templates.templates[state.tmp_choice]

            tgb.selector(
                value="{tmp_choice}",
                lov=list(templates.templates.keys()),
                label="choose templates",
                dropdown=True,
                on_change=retrieve_tmp,
                class_name="fullwidth",
            )
            tgb.input(
                value="{template}",
                label="template",
                multiline=True,
                class_name="fullwidth",
            )

            def render_tmp(state):
                tmp = state.template
                data = {
                    "name": state.name,
                    "param1": state.param1,
                    "param2": state.param2,
                    "param3": state.param3,
                    "param4": state.param4,
                }
                state.render_text = templates.render_tmp(tmp, data)
                state.annotated_render_text = templates.render_tmp_annotation(tmp, data)

            tgb.button(label="Render", on_action=render_tmp)

            tgb.text("{render_text}", class_name="fullwidth")
            # tgb.text("{annotated_render_text}")

    with tgb.part():  # model calling
        model_resp = ""
        model_choice = model.MODELS[0]
        tgb.selector(
            value="{model_choice}",
            lov=list(model.MODELS),
            label="model choice",
            dropdown=True,
        )

        def call_model(state):
            state.model_resp = model.model_call(state.model_choice, state.render_text)

        tgb.button("Call Model", on_action=call_model)
        tgb.text("{model_resp}")


if __name__ == "__main__":
    Gui(page).run(debug=True, stylekit=True)
