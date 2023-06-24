$('.ui.dropdown').dropdown();

$('.ui.sticky').sticky({
    context: '#example1'
});

$('#progresso').progress({
    total: 3
});

$('.message .close').on('click', function() {
    $('.message').hide();
});

$.ajax({
    method: 'GET',
    url: '/get_itens/',
    success: function (resposta) {
        let itens = ''
        for(let i = 0; i < resposta.length; i++){
            itens += '<div class="item" data-value="' + resposta[i] + '">' + resposta[i].toUpperCase() + '</div>'
        }
        $("#menu_item").html(itens)
        $("#menu_value1").html(itens)
        $("#menu_value2").html(itens)
    },
});

//$.ajax({
//    method: 'GET',
//    url: '/get_transaction/',
//    success: function (resposta) {
//        console.log(resposta)
//        let itens = ''
//        for(let i = 0; i < resposta.length; i++){
//            itens += '<div class="item" data-value="' + resposta[i] + '">' + resposta[i].toUpperCase() + '</div>'
//            $('#coluna').append('<th>'+ result.toUpperCase() + '</th>')
//            $('#linha').append('<td><textarea id="log' + result +'" readonly></textarea></td>')
//        }
//        $("#menu_transaction").html(itens)
//    },
//});

$('#new_transaction').click(function () {
    $.ajax({
        method: 'POST',
        url: '/new_transaction/',
        success: function (resposta) {
            let resultado = JSON.parse(resposta)
            console.log(resultado['result'])
            let result = resultado['result'];
            $('#name_new_transation').html(result.toUpperCase());
            $('#sucesso').show();
            $('#menu_transaction').append('<div class="item" data-value="' + result + '">' + result.toUpperCase() + '</div>')
            $('#coluna').append('<th>'+ result.toUpperCase() + '</th>')
            $('#linha').append('<td><textarea id="log' + result +'" readonly></textarea></td>')
        },
    });
});

function validate_fields(){
    let action = $('#action').val()
    if($('#transaction').val() == '')
        return false;
    else if(action == '')
        return false;
    else if($('#item').val() == '')
        return false;
    else if(action == "write_item"){
        if($('#value1').val().trim() == '')
            return false;
        else if($('#operator').val() == '')
            return false;
        else if($('#value2').val().trim() == '')
            return false;
    }
    return true;
}

$('#btnAdicionarAcao').click(function () {

    if(validate_fields()){
        $('.message').hide();
        let transaction = $('#transaction').val().toUpperCase();
        let action = $('#action').val().toUpperCase();
        let item = $('#item').val().toUpperCase();

        $('#fila').append('<tr><td>' + transaction + '</td><td>' + action + '(' + item + ')</td></tr>')

    }

});

$('#btnIniciar').click(function () {
    let action = $('#action').val()
    if(action == 'write_item') {
        $('#selected_item').val($('#item').val().toUpperCase());
        $('#value1').val('');
        $('#operator').val('');
        $('#value2').val('');
        $('#value_item').modal('show');
    }
    else
        active_action();
});

$('#btnCheck').click(function () {
    active_action();
});

function active_action () {

    if(validate_fields()){
        $('.message').hide();
        let transaction = $('#transaction').val();
        let action = $('#action').val();
        let item = $('#item').val();
        let value1 = 0;
        let operator = 0;
        let value2 = 0;
        let calculo = '';

        if(action == 'write_item'){
            value1 = $('#value1').val();
            operator = $('#operator').val();
            value2 = $('#value2').val();
            calculo = item.toUpperCase() + ' = ' + value1 + ' ' + operator + ' ' + value2 + ' ;\n';
        }

        $.ajax({
            method: 'POST',
            url: '/action/',
            data: { 'transaction': transaction, 'action': action, 'item': item, 'value1': value1, 'operator': operator, 'value2': value2},
            success: function (resposta) {
                let resultado = JSON.parse(resposta)
                console.log(resultado['result'])
                $("#log").val($("#log").val() + "\n" + resultado['result'])

                $('#log' + transaction).append(action + '(' + item.toUpperCase() +');\n' + calculo)
            },
        });
    } else
        $('#erro').show();

};