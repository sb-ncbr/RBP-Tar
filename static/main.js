function reenable() {
    $('#reset').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#submit_spinner').hide();
}

$(document).ready(function () {
    $('#submit_spinner').hide();

    $('#example1').on('click', function () {
        $('#reset').trigger('click');
        $('#chromosome').val('chr16');
        $('#start_min').val(31180139);
        $('#end_max').val(31191605);
        $('#strand').val('+');
    });

    $('#example2').on('click', function () {
        $('#example1').trigger('click');
        $('#protein_name').val('FUS');
    });

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
