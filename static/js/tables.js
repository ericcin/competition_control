// Function to convert JSON to HTML table
function jsonToHtmlTable(jsonData) {
  var table = $('<table class="fl-table">');
  var thead = $('<thead>').appendTo(table);
  var tbody = $('<tbody>').appendTo(table);

  // Create table headers
  var headers = Object.keys(jsonData[0]);
  var headerRow = $('<tr>').appendTo(thead);
  headers.forEach(function (header) {
    $('<th>').html(header).appendTo(headerRow);
  });

  // Create table rows and cells
  jsonData.forEach(function (rowData) {
    var row = $('<tr>').appendTo(tbody);
    headers.forEach(function (header) {
      $('<td>').html(rowData[header] === ' ' ? '&nbsp;' : rowData[header]).appendTo(row);
    });
  });

  return table;
}

function pythonListToJSON(header, list) {
  console.log(list)
  return list.map(function (item) {
    var obj = {};
    obj[header] = item;
    return obj;
  });
}

// Generate the new HTML markup for the transactions
function generateTransactionHTML(transactions) {
  let transactionHTML = "";
  for (const transaction of transactions) {
    scrutinize(transaction, 'transaction', 'generateTransactionHTML');
    let headerHTML = `<h2 class="transaction-name">Transação ${transaction["id"]}</h2>`;
    let phaseHTML = `<p class="phase">Phase: ${transaction["phase"]}</p>`;
    let statusHTML = `<p class="status">Status: ${transaction["status"]}</p>`;
    let commands = transaction["commands"];
    scrutinize(commands, 'commands', 'generateTransactionHTML');
    console.log("transaction[next_query]: " + transaction["next_query"])
    let parsedCommandList = commands.map((item, index) => {
      console.log(index)
      console.log(item)
      if (index === transaction["next_query"]) {
        return `<li id="command-${index}" class="next-query">${item.trim()}</li>`;
      } else {
        return `<li id="command-${index}">${item.trim()}</li>`;
      }
    }).join('');
    let operationsHTML = `<ol class="operation-list">${parsedCommandList}</ol>`;
    let locksHTML = transaction["locks"].length > 0 ? `<ul class="held-locks">${transaction["locks"]}</ul>` : "";
    let killButtonHTML = `<button id="${transaction["id"]}" class="killButton">Matar</button>`
    transactionHTML += `<div class="transaction fly">${headerHTML}${phaseHTML}${statusHTML}<h3>Queries</h3>${operationsHTML}<h3>Bloqueios</h3>${locksHTML}</div>`;
  }
  return `<div class="transaction-container fly">${transactionHTML}</div>`;
}

function updateDataItemTable(data) {
  //scrutinize(data, place = 'updateDataItemTable')
  var jsonTable = jsonToHtmlTable(pythonListToJSON("Item de Dados", data));
  //scrutinize(jsonTable, variableName = 'jsonTable', place = 'updateDataItemTable')
  $('#dataItemTableContainer').empty().append(jsonTable);
}

function updateTransactionTables(data) {
  scrutinize(data, place = 'updateTransactionTables before data map')
  transaction_data = data.map(({ commands, next_query, id, locks, phase, status }) => ({ id, phase, status, next_query, commands, locks }));
  scrutinize(transaction_data, place = 'updateTransactionTable after data map')
  var jsonTable = jsonToHtmlTable(transaction_data);
  scrutinize(jsonTable, variableName = 'jsonTable', place = 'updateTransactionTable')
  $('#transactionTableContainer').empty().append(jsonTable);

  // Find the existing <div> element by its class
  const existingContainer = $(".transaction-container");

  // Replace the HTML content with the new generated HTML markup
  if (existingContainer.length > 0) {
    const newHTML = generateTransactionHTML(data);
    existingContainer.html(newHTML);
  }

  locks_data = data["formatted_locks"];
  scrutinize(locks_data)
  updateLocksTable(locks_data)

}

function updateLocksTable(data) {
  scrutinize(data, 'data', 'updateLocksTable');

  scrutinize(data, 'data', 'updateLocksTable');
  const jsonTable = jsonToHtmlTable(data);
  scrutinize(jsonTable, 'jsonTable', 'updateLocksTable');
  $('#lockTableContainer').empty().append(jsonTable);
}
