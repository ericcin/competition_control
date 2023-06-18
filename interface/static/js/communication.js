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

$(document).ready(function () {
  // Validar lista de data items na text area
  $('#dataItemText').change(function () {
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

  // Ler data items - provavelmente será eliminada
  $('#readDataItemButton').click(function () {
    var requestData = {
      method: 'list_data_items',
      message: '{}',
    }
    timePrint(requestData.message, '#readDataItemButton', 'message')
    checkType(requestData.message, "message", '#readDataItemButton');
    timePrint(requestData, '#readDataItemButton', 'requestData')
    checkType(requestData, "requestData", '#readDataItemButton');

    $.ajax({
      url: "http://127.0.0.1:5000/LockManager",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(requestData),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (data) {
        timePrint(data, '#readDataItemButton success', 'data');
        checkType(data, "data", '#readDataItemButton success');
        var jsonTable = jsonToHtmlTable(pythonListToJSON("Item de Dados", data));
        $('#dataItemTableContainer').empty().append(jsonTable);
      }
    });
  });

  // Setar data items
  $('#setDataItemsButton').click(function () {
    var requestData = {
      method: 'init',
      message: { data_items: eval($('#dataItemText').val()) },
    }
    timePrint(requestData.message, '#setDataItemsButton', 'message')
    checkType(requestData.message, "message", '#setDataItemsButton');
    timePrint(requestData, '#setDataItemsButton', 'requestData')
    checkType(requestData, "requestData", '#setDataItemsButton');

    $.ajax({
      url: "http://127.0.0.1:5000/LockManager",
      type: "POST",
      dataType: 'json',
      data: JSON.stringify(requestData),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (data) {
        timePrint(data, '#setDataItemsButton success', 'data');
        checkType(data, "data", '#setDataItemsButton success');
        var jsonTable = jsonToHtmlTable(pythonListToJSON("Item de Dados", data));
        $('#dataItemTableContainer').empty().append(jsonTable);
      }
    });
  });
});