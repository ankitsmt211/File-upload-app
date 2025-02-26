from Fileapp.models.user import User
from Fileapp.utils.jwt.jwt_encoder_decoder import JWTManager
from Fileapp.utils.password_hashing import Encrypt
from Fileapp.utils.response_handler.response_handler import ResponseEngine


class Login:

    def on_post(self, request, response):
        user_name = request.media.get('user_name', '')
        password = request.media.get('password', '')
        if not user_name:
            return ResponseEngine(response=response, body='Please Enter Username/Email').error_response()
        elif not password:
            return ResponseEngine(response=response, body='Please Enter Password').error_response()
        user_obj = User.objects.filter(user_name=user_name).first()
        if not user_obj:
            return ResponseEngine(response=response, body='User doesnot exists').error_response()

        decrypted_password = Encrypt.decrypt(password, user_obj.password)
        if not decrypted_password:
            return ResponseEngine(response=response, body='Invalid Password').error_response()
        payload = {'user_id': str(user_obj.pk)}
        jwt = JWTManager()
        token = jwt.encode(payload=payload)
        return ResponseEngine(response=response, body={'user': user_obj.to_dict, 'token': token}).success_response()
