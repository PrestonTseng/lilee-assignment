from flask import request, Blueprint, jsonify, abort
from model import Vehicle
from model import db
import traceback
import sys


def abort_msg(e):
    """500 bad request for exception

    Returns:
        500 and msg which caused problems
    """
    error_class = e.__class__.__name__  # 引發錯誤的 class
    detail = e.args[0]  # 得到詳細的訊息
    cl, exc, tb = sys.exc_info()  # 得到錯誤的完整資訊 Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # 取得最後一行的錯誤訊息
    fileName = lastCallStack[0]  # 錯誤的檔案位置名稱
    lineNum = lastCallStack[1]  # 錯誤行數
    funcName = lastCallStack[2]  # function 名稱
    # generate the error message
    errMsg = "Exception raise in file: {}, line {}, in {}: [{}] {}. Please contact the member who is the person in charge of project!".format(
        fileName, lineNum, funcName, error_class, detail
    )
    # return 500 code
    abort(500, errMsg)


blue_vehicle = Blueprint("vehicles", __name__)


@blue_vehicle.route("", methods=["GET"])
def get_vehicles_all():
    try:
        results = Vehicle.query.all()
        return jsonify([result.get_dict() for result in results])
    except Exception as e:
        abort_msg(e)


@blue_vehicle.route("", methods=["POST"])
def add_vehicle():
    data = request.get_json()
    try:
        entity = Vehicle(data["name"])
        db.session.add(entity)
        db.session.commit()
        return jsonify(entity.get_dict())
    except Exception as e:
        abort_msg(e)


@blue_vehicle.route("/<id>", methods=["PUT"])
def update_vehicle(id):
    data = request.get_json()
    try:
        entity = db.get_or_404(Vehicle, id)
        entity.name = data["name"]
        db.session.commit()
        return jsonify(entity.get_dict())
    except Exception as e:
        abort_msg(e)


@blue_vehicle.route("/<id>", methods=["DELETE"])
def delete_vehicle(id):
    try:
        entity = db.get_or_404(Vehicle, id)
        db.session.delete(entity)
        db.session.commit()
        return jsonify(True)
    except Exception as e:
        abort_msg(e)
