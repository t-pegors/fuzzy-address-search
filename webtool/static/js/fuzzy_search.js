
$(document).ready(function (e) {

    /////////////////
    // FILE UPLOAD //
    /////////////////

    $('#file_upload').on('click', function () {

        var form_data = new FormData();
        var ins = document.getElementById('formFile').files.length;

        if(ins == 0) {

            $('#msg').html('<span style="color:red">Select at least one file</span>');
            return;
        } else {

            $('#msg').html('Upload in progress...');
            $('#div_file_progress_bar').attr('hidden', false);

            // add filename to form_data object
            form_data.append("input_file", document.getElementById('formFile').files[0])

            $.ajax({
                url: '/_upload_file',
                dataType: 'json',
                cache: false,
                contentType: false,
                processData: false,
                data: form_data,
                type: 'POST',
                success: function (response) {

                    $('#msg').html(response['message']);
                    $('#div_file_progress_bar').attr('hidden', true);

                    // populate the column dropdown in Step 2
                    $('#column_dropdown').attr('disabled', false);
                    $('#column_dropdown').empty();
                    $(column_dropdown).append('<option selected="true" disabled>Choose a column...</option>');
                    $.each(JSON.parse(response['columns']), function(index, item) {
                        $('#column_dropdown').append($('<option></option>').text(item));
                    });

                },
                error: function(response) {
                    $('#msg').html(response['message']);
                    $('#div_file_progress_bar').attr('hidden', true);
                }
            });
        };
    });

    $('#column_dropdown').change(function() {
        $('#vocab_go').removeClass('btn-warning');
        $('#vocab_go').addClass('btn-success');
        $('#vocab_go').attr('disabled', false);
    });

    /////////////////
    // BUILD VOCAB //
    /////////////////

    $('#vocab_go').on('click', function() {

        $('#div_vocab_progress_bar').attr('hidden', false);
        $('#build_msg').html('Build in progress');
        column = $('#column_dropdown :selected').text()

        $.ajax({
            url: '/_build_vocab',
            data: {column: $('#column_dropdown :selected').text()},
            type: 'POST',
            success: function (response) {

              $('#div_vocab_progress_bar').attr('hidden', true);
              $('#build_msg').html(response['message']);
              $('#addresses').attr('disabled', false)

            },
            error: function (response) {

                $('#div_vocab_progress_bar').attr('hidden', false);
                $('#build_msg').html(response['message']);
            }
        })
    });

    ////////////////////
    // ADDRESS LIST ////
    ////////////////////

    $("#addresses").on("input propertychange paste", (function() {

        query_list = [];

        // create an array from each row of the textbox (determined by newline)
        var lines = $('#addresses').val().split(/\n/);
        for (var i=0; i < lines.length; i++) {
            if (/\S/.test(lines[i])) {
                query_list.push($.trim(lines[i]))
            }
        }

        if (query_list.length > 0) {

            query_length = query_list.length;
            $('#num_rows').html(query_length + " addresses to search.");
            $('#threshold').attr('disabled', false);

        } else {

            query_length = 0;
            $('#num_rows').html("0 addresses to search.");
        };

    }));

    $('#threshold').on("input propertychange", function() {
        $('#search').attr('disabled', false);
        $('#search').removeClass('btn-warning');
        $('#search').addClass('btn-success');
    });

    ////////////////////
    // ADDRESS LIST ////
    ////////////////////

    $('#search').on('click', function() {

        $('#div_search_progress_bar').attr('hidden', false);
        $('search_msg').html('');

        // record table
        threshold = $('#threshold').val();

        $.getJSON('/_search', {
            address: JSON.stringify(query_list),
            threshold: threshold
            })
        .done(function(data) {

            $('#search_msg').html('Search success.');

            var columns = [];
            columnNames = Object.keys(data[0]);
            for (var i in columnNames) {
                columns.push({data: columnNames[i],
                              title: columnNames[i]})
            }

            if ($.fn.DataTable.isDataTable('#fuzzy_address_table')) {
                $('#fuzzy_address_table').DataTable().clear().destroy()
                $('#fuzzy_address_table').empty()
            }

            $('#div_search_progress_bar').attr('hidden', true);

            // defin the table
            table = $('#fuzzy_address_table').DataTable({
                data: data,
                columns: columns,
                pageLength: 20,
                //colReorder: true,
                order: [0, "desc"],
                //scrollY: 500,
                //scrollX: true,
                //responsive: true,
                dom: 'Bfrtip',
                buttons: ['copy', {
                    extend: 'csv',
                    text: 'CSV',
                    extension: '.csv',
                    title: 'fuzzy_address_results',
                    exportOptions: {
                        modifier: {
                            page: 'all',
                            search: 'none',
                        }
                    }
                }]
            });
        })
        .fail(function() {
            $('#div_search_progress_bar').attr('hidden', true);

            $('#search_msg').html('No results found.');

            if ($.fn.DataTable.isDataTable('#fuzzy_address_table')) {
                $('#fuzzy_address_table').DataTable().clear().destroy();
                $('#fuzzy_address_table').empty()
            }
        })
        return false;
    })


});



