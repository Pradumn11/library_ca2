$(document).ready(function() {

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
                    throw new Error(`HTTP error! Status: ${response.status}`);
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
                    `<button type="button" id="returnBtn" data-id=${issuer.issuer_id} class="btn btn-danger">Return</button>`)+
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