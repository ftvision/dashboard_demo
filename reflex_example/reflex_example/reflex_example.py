"""A demo reflex app."""

import reflex as rx

from data import fields, model, templates


class InputParams(rx.State):
    param: dict[str, str] = {k: "" for k, _ in fields.all_param_fields()}
    # to allow for_each iterate over all names
    param_names: list[str] = list(param.keys())

    def update_param(self, key, new_value: str):
        self.param[key] = new_value


class Template(rx.State):
    templates: list[str] = list(templates.templates.keys())
    tmp_name: str = ""
    # as an intermediate state for computed var `tmp_text`
    pick_tmp: str = ""

    @rx.var  # derived/computed variables
    def tmp_text(self) -> str:
        self.pick_tmp = (
            templates.templates.get(self.tmp_name) if self.tmp_name else self.pick_tmp
        )
        return self.pick_tmp

    def set_tmp_text(self, value) -> str:
        self.pick_tmp = value
        self.tmp_name = ""


class PromptRendering(rx.State):
    rendered_text: str = ""
    annotated_rendered_text: str = ""

    async def render(self):
        params = await self.get_state(InputParams)
        template = await self.get_state(Template)
        self.rendered_text = templates.render_tmp(template.tmp_text, params.param)


class ModelResponse(rx.State):
    model_names: list[str] = model.MODELS
    model_name: str = model_names[0]
    model_resp = ""

    async def make_call(self):
        prompt = await self.get_state(PromptRendering)
        self.model_resp = model.model_call(self.model_name, prompt.rendered_text)


def index():
    param_inputs = [
        rx.foreach(
            InputParams.param_names,
            lambda key: rx.input(
                label=key,
                placeholder=f"Enter {key}",
                value=InputParams.param[key],
                on_change=lambda new_value, key=key: InputParams.update_param(
                    key, new_value
                ),
                width="100%",
            ),
        ),
    ]
    rendering = [
        rx.select(
            Template.templates,
            placeholder="Select a template name",
            label="Template Selection",
            value=Template.tmp_name,
            on_change=Template.set_tmp_name,
            width="100%",
        ),
        rx.text_area(
            placeholder="template",
            value=Template.tmp_text,
            on_change=Template.set_tmp_text,
            width="100%",
        ),
        rx.button("Render Prompt", on_click=PromptRendering.render),
        rx.text_area(
            placeholder="rendered_text",
            value=PromptRendering.rendered_text,
            width="100%",
        ),
    ]
    model_call = [
        rx.select(
            ModelResponse.model_names,
            placeholder=ModelResponse.model_name,
            label="Model Selection",
            on_change=ModelResponse.set_model_name,
        ),
        rx.button("Model Call", on_click=ModelResponse.make_call),
        rx.text_area(value=ModelResponse.model_resp),
    ]
    return rx.center(
        rx.vstack(
            rx.heading("Playground", font_size="2em"),
            rx.hstack(
                rx.vstack(*param_inputs, width="100%"),
                rx.vstack(*rendering, width="100%"),
                width="100%",
            ),
            rx.box(*model_call, width="100%"),
            width="80%",
        ),
        width="90%",
    )


app = rx.App()
app.add_page(index)
