import os
import traceback
import requests
from dotenv import load_dotenv
load_dotenv()


class SendErrorToBotMiddleware:
    def __init__(self, get_response, model=None):
        self.get_response = get_response
        self.model = model

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        token = os.getenv('TOKEN')
        chat_id = os.getenv('MY_CHAT_ID')
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        traceback_info = traceback.format_exc()
        exception_type = type(exception).__name__
        user = request.user
        project_name = "IMB"
        if request.user.is_authenticated:
            message = f"{project_name}\n{exception_type}: {str(exception)}\n\n{traceback_info}\n\n{project_name} (username: {user.username} ({user.first_name} {user.last_name}))"
        else:

            message = f"{project_name}\n{exception_type}: {str(exception)}\n\n{traceback_info}\n\n{project_name}"
        data = {
            'chat_id': chat_id,
            'text': message
        }
        requests.post(url=url, params=data)
