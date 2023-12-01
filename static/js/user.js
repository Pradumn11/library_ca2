
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

function showNotification(message, type) {

    var notification = document.createElement('div');
    notification.className = `alert alert-${type} mt-3`;
    notification.textContent = message;
    alert(message);
    document.body.appendChild(notification);


    setTimeout(function () {
        notification.style.display = 'none';
    }, 5000);
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
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
        console.log("thendata")
            window.location.href = '/user/getAllUsers';
//            showNotification(data.body, 'success');
        })
        .catch(error => {
//            showNotification(error.error, 'error');
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
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {

            window.location.href = '/user/getAllUsers';
            showNotification(data['message'], 'success');
        })
        .catch(error => {
            showNotification(error.error, 'error');
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
                var row = '<tr>' +
                    '<td>' + user.user_id + '</td>' +
                    '<td>' + user.firstname + ' ' + user.lastname + '</td>' +
                    '<td>' + user.username + '</td>' +
                    '<td>' + user.email + '</td>' +
                    '<td>' + user.contact + '</td>' +
                    '<td>' + user.role + '</td>' +
                    '<td>' + (user.active ? 'ACTIVE' : 'INACTIVE') + '</td>' +
                    '<td>' +
                    '<button type="button" class="btn btn-danger">Delete</button>' +
                    '<button type="button" class="btn btn-primary">Edit</button>' +
                    '</td>' +
                    '</tr>';

                $('#userTable tbody').append(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

});