from flask import jsonify

class ApiResponse:
    def success(self, response, code, token=None):
        print("\nApiResponse().success()" * 3)
        print(type(response))
        msg = response if isinstance(response, str) else "Successfully"
        result = [] if isinstance(response, str) else response
        res = {
            "data": {
                "message": msg,
                "responseCode": code,
                "result": result,
            }
        }
        return jsonify(res)

    def paginationSuccess(self, response, code, count):
        res = {
            "data": {
                "message": "Successfully",
                "responseCode": code,
                "result": response,
                "total_records": count
            }
        }

        return jsonify(res)

    def error(self, response, code):
        print("\nApiResponse().error()" * 3)
        return jsonify({
            "data": {
                "message": "error",
                "responseCode": code,
                "error": response
            }
        })
