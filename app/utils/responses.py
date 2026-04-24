from flask import jsonify

def success_response(data, message=None, status_code=200, extra=None):
    response = {"success": True, "data": data}
    if message:
        response["message"] = message
    if extra:
        response.update(extra)
    return jsonify(response), status_code

def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code
