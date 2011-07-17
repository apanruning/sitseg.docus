$('document').ready(function(){
    $('.column_form :input').change(function(){
        form = $(this).parent('form');
        data = $(form).serializeArray();
        target = $(form).attr('action');
        $.post(
            target, 
            data, 
            function(json){
                data_column = $(form).parent('.data_column ');

                $(data_column).replaceWith(json);
                object_id = $(json).find('input[name="object_id"]').val();
                is_available = $(json).find('input[name="is_available"]').attr('checked');
                if (is_available && $('#import_form').has('input[value="'+object_id+'"]').length === 0){
                    $(json).find('input[name="object_id"]').insertBefore('#import_form input');
                }
                if ( !(is_available) && $('#import_form').has('input[value="'+object_id+'"]').length <=1 ){
                    $('#import_form input[value="'+object_id+'"]').remove();
                }
            }
        );
        

    })
})
