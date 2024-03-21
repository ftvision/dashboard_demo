import gradio as gr

from data import fields, model, templates

with gr.Blocks() as demo:
    input_params = gr.State({})  # State needs to be within Block

    with gr.Row() as row:

        with gr.Column(scale=1) as input_col:
            text_boxes = {}  # collect all textbox for example later
            for field, type in fields.all_param_fields():
                param = gr.Textbox(label=field)
                param.change(
                    fn=lambda value, state, field=field: state.update({field: value}),
                    inputs=[param, input_params],
                )
                text_boxes[field] = param

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
                with gr.Tab("Annotated Render Text"):
                    annotated_render_txt = gr.HighlightedText(
                        combine_adjacent=True,
                    )
                with gr.Tab("Render Text"):
                    render_txt = gr.Textbox()

            render_btn.click(
                templates.render_tmp_annotation,
                inputs=[
                    tmp_textbox,
                    input_params,
                ],
                outputs=annotated_render_txt,
            )

            render_btn.click(
                templates.render_tmp,
                inputs=[
                    tmp_textbox,
                    input_params,
                ],
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

    gr.Examples(
        examples=[
            ["name", "param1", "param2", "param3", "param4", "template1"],
            ["n1", "p1", "p2", "p3", "p4", "template2"],
        ],
        inputs=list(text_boxes.values()) + [tmp_choice],
    )

if __name__ == "__main__":
    demo.launch()
