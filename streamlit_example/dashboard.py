"""A demo streamlit app."""

import streamlit as st
from annotated_text import annotated_text

from data import fields, model, templates

st.title("Prompt Iteration Playground")


## NOTE, the following naive example of initialize st.session_state is wrong
#
# st.session_state.input_params = {}
#
# initialize and manage st.session_state is a bit tricky
def init(session_state, key, init_value):
    if key not in session_state:
        session_state[key] = init_value


init(st.session_state, "input_params", {})
init(st.session_state, "template", "")
init(st.session_state, "model_resp", "")
init(st.session_state, "rendered_text", {"raw": "", "annotated": ""})

# two columns
col1, col2 = st.columns([0.25, 0.75])

with col1:
    for field, type in fields.all_param_fields():
        st.session_state.input_params[field] = st.text_input(label=field)

with col2:
    tmp_choice = st.selectbox(
        label="choose templates", options=list(templates.templates.keys())
    )

    if tmp_choice:
        st.session_state.template = templates.templates[tmp_choice]

    tmp_textbox = st.text_area(label="template", value=st.session_state.template)

    # render template box with annotated and un-annotated result
    render_action = st.button("Render", type="primary")
    if render_action:
        st.session_state.rendered_text["annotated"] = templates.render_tmp_annotation(
            tmp_textbox, st.session_state.input_params
        )
        st.session_state.rendered_text["raw"] = templates.render_tmp(
            tmp_textbox, st.session_state.input_params
        )

    tab1, tab2 = st.tabs(["Annotated Rendering", "Raw Rendering"])
    with tab1:
        annotated_render = [
            token_pair if token_pair[1] is not None else token_pair[0]
            for token_pair in st.session_state.rendered_text["annotated"]
        ]
        annotated_text(annotated_render)
    with tab2:
        rendered_txt = st.write(st.session_state.rendered_text["raw"])

model_choice = st.selectbox(label="model choice", options=model.MODELS)
model_call_btn = st.button("Call Model")

if model_call_btn:
    st.session_state.model_resp = model.model_call(
        model_choice, st.session_state.rendered_text["raw"]
    )

model_resp = st.text_area("model output", st.session_state.model_resp)
