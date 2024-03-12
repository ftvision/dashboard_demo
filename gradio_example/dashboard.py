import gradio as gr

from data import fields, model, templates


def greet(name):
    return "Hello " + name + "!"


with gr.Blocks() as demo:
    with gr.Row() as row:
        # input parameters
        with gr.Column(scale=1) as params:
            text_boxes = set()  # try dynamically generate param textbox
            for field, type in fields.all_param_fields():
                text_boxes.add(gr.Textbox(label=field))

        # using parameters and templates to render prompt
        with gr.Column(scale=3) as render:
            tmp_choice = gr.Dropdown(
                list(templates.templates.keys()), label="choose template"
            )
            tmp_textbox = gr.Textbox(label="template", interactive=True)
            tmp_choice.change(
                lambda tmp_name: templates.templates[tmp_name],
                inputs=tmp_choice,
                outputs=tmp_textbox,
            )
            with gr.Group() as render_grp:
                render_btn = gr.Button("Render")
                render_txt = gr.Markdown("text-to-be-rendered", label="rendered text")

            def render(component_data: dict):
                # this is a bit weird syntax from Gradio.
                # if inputs are passed in as a set() in the event, the callback would get a dictionary as input
                data = {}
                for param_box in text_boxes:
                    data[param_box.label] = component_data[param_box]
                text = templates.render_tmp(component_data[tmp_textbox], data)
                return text

            render_btn.click(
                render,
                inputs=text_boxes | {tmp_textbox},  # dynamically get multiple input
                outputs=render_txt,
            )

    # run model
    with gr.Group() as model_run:
        model_choice = gr.Dropdown(model.MODELS)
        model_call_btn = gr.Button("Call Model")
        model_resp = gr.Markdown("Wait for Model Return")
        model_call_btn.click(
            fn=model.model_call,
            inputs=[model_choice, render_txt],
            outputs=model_resp,
            api_name="model_call",
        )

demo.launch()
