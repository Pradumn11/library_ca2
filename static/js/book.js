[12:42 PM, 12/1/2023] Pradumn DBS InfoSystem: $(document).ready(function() {

$('#issuerTable').on('click', '#returnBtn', function() {
        var issuerId = $(this).data('id');
        console.log(issuerId);
              fetch('/issue/returnBook?issuerId='+issuerId, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(HTTP error! Status: ${response.status});
                }
                return response.json();
            })
            .then(data => {
                window.location.href = '/issue/getAllIssuedBooks';
            })
            .catch(error => {
                console.error('Error:', error);
            });

});

$('.form-control').on('input', function() {

    var searchValue = $(this).val();
    console.log(searchValue);

    var apiUrl = '/issue/searchIssuer?value=' + searchValue;


    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {

            $('#issuerTable tbody').empty();
            data.forEach(issuer => {
                var row = '<tr>' +
                    '<td>' + issuer.issuer_id + '</td>' +
                    '<td>' + issuer.user_id +'</td>' +
                    '<td>' + issuer.book_id + '</td>' +
                    '<td>' + issuer.fullname + '</td>' +
                    '<td>' + issuer.book_title + '</td>' +
                    '<td>' + issuer.issue_date + '</td>' +
                    '<td>' + issuer.return_date + '</td>' +
                    '<td>' + issuer.days + ' Days' + '</td>' +
                    '<td>' + issuer.due + ' Days' + '</td>' +
                    '<td>' + (issuer.active ? 'ACTIVE' : 'RETURNED') + '</td>' +
                    '<td>' +
                    (!issuer.active?'':
                    <button type="button" id="returnBtn" data-id=${issuer.issuer_id} class="btn btn-danger">Return</button>)+
                '</td>'+
                    '</td>' +
                    '</tr>';

                $('#issuerTable tbody').append(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
});
[12:42 PM, 12/1/2023] Pradumn DBS InfoSystem: document.getElementById('addBookBtn').addEventListener('click', function () {
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
            console.log(formDataObj);
            console.log(formDataObj['bookId']);
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
                throw new Error(HTTP error! Status: ${response.status});
            }
            return response.json();
        })
        .then(data => {
            window.location.href = '/book/getAllBooks';
        })
        .catch(error => {
            console.error('Error:', error);
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
                    throw new Error(HTTP error! Status: ${response.status});
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
            .catch(error => {
                console.error('Error:', error);
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
                throw new Error(HTTP error! Status: ${response.status});
            }
            return response.json();
        })
        .then(data => {
            window.location.href = '/book/getAllBooks';
        })
        .catch(error => {
            console.error('Error:', error);
        });

        });


$('#bookTable').on('click', '#reserveBtn', function() {

    $('#issuerForm').find('input, select').val('');
    var bookTitle = $(this).data('title');
    var bookId = $(this).data('id');
    $('#issuerForm').attr('data-id', bookId);
    $('#reserveModalLabel').text('Reserve Book: ' + bookTitle);
    $('#issuerModal').modal('show');

});

$('#issuerForm').submit(function(event) {
        event.preventDefault();
        let bookId=$(this).data('id');
        let days = $('#issueDays').val();
        let userId=$('#userId').val();

        console.log("Entered days:", days);
        console.log("Entered userId:", userId);
        console.log("Entered bookId:", bookId);
        let formDataObj={}

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
        .then(response => {
            if (!response.ok) {
                throw new Error(HTTP error! Status: ${response.status});
            }
            return response.json();
        })
        .then(data => {
            window.location.href = '/book/getAllBooks';
        })
        .catch(error => {
            console.error('Error:', error);
        });
//        $('#reserveModal').modal('hide');
    });


$('#bookSearch').on('input', function() {

    var searchValue = $(this).val();

    var apiUrl = '/book/searchBook?value=' + searchValue;


    fetch(apiUrl)
        .then(response => response.json())
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

                $('#bookTable tbody').append(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});


});