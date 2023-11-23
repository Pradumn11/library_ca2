from flask import render_template, redirect, request, url_for, session, Blueprint, jsonify
from src.service.userService import UserService
from src.exceptions.LibraryException import LibraryException
from src.models.User import User

user_service = UserService()

user_controller = Blueprint('user', __name__)


@user_controller.route("/", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        userName = request.form.get('username')
        password = request.form.get('password')
        check = user_service.check_user_creds(userName, password)
        if isinstance(check, tuple):
            user, error = check
            if user is None:
                return render_template("login.html", error=error)
        else:
            user = check
            session['user_id'] = user[0]["user_id"]
            return redirect(url_for('user.dashboard'))
    return render_template("login.html")


@user_controller.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        try:

            user_id = int(session['user_id'])
            user_detail = user_service.get_user_by_id(user_id)

            if user_detail is not None:
                return render_template('dashboard.html', userdetail=user_detail)

        except LibraryException as e:
            return render_template('login.html', error=str(e))

    else:
        return render_template('login.html')


@user_controller.route("/getAllUsers")
def get_all_users():
    users = user_service.get_all_users()
    return jsonify(users)


@user_controller.route("/addUser", methods=['POST'])
def addUser():
    user_data = request.json
    user = User(
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        username=user_data.get('username'),
        password=user_data.get('password'),
        email=user_data.get('email'),
        contact=user_data.get('contact'),
        active=user_data.get('active'),
        role=user_data.get('role')
    )
    user_service.add_user(user)
    return jsonify({"message": "User added successfully"})


@user_controller.route("/removeUser/<int:user_id>", methods=['DELETE'])
def removeUser(user_id):
    user_service.remove_user(user_id)
    return jsonify({"message": "User deleted successfully"})

@user_controller.route('/updateBook', methods=['PUT'])
def updateUser():
    user_data = request.json
    user = User(
        user_id=user_data.get("user_id"),
        first_name=user_data.get("first_name"),
        last_name=user_data.get("last_name"),
        username=user_data.get("username"),
        password=user_data.get("password"),
        email=user_data.get("email"),
        contact=user_data.get("contact"),
        active=user_data.get("active"),
        role=user_data.get("role"),
    )
    user_service.update_user(user)
    return jsonify({"message": "User updated successfully"})


