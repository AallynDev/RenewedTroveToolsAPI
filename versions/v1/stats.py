from quart import Blueprint, request, abort, jsonify, current_app, send_file, Response
from PIL import Image
from enum import Enum
from aiohttp import ClientSession
from io import BytesIO
from pathlib import Path
from hashlib import md5
from versions.v1.models.database.api import API, Mastery
from versions.v1.utils.authorization import authorize
from json import loads
from base64 import b64encode

stats = Blueprint('stats', __name__, url_prefix='/stats')
stats_folder = Path('versions/v1/data')

@stats.route('/file/<path:u_path>', methods=['GET'])
async def file(u_path):
    file = stats_folder.joinpath(u_path)
    if file.exists():
        return await send_file(file)
    else:
        return abort(404)
    
@stats.route('/files', methods=['GET'])
async def files():
    return jsonify([str(x.relative_to(stats_folder)) for x in stats_folder.rglob('*') if x.is_file()])

@stats.route('/get_data', methods=['GET'])
async def get_data():
    files = {}
    for x in stats_folder.rglob('*'):
        if x.is_file():
            file_name = str(x.relative_to(stats_folder).as_posix())
            files[file_name] = b64encode(x.read_bytes()).decode('utf-8')
    return jsonify(files)

@stats.route('/mastery', methods=['GET'])
async def mastery():
    data = await API.find_one({"_id": "api"})
    if data is None:
        return abort(404)
    data = loads(data.json())["mastery"]
    return jsonify(data)
    

@stats.route('/mastery', methods=['PUT'])
async def update_mastery():
    if not (user := await authorize(request)):
        return abort(401)
    if not user.is_admin:
        return abort(403)
    data = await request.json
    try:
        mastery_data = data["mastery_data"]
    except KeyError:
        return abort(400)
    mastery = await API.find_one({"_id": "api"})
    mastery.mastery = Mastery(
        normal=mastery_data["normal"],
        geode=mastery_data["geode"],
    )
    await mastery.save()
    return "OK", 200