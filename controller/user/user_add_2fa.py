from sanic.request import Request
from sanic.response import raw, text
import qrcode
import pyotp
import io

from helpers.check_request import check_request


async def user_add_2fa(request: Request):
    if request.method == 'GET':
        request, user = await check_request(request, list(), True)
        await user.add_totp()
        img_bytes = io.BytesIO()
        qrcode.make(
            pyotp.totp.TOTP(user.totp_key).provisioning_uri(name=user.login, issuer_name='Napoleon IT')
        ).save(img_bytes, format='PNG')
        return raw(img_bytes.getvalue(), content_type='image/png')
    else:
        request, user = await check_request(request, ['2FA_code'], True)
        await user.check_totp(request.json.get('2FA_code'))
        await user.update(totp_active=True)
        return text('Success')
