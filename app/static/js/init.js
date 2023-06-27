$('.ui.dropdown').dropdown();

$('.message .close').on('click', function() {
    $('.message').hide();
});

//$('.ui.sticky').sticky({
//    context: '#example1'
//});

$.ajax({
    method: 'GET',
    url: '/get_itens/',
    success: function (resposta) {
        let itens = '';
        let itens2 = '';
        let itens3 = '';
        for(let i = 0; i < resposta.length; i++){
            itens += '<div class="item" data-value="' + resposta[i] + '">' + resposta[i].toUpperCase() + '</div>';
            itens2 += '<option class="item" value="' + resposta[i] + '">';
            itens3 += '<tr><td>' + resposta[i].toUpperCase() + '</td><td id="' + resposta[i] + '"></td></tr>';
        }
        $("#menu_item").html(itens);
        $("#menu_value1").html(itens2);
        $("#menu_value2").html(itens2);
        $("#itens_block").html(itens3);
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

$('#btnRealizarAcao').click(function () {
    let action = $('#action').val()
    if(action == "write_item") {
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

        if(action == "write_item"){
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
                result = resultado['result']
                console.log(result)

                $("#log").val($("#log").val() + "\n" + result['text'])

                if(result['value'] == true){
                    $('#log' + transaction).append(action + '(' + item.toUpperCase() +');\n' + calculo)
                    if(action == 'read_lock' || action == 'write_lock' || action == 'unlock')
                        update_locks();
                }

            },
        });
    } else
        $('#erro').show();

};

function update_locks () {

    $.ajax({
            method: 'POST',
            url: '/get_locks/',
            success: function (resposta) {
                for(i in resposta) {
                    r = resposta[i]
                    console.log(r[3]);
                    $('#' + r[0]).html(""+ r[3])
                }
            },
        });

}

$('#btnResolverImpasse').click(function () {

    $.ajax({
            method: 'POST',
            url: '/solve_errors/',
//            data: { 'transaction': transaction, 'action': action, 'item': item, 'value1': value1, 'operator': operator, 'value2': value2},
            success: function (resposta) {
//                let resultado = JSON.parse(resposta)

            },
        });

});

$('#btnRegistro').click(function () {

    $.ajax({
            method: 'POST',
            url: '/get_complete_locks/',
            success: function (resposta) {
//                let resultado = JSON.parse(resposta)
                  console.log(resposta);

                  let complete_locks = '';
                  for(i in resposta){
                    r = resposta[i];
                    complete_locks += '<tr><td>' + r[4].toUpperCase() + '</td><td>' + r[3] + '</td><td>' + r[1].toUpperCase()
                    + '</td><td>' + r[0].toUpperCase() + '</td></tr>';
                  }

                  $('#complete_locks').html(complete_locks);
                  $('#modal_complete_locks').modal('show');
            },
        });

});