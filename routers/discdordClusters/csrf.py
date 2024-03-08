from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect

router = APIRouter(
    prefix='/csrfToken'
)

@router.get('/')
async def get_csrf_token(csrf_protect:CsrfProtect = Depends()):
	csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
	response = JSONResponse(status_code=200, content={'csrf_token': csrf_token})
	csrf_protect.set_csrf_cookie(signed_token, response)
	return response