function getUserObj(){
     let formData ={}
     formData['firstName']=$("#firstName").val();
     formData['lastName']=$("#lastName").val();
     formData['userName']=$("#userName").val();
     formData['password']=$("#password").val();
     formData['email']=$("#email").val();
     formData['contact']=$("#contact").val();
     formData['role']=$("#role").val();
     formData['active']=true;

     return formData;
}


$('#editBtn').on('click', function() {


        var userId = $(this).data('id');

        fetch('/user/getUserById/'+userId, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(userData => {

                $('#firstName').val(userData.firstname);
                $('#lastName').val(userData.lastname);
                $('#userName').val(userData.username);
                $('#password').val(userData.password);
                $('#email').val(userData.email);
                $('#contact').val(userData.contact);
                $('#role').val(userData.role);

                $('#editUserModal').modal('show');
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

$('#editUserForm :input').attr('required', true);
 $('#editUserForm').submit(function(event) {
        event.preventDefault();
        let formDataObj=getUserObj();

            let user_Id = $('#editUserForm').data('id');
            formDataObj['userId']=user_Id;

        fetch('/user/updateUser', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formDataObj),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                                 throw new Error(data.error);
                        });
                 }
            return response.json();
        })
        .then((data) => {
        $("#editUserModal").modal("hide");
        if (data.message) {
          showAlert(data.message, "/dashboard");
        }
        })
        .catch(error => {
            if (error.message) {
          displayCommonError(error.message);
                }
        });
    });

$('#searchIssuer').on('input', function() {

    var searchValue = $(this).val();


    var apiUrl = '/issue/searchIssuer?value=' + searchValue;


    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        $("#issuerTable tbody").empty();
        data.forEach((issuer) => {
          var row =`
    <tr>
        <td>${issuer.issuer_id}</td>
        <td>${issuer.book_id}</td>
        <td>${issuer.book_title}</td>
        <td>${issuer.issue_date}</td>
        <td>${issuer.return_date}</td>
        <td>${issuer.days} Days</td>
        <td>${issuer.due} Days</td>
        <td>${issuer.active ? 'ACTIVE' : 'RETURNED'}</td>

    </tr>
`;

                $('#issuerTable tbody').append(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            });
});
