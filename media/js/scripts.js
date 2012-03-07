function pjax(){
    event.preventDefault();
    container = $(this).attr('rel'),
    target = $(this).attr('href');
    $.get(
        target,
        function(data){
            $(container).empty();
            $(container).append(data);
        }
    
    );
}
function collapsable(){
    $(this).off('click');
    $('.expanded').toggle('blind').toggleClass('expanded')
    $('.active').toggleClass('active');
    container = $(this).attr('rel'),
    target = $(this).attr('href');
    $(this).toggleClass('active');
    $(container).toggleClass('expanded');
    $(container).toggle('blind');
    return false;
}
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

$(function(){
    $('body').on('ajaxComplete', function(){
        $(this).find('.tabs').tabs();
    });
    $('.tabs').tabs();

    $('body').on('change', '.column_form :input', column_form_change);
    $('body').on('click', '.control',function(){
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
    
    $('body').on('submit', '.import_form', function(){
        target = $(this).attr('action');
        container = $(this).parents('div');
        data = $(container).find('.column_form').serializeArray();
        message = $('<li>').append($('<strong>').text('Los datos se están procesando'));
        $('#messages').append(message);
        $.post(
            target, 
            data,
            function(response, status){
                $('#messages li').remove();
                $('#messages').append(response);
                window.setTimeout(function(){
                    $('#messages .control').click()
                }, 3000);
            }
        );

        return false;
    });
    $('.graph-select>li a ').on('click', function(){
        $('.selected').toggleClass('selected');
        $(this).parents('li').toggleClass('selected');
    });

//    TODO: Tratar de darle tab-focus a la primera pestaña
//    TODO: Asignar eventos de teclado
//    $('body').on('tabscreate', function(event, ui){
//        console.log(event, ui)
//    })    
   
    $('body').on('click.pjax', '.pjax', pjax)
    
    $('body').on('click.collapsable','.collapsable', collapsable)
    
   

     window.setTimeout(function(){
        $('#messages .control').click()
    }, 3000);
});
