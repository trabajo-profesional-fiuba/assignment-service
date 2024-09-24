from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class ResponseBuilder:
    def build_clear_cache_response(content, status_code):
        response = JSONResponse(content=jsonable_encoder(content))
        response.headers["Clear-Site-Data"] = '"cache"'
        response.status_code = status_code

        return response 

    def build_private_cache_response(content):
        response = JSONResponse(content=jsonable_encoder(content))
        response.headers["Cache-Control"] = "private, max-age=300"

        return response