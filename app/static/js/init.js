$('.ui.dropdown')
  .dropdown()
;

$('#btnRealizarAcao').click(function () {

    let transaction = $('#transaction').val()
    let action = $('#action').val()
    let item = $('#item').val()

    $.ajax({
        method: 'POST',
        url: '/action/',
        data: { 'transaction': transaction, 'action': action, 'item': item},
        success: function (resposta) {
            let resultado = JSON.parse(resposta)
            console.log(resultado['result'])
            $("#log").val($("#log").val() + "\n" + resultado['result'])
        },
    });

})