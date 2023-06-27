function goPost(route, requestData, successCallbackFunction) {
  $.ajax({
    url: "http://127.0.0.1:{{port}}" + route,
    type: "POST",
    dataType: 'json',
    data: JSON.stringify(requestData),
    contentType: "application/json; charset=utf-8",
    success: function (data) {
      scrutinize(data, "data", '#readDataItemButton success');
      successCallbackFunction(data);
    }
  });
}

function lockManager(requestData, successCallbackFunction) {
  goPost("/LockManager", requestData, successCallbackFunction)
}

function transactionManager(requestData, successCallbackFunction) {
  goPost("/TransactionManager", requestData, successCallbackFunction)
}

function listDataItems() {
  var requestData = {
    method: 'list_data_items',
    message: '{}',
  }

  //scrutinize(requestData.message, "message", 'listDataItems');
  //scrutinize(requestData, "requestData", 'listDataItems');

  lockManager(requestData, updateDataItemTable);
}

function listTransactions() {
  var requestData = {
    method: 'list_transactions',
    message: '{}',
  }

  scrutinize(requestData.message, "message", 'listTransactions');
  scrutinize(requestData, "requestData", 'listTransactions');

  transactionManager(requestData, updateTransactionTables);
}

function listLocks() {
  var requestData = {
    method: 'list_locks',
    message: '{}',
  }

  scrutinize(requestData.message, "message", 'listLocks');
  scrutinize(requestData, "requestData", 'listLocks');

  transactionManager(requestData, updateLocksTable);
}

function setDataItems() {
  var requestData = {
    method: 'reset',
    message: { data_items: eval($('#dataItemText').val()) },
  }

  //scrutinize(requestData.message, "message", 'setDataItems');
  //scrutinize(requestData, "requestData", 'setDataItems');

  lockManager(requestData, updateDataItemTable);
}

function insertTransaction() {
  var requestData = {
    method: 'add_transaction',
    message: { transaction_string: $('#transactionText').val() },
  }

  //scrutinize(requestData.message, "message", 'insertTransaction');
  //scrutinize(requestData, "requestData", 'insertTransaction');

  transactionManager(requestData, updateTransactionTables);
}

function stepInto() {
  var requestData = {
    method: 'step_into',
    message: '{}',
  }

  scrutinize(requestData.message, "message", 'stepInto');
  scrutinize(requestData, "requestData", 'stepInto');

  transactionManager(requestData, updateTransactionTables);
}

function killButtonClickHandler() {

  var requestData = {
    method: 'reset',
    message: { id: eval($(this).attr("id")) },
  }

  transactionManager(requestData, updateTransactionTables);

}
