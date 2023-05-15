from flask import Blueprint

from controllers.projectController import index,create,insert,delete

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/create', methods=['GET'])(create)
blueprint.route('insert',methods=['GET'])(insert)
