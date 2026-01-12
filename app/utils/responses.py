from flask import jsonify

def success(data, message="OK", status_code=200, redirect_url=None):
    return jsonify({
        "success": True,
        "msg": message,
        "data": data,
        "redirect_url":redirect_url
    }), status_code


def error(message, status_code=400, data={},redirect_url=None):
    return jsonify({
        "success": False,
        "error": message,
        "data": data,
        "redirect_url":redirect_url
    }), status_code
