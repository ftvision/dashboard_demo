# Comparison between `Gradio`, `Streamlit`, `Taipy`, and `Reflex`

## Summary

All four libraries are **Python Only Web App/Dashboard** makers. Users don't need to learn anything about frontend design, such as React, Selvte, Vanilla Javascript, CSS, or even HTML. They say: "Python is all you need". 


|                                   | Gradio       | Streamlit | Taipy               | Reflex              |
| :-------------------------------- | :----------- | :-------- | :------------------ | :------------------ |
| **Supporting Company**            | Hugging Face | Snowflake | Independent Startup | Independent Startup |
| **Dependency Count (in MacOS)**   | 71           | 44        | 88                  | 65                  |
| **LoC for Demo**                  | 79           | 69        | 79                  | 118                 |
| **Web Server**                    | FastAPI      | Tornado   | Flask               | npm?                |
| **Easiness Ranking**              | 1 (tie)      | 1 (tie)   | 2                   | 3                   |
| **View Ranking**                  | 2            | 1         | 3 (tie)             | 3 (tie)             |
| **Data/State Management Ranking** | 2            | 3         | 4                   | 1                   |
| **Web Sever Ranking**             | 1            | 2         | 3                   | 4                   |

Note that **Reflex** has a dependency of Pydantic 1.10, whereas **Gradio** has a pydantic 2.0+. If the rest of your project has dependency on Pydantic, you probably can only choose one of these two.

## Learning Curve and User Friendliness

I have no prior experience with any of these libraries; I've learned all these libraries for this project. 

From a beginner's perspective, all four libraries offer relatively gentle learning curves, with **Gradio** and **Streamlit** potentially having the shallowest slopes. Both of these libraries prioritize simplicity and ease of use, allowing users to quickly grasp their concepts and start building interactive applications.

Documentation plays a crucial role in facilitating the learning process, and all four libraries excel in this aspect. They provide comprehensive tutorials, API references, and concrete examples, enabling users to understand the libraries' functionalities through practical implementation. However, **Gradio** and **Streamlit** stand out with their extensive documentation and larger community support. This abundance of resources not only includes official documentation but also external sources like Google Search, Github, and Reddit, where users can find additional help and guidance.

**Reflex** takes user support a step further by incorporating an AI chatbot into its documentation interface. This innovative feature provides a chat-GPT-ish interface within the search box, allowing beginners to ask questions and receive responses with references to documentation and examples. This interactive support mechanism enhances the user-friendliness of **Reflex** for those new to the library.

**Conclusion:** for rapid prototype and researcher tooling, I would prefer to learn **Gradio** = **Streamlit** > **Taipy** > **Reflex**. If users would like to how lower control of frontend design, **Reflex** is probably a better choice.

## View Creation: Layout & UI Components

**Gradio** comes with a lot of UI components that developers can use to make web apps that allow users to interact with machine learning (ML) or AI models. It is so deeply coupled with the ML field that it has a lot of out-of-box components for ML workflows. It has two major ways to create UIs: via `gr.Interface` or via `Blocks`. The `gr.Interface` is a UI for a single function. In many cases, this is really fast for prototyping. `gr.Blocks` gives users more flexibility to customize the view. 

**Gradio** view API leverage Python's [`with`-statement](https://docs.python.org/3/reference/compound_stmts.html#with) and [Context Manager](https://docs.python.org/3/library/stdtypes.html#context-manager-types) to make UI layout easier to manage.

```python
with gr.Row() as row:
    with gr.Column(scale=1) as input_col:
        gr.Textbox(label="Left Column TextBox")

    with gr.Column(scale=3) as render:
        tmp_choice = gr.Dropdown(
                ["tmp1", "tmp2"], label="choose template"
            )
```


**Streamlit** is similar to **Gradio**, with the same amount of, if not more, out-of-box UI Components. It also has a very active community that contributes even more pre-defined UI Components. 

```python
col1, col2 = st.columns([0.25, 0.75])

with col1:  # a narrower column on the left
    st.text_input(label="Left Column TextBox")
 
with col2:  # a wider column on the right
    tmp_choice = st.selectbox(label="choose templates", options=["tmp1", "tmp2"])
```

It also leverages the `with`-statement, and the entire python module would be a full page.

**Taipy** seems to focus on featuring Markdown-driven view definition. I personally find its customized Markdown syntax adds unnecessary complexity and doesn't play very well with python native code. It also provides python native API though, but it is much harder for me to dynamically generate UI components like I did in **Gradio and Streamlit** (see the comments in the `taipy_example/dashboard`). In fact, **Taipy** is the only library I gave up on dynamically generating the parameter input boxes. It also is still in development, so it doesn't have as many UI Components as the others have. 

However, **Taipy** claims they provide more responsive UI interactions, especially for interative figures.

**Reflex** takes a very different approach from the other three. It uses a nested input to set up the layout, as in the example below.

```python
rx.hstack(
    rx.vstack(
        rx.input(label="Left Colume")
    ),
    rx.vstack(
        rx.select(
            ["tmp1", "tmp2"],
            label="Template Selection",
        ),
    ),
),
```

It has a lot of UI Components, but needs users to set up the styling correctly. On the one hand, it provides the flexbility; on the other hand, it asks too much for users who may not be a frontend developer or who may not be interested in putting beauty in front of functionality.


