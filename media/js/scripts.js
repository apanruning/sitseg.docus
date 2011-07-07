$('document').ready(function(){
    $('.column_form :input').change(function(){
        form = $(this).parent('form');
        if ($(this).attr('name') ==='is_available') {
            selected_object_id = $(form).find('input[name="object_id"]');
            if ($('#import_form').has(selected_object_id)){
                console.log('has')
            };
        };
        $(form).submit();

    })
})
