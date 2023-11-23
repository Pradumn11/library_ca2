from flask import Flask, jsonify
from src.controller.UserController import user_controller
from src.controller.BookController import book_controller
from src.exceptions.LibraryException import LibraryException


myapp = Flask(__name__, static_url_path='/static')
myapp.static_url_path = '/static'
myapp.register_blueprint(user_controller, url_prefix='/user')

myapp.config['SECRET_KEY'] = 'ABSBSBSBBSBSBBSBSB'


@myapp.errorhandler(LibraryException)
def handle_custom_exception(error):
    response = {
        'error': str(error),
        'status_code': error.http_status
    }
    return jsonify(response), 500


if __name__ == '__main__':
    myapp.run()