**Conclusion** I would prefer **Streamlit** > **Gradio** > **Taipy** ~ **Reflex**


## Data Interaction: Events, Callbacks, and State Management

**Gradio** defines the event callback with vanilla python functions, with input parameters and return values. To supply this function as a event callbacks, we need to define `inputs` and `outputs` UI Components, where the **value** of these UI Components will be read and write by the function. 

```python
button = gr.Button("Call Model")
output_ui_component = gr.Markdown("Wait for Model Return")
button.click(
    fn=foo,
    inputs=[intput_ui_component_1, intput_ui_component_2],
    outputs=output_ui_component,
)
```

In most cases, it's a straightforward mapping. Sometimes, if you need to retrieve some dynamic attributes of the UI Components, you may need to supply `inputs` and `output` differently, or use `gr.State`.


**Streamlit** has a very interesting way of controlling events -- it renders the entire page from top to bottom whenever there is a UI event. This simplifies the code reasoning, and does not need users to reason through a callback hell in a large project. All you need to do if check if an event has happend to a UI component at the current iteration of rendering.

```python
clicked = st.button("Call Model") # each iteration, this will get checked.

if clicked:
    st.session_state.some_field = foo(input1, input2)
    # now an exercise question: what if you have two buttons and you can only click one

st.write(st.session_state.some_field)  # use `some_field` in another UI component.
```

This is really nice for many apps, but it actually becomes counter-productive when users really want to have controlled, local interaction between several specific UI components. Also, alway refreshing the whole page raises potential performance concerns: what is you have a large amount of data, but everytime you only need to change a very small subset? Streamlit may re-render the entire set of data again and again, with a slight touch on any UI piece. To manage the state in a session, it provides `st.session_state`, which is almost a dictionary. The always-top-to-bottom rendering logic sometimes interact with `st.session_state` in a counter-intuitive way. See the *NOTE on session_state initialization* in `streamlit_example/dashboard.py`


**Taipy** uses traditional `on_change`, `on_click` event callbacks to control the data interaction between different UI components. Each callback function takes the entire `state` in the current session as input and allow data manipulations within the `state`. One interesting aspect of the state is the *variable binding* -- Taipy's `state` automatically gets the data from the locally defined variables. This allows a UI component to have value as `{var}` that be be directly resolved with a local `var`. 

```python
def call_model(state):  # callback function, takes `state` as inout
    state.model_resp = model.model_call(state.model_choice, state.render_text)

tgb.button("Call Model", on_action=call_model)
tgb.text("{model_resp}")  # variable binding
```

However, personally I found it brings more inconvenience to me: I don't know how to dynamically create state fields in local and get variable binding, and I don't know how to handle a varible of `dict` type with a dynamic key (`"{{dictionary[{field}]}}"` doesn't seem to work). 

**Reflex** is very similar to **Taipy**, with event callbacks such as `on_change`, `on_click` for data interaction. It puts an emphasize on properly modeling data states (with `rx.State`). Each state is a class, with data fields and member functions, where data fields represents the state of the data, member functions represents the computations and manipulations of data and serve as callback function instances.

```python
class ModelResponse(rx.State):
    model_names: list[str] = model.MODELS
    model_name: str = model_names[0]
    model_resp = ""

    async def make_call(self):
        # one state can get another state in global space.
        prompt = await self.get_state(PromptRendering)
        # callback is responsible for changing the state, and UI is responsible for rendering the state.
        self.model_resp = model.model_call(self.model_name, prompt.rendered_text)

rx.button("Model Call", on_click=ModelResponse.make_call),
rx.text_area(value=ModelResponse.model_resp),
```

**Conclusion**: for state management, I really like **Reflex**'s emphasis on `rx.State` data modeling. After learning that, I was able to leverage **Gradio**'s `gradio.State` better to simplify my dashboard code. Combining event-driven data interaction and state management, I would prefer **Gradio** > **Reflex** > **Streamlit** > **Taipy**. However, performance is a missing piece in my ranking.

## Serving: web servers

Ultimately, web apps are served by web services. Behind the scence, each library has chosen their underlying web service framework.

**Gradio** uses [the **FastAPI** framework](https://github.com/gradio-app/gradio/blob/main/gradio/blocks.py#L1996-L1999), a morden high performance, asynchronous web framework in Python. Because it uses **FastAPI**, it can be easily mounted on any existing FastAPI services. Mounting multiple demo as different endpoints of a FastAPI service is the way to create a multi-page web app.

**Streamlit** uses the **Tornado** framework, anothe asynchrnous web framework. To launch a web server, you need to run ```python -m streamlit run``` or put the streamlit CLI library into the `main`. To create a multi-page web app, we follow [the required directory structure](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app) and let streamlit to figure out how to organize the web pages.

**Taipy** uses the **Flask** framework, a micro-framework for web development. To create a multi-page web app, it allows user to configure a route table. If users have previous extensive experience with Flask, they may like Taipy.

**Reflex** has its own web framework, and it seems that it uses npm. This makes it not a clean Python-only framework, in my opinion. To run the server, you need to ```reflex init``` the directory first, then ```reflex run```.

**Conclusion**: for underlying web server performance and flexbility, I would prefer **Gradio** > **Streamlit** > **Taipy** > **Reflex**. 