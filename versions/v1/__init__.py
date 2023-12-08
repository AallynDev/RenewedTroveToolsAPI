from quart import Blueprint

from .mods import mods
from .star_chart import star

api_v1 = Blueprint('api_v1', __name__, url_prefix='/v1', subdomain="kiwiapi")
# Register Endpoints
api_v1.register_blueprint(star)
api_v1.register_blueprint(mods)
