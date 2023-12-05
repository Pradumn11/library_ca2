
document.getElementById('addUserBtn').addEventListener('click', function () {
            $('#addUserForm').find('input, select').val('');
            $('#addUsserForm').attr('data-mode', 'add');
            $('#addUserModal').modal('show');
        });

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

$(document).ready(function() {
$('#addUserForm :input').attr('required', true);
 $('#addUserForm').submit(function(event) {
        event.preventDefault();
        let formDataObj=getUserObj();

        let mode = $('#addUserForm').data('mode');
        let endpoint="";
        let method="";


        if(mode=='add'){
            endpoint='/user/addUser';
            method='POST'

        }else if(mode=='edit'){
            let user_Id = $('#addUserForm').data('id');
            formDataObj['userId']=user_Id;
            endpoint='/user/updateUser';
            method='PUT'

        }

        fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formDataObj),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
//                        if (data.error_code=="ALD_EXISTS")
                                 throw new Error(data.error);
                        });
                 }
            return response.json();
        })
        .then(data => {
        $("#addUserModal").modal("hide");
           if (data.message) {
          showAlert(data.message, "/user/getAllUsers");
        }
        })
        .catch(error => {

            if (error.message) {
          displayCommonError(error.message);
                }
        });
    });

    $('#userTable').on('click', '#deleteBtn', function() {
        var userId = $(this).data('id');

              fetch('/user/removeUser/'+ userId, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) {
           return response.json().then((data) => {
            throw new Error(data.error);
           });
                }
                return response.json();
            })
            .then(data => {
        if (data.message) {
          showAlert(data.message, "/user/getAllUsers");
        }
      })
      .catch((error) => {
        showAlert(error, null);
      });
  });


$('#userTable').on('click', '#editBtn', function() {
        $('#addUserForm').attr('data-mode', 'edit');

        var userId = $(this).data('id');
        $('#addUserForm').attr('data-id', userId);
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


                $('#addUserModal').modal('show');
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });


$('#userSearch').on('input', function() {
    var searchValue = $(this).val();

    var apiUrl = '/user/searchUser?value=' + searchValue;


    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {

            $('#userTable tbody').empty();
            data.forEach(user => {
                var row = `
    <tr>
        <td>${user.user_id}</td>
        <td>${user.firstname} ${user.lastname}</td>
        <td>${user.username}</td>
        <td>${user.email}</td>
        <td>${user.contact}</td>
        <td>${user.role}</td>
        <td>${user.active ? 'ACTIVE' : 'INACTIVE'}</td>
        <td>
            <button type="button" id="deleteBtn" data-id="${user.user_id}" class="btn btn-danger">Delete</button>
            <button type="button" id="editBtn" data-id="${user.user_id}" class="btn btn-primary">Edit</button>
             ${user.due > 0 ? `<button type="button" id="returnDueBtn" data-id="${user.user_id}" class="btn btn-success">Pay Due</button>` : ''}
        </td>
    </tr>
`;

                $('#userTable tbody').append(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});


$('#userTable').on('click', '#returnDueBtn', function() {

var userId = $(this).data('id');


    fetch('/user/getUserById/' + userId, {
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

        var perDayFine = 10;
        var dueDays = userData.due;
        var amountToPay = dueDays * perDayFine;


        $('#dueInfo').text(`You have ${dueDays} days of due. The total amount to pay is €${amountToPay}. How many days do you want to pay?`);
        $('#dueDaysInput').val(dueDays);

        $("#payDueModal").modal("show");
      });

        // Handle submit button click
        $('#submitDueBtn').on('click', function () {
            var daysToPay = $('#dueDaysInput').val();
            fetch(`/issue/returnDue?userId=${userId}&dueReturned=${daysToPay}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
         if (!response.ok) {
          return response.json().then((data) => {
            if (data.error_code == "IVD_OPN") throw new Error(data.error);
          });
        }
        })
        .then((data) => {
        if (data.message) {
          showAlert(data.message, "/user/getAllUsers");
        }
        })
        .catch((error) => {
          if (error) {
            displayCommonError(error,"commonDueError");
          }
        });
});
   });

$('#addUserModal').on('hide.bs.modal', function () {
            clearCommonError('commonFormError');
  });
removeCommonErrorListeners("#addUserForm", "commonFormError");
removeCommonErrorListeners("#payDueModal", "commonDueError");

});


