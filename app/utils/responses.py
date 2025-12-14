from flask import jsonify

def success(data, message="OK", status_code=200):
    return jsonify({
        "success": True,
        "msg": message,
        "data": data
    }), status_code


def error(message, status_code=400):
    return jsonify({
        "success": False,
        "message": message
    }), status_code
