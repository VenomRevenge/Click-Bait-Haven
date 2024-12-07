import aiohttp
from click_bait_haven import settings

async def send_email(name, email, message, user_info):

    url = 'https://api.web3forms.com/submit'
    access_key = settings.WEB3FORMS_EMAIL_ACCESS_KEY

    account_user = user_info.get('name', None)
    account_email = user_info.get('email', None)

    message = f"The user from Click-Bait haven {account_user} with email {account_email} has sent you a message:\n\n\n" + message

    payload = {
        'access_key': access_key,
        'email': email,
        'name': name,
        'message': message,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            status = response.status
            return status
