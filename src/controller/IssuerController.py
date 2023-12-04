from flask import Blueprint, request, jsonify, render_template

from src.models.Issuer import Issuer
from src.service.IssuerService import IssuerService
from src.utils.libraryUtils import login_required

issuer_service = IssuerService()

issuer_controller = Blueprint('issuer', __name__)


@issuer_controller.route("/issueBook", methods=["POST"])
def issue_Book():
    issuer_data = request.json
    issuer = Issuer(
        book_id=issuer_data.get('bookId'),
        user_id=issuer_data.get('userId'),
        active=True,
        days=int(issuer_data.get('days'))
    )
    issuer_service.addIssue(issuer)
    return jsonify({"message": "Book Issue successfully"})


@issuer_controller.route("/returnBook", methods=["PUT"])
def return_Book():
    issuer_id = request.args.get("issuerId", type=int)
    issuer_service.returnIssuedBook(issuer_id)
    return jsonify({"message": "Book Return successfully"})


@login_required
@issuer_controller.route("/getAllIssuedBooks")
def get_Issued_Books():
    offset = int(request.args.get('offset', 0))
    issuers = issuer_service.get_All_Issued_Books()
    print(issuers)
    return render_template('issuer.html', issuers=issuers)


@issuer_controller.route("/returnDue", methods=["PUT"])
def return_due():
    user_id = request.args.get("userId", type=int)
    dueReturned = request.args.get("dueReturned", type=int)
    issuer_service.returnDue(dueReturned, user_id)
    return jsonify({"message": "Due Return successfully"})


@issuer_controller.route("/searchIssuer")
def searchIssuers():
    offset = request.args.get('offset', 0)
    value = request.args.get('value', None)
    value=value.strip()

    if value == '""' or value is None:
        return issuer_service.get_All_Issued_Books()

    return issuer_service.search_Issuers(value, offset)