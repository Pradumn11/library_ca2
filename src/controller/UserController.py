from flask import render_template, redirect, request, url_for, session, Blueprint, jsonify
from src.service.UserService import UserService
from src.service.IssuerService import IssuerService
from src.exceptions.LibraryException import LibraryException
from src.models.User import User
from src.utils.libraryUtils import *

user_service = UserService()

user_controller = Blueprint('user', __name__)
issue_service = IssuerService()

@user_controller.route('/', methods=["POST", "GET"])
@user_controller.route("/login", methods=["POST", "GET"])
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
@login_required
def dashboard():
    if 'user_id' in session:
        try:

            user_id = int(session['user_id'])
            user_detail = user_service.get_user_by_id(user_id)
            issued_details = issue_service.getAllIssuedBooksForUser(user_id)

            if user_detail is not None:
                if user_detail['role'] == 'ADMIN':
                    return render_template('dashboard.html', user_id=session.get('user_id'))
                return render_template('userDashboard.html', userdetail=user_detail, issuers=issued_details)

        except LibraryException as e:
            return render_template('login.html', error=str(e))

    else:
        return render_template('login.html')


@user_controller.route("/user/getAllUsers")
@login_required
def get_all_users():
    offset = int(request.args.get('offset', 0))
    users = user_service.get_all_users(offset, 10)

    return render_template('user.html', users=users, user_id=session.get('user_id'))


@user_controller.route("/user/addUser", methods=['POST'])
def addUser():
    user_data = request.json
    user = User(
        first_name=user_data.get('firstName'),
        last_name=user_data.get('lastName'),
        username=user_data.get('userName'),
        password=user_data.get('password'),
        email=user_data.get('email'),
        contact=user_data.get('contact'),
        active=user_data.get('active'),
        role=user_data.get('role')
    )
    user.validate()
    user_service.add_user(user)
    return jsonify({"message": "User added successfully"})


@user_controller.route("/user/removeUser/<int:user_id>", methods=['DELETE'])
def removeUser(user_id):
    user_service.remove_user(user_id)
    return jsonify({"message": "User deleted successfully"})


@user_controller.route('/user/updateUser', methods=['PUT'])
def updateUser():
    user_data = request.json
    user = User(
        user_id=user_data.get("userId"),
        first_name=user_data.get("firstName"),
        last_name=user_data.get("lastName"),
        username=user_data.get("userName"),
        password=user_data.get("password"),
        email=user_data.get("email"),
        contact=user_data.get("contact"),
        active=user_data.get("active"),
        role=user_data.get("role"),
    )
    user.validate()
    user_service.update_user(user)
    return jsonify({"message": "User updated successfully"})


@user_controller.route("/user/getUserById/<int:user_id>")
def get_user_bu_id(user_id):
    return user_service.get_user_by_id(user_id)


@user_controller.route("/user/searchUser")
def searchUsers():
    offset = request.args.get('offset', 0)
    value = request.args.get('value', None)
    value = value.strip()

    if value == '""' or value is None:
        return user_service.get_all_users(0, 10)

    return user_service.searchUsers(value, offset)


@user_controller.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.user_login'))
