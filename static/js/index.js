$(document).ready(function () {
  var inputElements = $('input[type="text"], input[type="password"]');

  var errormsg = $(".login_error");

  inputElements.focus(function () {
    errormsg.css("display", "none");
  });


  $('#resetButton').on('click', function() {
            $('#resetPasswordModal').modal('show');
  });

  $('#resetPasswordForm').submit(function(event) {
        event.preventDefault();

        let formData ={}
        formData['userName']=$("#usernamePass").val();
        formData['oldPassword']=$("#oldPassword").val();
        formData['newPassword']=$("#newpassword").val();


    });




});

