from flask import Blueprint

bp = Blueprint('api_res_output_temp', __name__)

from .dir import bp as bp_dir
bp.register_blueprint(bp_dir)

from .file import bp as bp_file
bp.register_blueprint(bp_file)
