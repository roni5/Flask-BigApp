from flask import render_template, session, url_for

from .. import bp, page_needs


@bp.route("/", methods=["GET"])
def index():
    render = bp.tmpl("index.html")
    print(url_for('example.example_nested.index'))
    return render_template(render, **page_needs)
