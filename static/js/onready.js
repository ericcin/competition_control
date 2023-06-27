function trimTextAreas() {
    $('textarea').each(function () {
        var trimmedValue = $(this).val().trim();
        $(this).val(trimmedValue);
    });
}

function validateDataItemList(dataItemList, place) {
    let result = false;
    try {
        const parsedData = JSON.parse(dataItemList);
        if (Array.isArray(parsedData) && parsedData.every(item => typeof item === 'string')) {
            result = [true, parsedData, checkType(parsedData, 'dataItemList', place)];
        }
    } catch (error) {
        timePrint(error, place, 'dataItemList');
        timePrint('Invalid format.', place, 'dataItemList');
    }
    return result;
}

function onReady() {

    listDataItems();
    listTransactions();
    listLocks();
    trimTextAreas();

    // Validar lista de data items na text area
    $('#dataItemText').change(function () {
        trimTextAreas();
        const trimmedValue = $('#dataItemText').val().trim();
        $('#dataItemText').val(trimmedValue);
        const isValid = validateDataItemList($('#dataItemText').val(), 'dataItemText change')[0];
        timePrint(isValid)
        $('#setDataItemsButton').prop('disabled', !isValid);
        dataItemValidationMessage.textContent = "";
        if (!isValid) {
            dataItemValidationMessage.textContent = 'Lista de itens de dados em um formato inválido. Use um array JavaScript ou lista Python.';
        }
    });

    // Validar transação na text area
    $('#transactionText').change(function () {
        trimTextAreas();
    });

    // Ler data items - provavelmente será eliminada
    $('#readDataItemButton').click(listDataItems);

    // Setar data items
    $('#setDataItemsButton').click(setDataItems);

    // Inserir transação
    $('#insertTransactionButton').click(insertTransaction);

    // Step Into
    $('#stepIntoTransactionButton').click(stepInto);
}
$(document).ready(onReady);