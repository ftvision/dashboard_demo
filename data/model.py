"""A mock model call"""

MODELS = (
    "model1",
    "model2",
    "model3",
)


def model_call(model: str, prompt: str):
    if model not in MODELS:
        raise KeyError(f"{model} does not exist")

    if model == "model1":
        return f"call model1: with {prompt}"

    if model == "model2":
        import time

        time.sleep(2)
        return f"call model2, slow, with {prompt}"

    if model == "model3":
        return f"call model3, with {prompt}"
