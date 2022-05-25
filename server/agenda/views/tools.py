import os
import io

import flask
import ezt

TEMPLATES_DIR = os.path.join(os.path.abspath('agenda'), flask.current_app.template_folder)


def load_template(tname):
    return ezt.Template(os.path.join(TEMPLATES_DIR, tname),
                        base_format=ezt.FORMAT_HTML)


def render(t, data):
    "Helper to render a template/page with some data."

    # Add some default/basic data, without modifying the callers' data.
    augmented = data.copy()
    augmented.update({
        'bs_css_url': flask.url_for('static', filename='css/bootstrap.min.css'),
        'navbar_css_url': flask.url_for('static', filename='css/navbar-top-fixed.css'),
        'bs_js_url': flask.url_for('static', filename='js/bootstrap.min.js'),
        })

    buf = io.StringIO()
    t.generate(buf, augmented)
    return buf.getvalue()