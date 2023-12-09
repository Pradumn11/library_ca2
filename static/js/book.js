
document.getElementById('addBookBtn').addEventListener('click', function () {
            $('#addBookForm').find('input, select').val('');
            $('#addBookForm').attr('data-mode', 'add');
            $('#addBookModal').modal('show');
        });
function getBookObj(){

     let formData ={}
     formData['title'] = $("#title").val();
     formData['authorName']=$("#authorName").val();
     formData['category']=$("#category").val();
     formData['available']=$("#available").val();
     formData['totalQuantity']=$("#totalQuantity").val();
     formData['libSection']=$("#libSection").val();
     formData['active']=true;
     return formData;
}

$(document).ready(function() {
$('#addBookForm :input').attr('required', true);


    $('#addBookForm').submit(function(event) {
        event.preventDefault();
        let formDataObj=getBookObj();

        let mode = $('#addBookForm').data('mode');
        let endpoint="";
        let method="";

        if(mode=='add'){
            endpoint='/book/addBook';
            method='POST'
        }else if(mode=='edit'){
            let book_Id = $('#addBookForm').data('id');
            formDataObj['bookId']=book_Id;
            endpoint='/book/updateBook';
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
          return response.json().then((data) => {
            if (data.error_code == "IVD_OPN") throw new Error(data.error);
            throw new Error(data.error);
          });
            }
            return response.json();
        })
        .then(data => {
       $("#addBookModal").modal("hide");
      if (data.message) {
          showAlert(data.message, "/book/getAllBooks");
        }
      })
        .catch(error => {
        displayCommonError(error,"commonFormError");
      });
  });


$('#bookTable').on('click', '#editBtn', function() {
        $('#addBookForm').attr('data-mode', 'edit');

        var bookId = $(this).data('id');
        $('#addBookForm').attr('data-id', bookId);
        fetch('/book/getBookById/'+bookId, {
            method: 'GET',
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
            .then(bookData => {

                $('#title').val(bookData.title);
                $('#authorName').val(bookData.author_name);
                $('#category').val(bookData.category);
                $('#available').val(bookData.available);
                $('#totalQuantity').val(bookData.total_quantity);
                $('#libSection').val(bookData.lib_section);

                $('#addBookModal').modal('show');
            })
      .catch((error) => {
         showAlert(error, null);
      });
  });

$('#bookTable').on('click', '#deleteBtn', function() {
    var bookId = $(this).data('id');
          fetch('/book/deleteBook/'+bookId, {
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
       .then((data) => {

        if (data.message) {
          showAlert(data.message, "/book/getAllBooks");
        }
      })
      .catch(error => {

        showAlert(error, null);
      });
  });

$('#bookTable').on('click', '#reserveBtn', function() {

    $('#issuerForm').find('input, select').val('');
    var bookTitle = $(this).data('title');
    var bookId = $(this).data('id');
    $('#issuerForm').data('id', bookId);
    $('#reserveModalLabel').text('Reserve Book: ' + bookTitle);
    $('#issuerModal').modal('show');

});

$('#issuerForm').submit(function(event) {
        event.preventDefault();
        let bookId=$(this).data('id');
        let days = $('#issueDays').val();
        let userId=$('#userId').val();

        let formDataObj = {};
        formDataObj['days']=days;
        formDataObj['bookId']=bookId;
        formDataObj['userId']=userId;

        fetch('/issue/issueBook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formDataObj),
        })
        .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.error);
          });
        }
            return response.json();
      })
      .then((data) => {
      if (data.message) {
      $('#issuerModal').modal('hide');
          showAlert(data.message, "/book/getAllBooks");
        }
      })
      .catch((error) => {
      $('#issuerModal').modal('hide');
        showAlert(error, null);
      });

  });


$('#bookSearch').on('input', function() {

    var searchValue = $(this).val();

    var apiUrl = '/book/searchBook?value=' + searchValue;


    fetch(apiUrl)
        .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.error);
          });
        }
        return response.json();
      })
      .then(data => {

            $('#bookTable tbody').empty();
            data.forEach(book => {
                var row = `<tr>
                <td>${book.book_id}</td>
                <td>${book.title}</td>
                <td>${book.author_name}</td>
                <td>${book.category}</td>
                <td>${book.available}</td>
                <td>${book.lib_section}</td>
                <td>${book.active ? 'ACTIVE' : 'INACTIVE'}</td>
                <td>
                    <button type="button" id="deleteBtn" data-id="${book.book_id}" class="btn btn-danger">Delete</button>
                    <button type="button" id="editBtn" data-id="${book.book_id}" class="btn btn-primary">Edit</button>
                    <button type="button" id="reserveBtn" data-id="${book.book_id}" data-title="${book.title}" class="btn btn-success">Issue Book</button>
                </td>
            </tr>`;

          $("#bookTable tbody").append(row);
        });
      })
      .catch((error) => {
        showAlert(error, null);
      });
  });
  $('#addBookModal').on('hide.bs.modal', function () {
            clearCommonError('commonFormError');
  });
  removeCommonErrorListeners("#addBookForm", "commonFormError");
});