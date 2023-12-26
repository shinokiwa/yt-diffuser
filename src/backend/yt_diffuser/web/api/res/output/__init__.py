from flask import Blueprint

bp = Blueprint('api_res_output', __name__)

from .image import bp as bp_image
bp.register_blueprint(bp_image)

from .temp import bp as bp_temp
bp.register_blueprint(bp_temp)