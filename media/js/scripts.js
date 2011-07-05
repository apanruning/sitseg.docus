$('document').ready(function(){
    $('.column_form :input').change(function(){
        $(this).parent('form').submit();
    })
})
