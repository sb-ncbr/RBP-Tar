function reenable() {
    $('#reset').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#submit_spinner').hide();
}

$(document).ready(function () {
    $('#submit_spinner').hide();
    $('#reset').on('click', function () {
        $('#results').DataTable().clear().draw();
    });

    let table = $('#results').DataTable({
        dom: 'frtipB',
        searching: false,
        scrollX: true,
        scrollY: true,
        columnDefs: [
            {
                targets: [1, 2],
                className: 'dt-body-right'
            }
        ],
        buttons: [{
            extend: 'csvHtml5',
            text: 'Download results (CSV)',
            }
        ]
    });

    $('#search').submit(function (e) {
        e.preventDefault();
        let form = $(this);
        table.ajax.url('/get_results?' + form.serialize()).load(reenable);
        $('#reset').prop('disabled', true);
        $('#submit').prop('disabled', true);
        $('#submit_spinner').show();
    });
});
