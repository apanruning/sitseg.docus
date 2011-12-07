$('document').ready(function(){
    function column_form_change(){
        form = $(this).parents('form');
        data = $(form).serializeArray();
        target = $(form).attr('action');
        $.post(
            target, 
            data, 
            function(response){
                data_column = $(form).parent('.data_column ');
                data_column = $(data_column).replaceWith(response);
            }
        );
    }
    $('.column_form :input').live('change', column_form_change)
    $('.control').live('click',function(){
        target = $(this).attr('href');
        $(this).toggleClass('active');
        $(target).toggle('fade', 300);
        return false;
        
    });
    $('form input[type="text"]:first').focus()
    $('input[type="file"]').change(function(){
        value = $(this).val();
        value = value.split('\\').reverse()[0];
        $('#id_name').val(value);
        
    });
    $('#import_form').submit(function(){
        target = $(this).attr('action');
        data = $('.column_form').serializeArray();
        message = $('<li>').append($('<strong>').text('Los datos se están procesando'));
        $('#messages').append(message);
        $.post(
            target, 
            data, 
            function(response){
                $('#messages li').remove();
                $('#messages').append(response);
                window.setTimeout(function(){
                    $('#messages .control').click()
                }, 3000);
            }
        );

        return false;
    })
    window.setTimeout(function(){
        $('#messages .control').click()
    }, 3000);
    $('.pjax').click(function(){
        $('#ajax-container').remove();
        target = $(this).attr('href');
        container = $(this).parents('li');
        $.get(
            target,
            function(data){
                wrapper = $('<div">').attr('id','ajax-container').append(data);
                $(container).append(wrapper).effect('highlight', {}, 2000);
            }
        
        );
        return false;
        
        
    })
    $('#accordion').accordion();    
})
