from sanic.request import Request
from sanic.response import text

from helpers.check_request import check_request
from view.exceptions import InvalidUsage


async def user_delete_2fa(request: Request):
    request, user = await check_request(request, ['2FA_code'], True)

    if user.totp_active:
        await user.check_totp(request.json.get('2FA_code'))
        await user.update(totp_active=False, totp_key=None)
        return text('Success')
    else:
        raise InvalidUsage('Two-factor authentication not activated')
