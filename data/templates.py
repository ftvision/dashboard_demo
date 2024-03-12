templates = {
    "template1": "this is template 1: {name} has {param1}",
    "template2": "this is template 2: {name} has {param1}, {param2}, {param3}",
}


def render_tmp(tmp: str, data: dict):
    data = {
        k: f"***{v}***" if v else "" for k, v in data.items()
    }  # stringize data and add markdown bold + italize
    rendered_text = tmp.format_map(data)
    return rendered_text


def render(template_name: str, data: dict = None):
    if template_name not in templates:
        raise KeyError(f"{template_name} is not one of template")
    tmp = templates[template_name]
    return render_tmp(tmp, data)


def test_render():
    data = {"name": "test", "param1": "a", "param2": "b", "param3": "c"}
    ret = render("template1", data)
    print(ret)

    ret = render("template2", data)
    print(ret)
