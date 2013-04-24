from flask import Blueprint, render_template
from app_tt.engine.model import Model

blueprint = Blueprint('tt4', __name__)


@blueprint.route('/<string(maxlength=255):book>/<int:page>/<int:table>')
def index(book, page, table):
    model = Model()
    coords = model.get_cells(book, page, table)
    coords = [list(coord) for coord in coords]

    cells = []
    
    #Preparing cells for javascript draw
    for idx in range(len(coords)):
        cells.append(dict(
            left=coords[idx][0],
            top=coords[idx][1],
            width=coords[idx][2] - coords[idx][0],
            height=coords[idx][3] - coords[idx][1],
            id=idx,
            text=coords[idx][4]))

    table_url = model.get_table_url(book, page, table)
    task_info = dict(url=table_url, cells=cells)
    return render_template('tt4/template_tt4.html', table=task_info)
