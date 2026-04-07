from pathlib import Path
from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = Path(__file__).parent

_jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(template_name: str, **context) -> str:
    template = _jinja_env.get_template(template_name)
    return template.render(**context)
