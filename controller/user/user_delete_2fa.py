from sanic.request import Request
from sanic.response import text

from helpers.check_request import check_request


async def user_delete_2fa(request: Request):
    request, user = await check_request(request, ['2FA_code'], True)

    await user.check_totp(request.json.get('2FA_code'))
    await user.update(totp_active=False, totp_key=None)
    return text('Success')
