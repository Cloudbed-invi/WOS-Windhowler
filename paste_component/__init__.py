import streamlit.components.v1 as components

_paste_component = components.declare_component(
    "paste_component",
    path="paste_component/frontend"
)

def paste_listener(key=None):
    return _paste_component(key=key, default=None)
