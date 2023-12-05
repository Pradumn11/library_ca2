from flask import Flask, jsonify
from src.controller.UserController import user_controller
from src.controller.BookController import book_controller
from src.controller.IssuerController import issuer_controller
from src.exceptions.LibraryException import LibraryException


myapp = Flask(__name__)
myapp.static_url_path = '/static'
myapp.register_blueprint(user_controller)
myapp.register_blueprint(book_controller, url_prefix='/book')
myapp.register_blueprint(issuer_controller, url_prefix='/issue')
myapp.config['SECRET_KEY'] = 'ABSBSBSBBSBSBBSBSB'


@myapp.errorhandler(LibraryException)
def handle_custom_exception(error):
    response = {
        'error': str(error),
        'error_code': error.error_code,
        'status_code': error.http_status

    }
    return jsonify(response), error.http_status


if __name__ == '__main__':
    myapp.run()
