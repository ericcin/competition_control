// Function to convert JSON to HTML table
function jsonToHtmlTable(jsonData) {
  var table = $('<table class="fl-table">');
  var thead = $('<thead>').appendTo(table);
  var tbody = $('<tbody>').appendTo(table);

  // Create table headers
  var headers = Object.keys(jsonData[0]);
  var headerRow = $('<tr>').appendTo(thead);
  headers.forEach(function (header) {
    $('<th>').text(header).appendTo(headerRow);
  });

  // Create table rows and cells
  jsonData.forEach(function (rowData) {
    var row = $('<tr>').appendTo(tbody);
    headers.forEach(function (header) {
      $('<td>').text(rowData[header]).appendTo(row);
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

var myHeader = 'Data Item';
var myList = ['Apple', 'Banana', 'Orange'];

var jsonArray = pythonListToJSON(myHeader, myList);
console.log(jsonArray);

function listCSVs() {
  $.get('http://127.0.0.1:5000/list_csv_files', function (data) {
    // Print the received JSON data
    console.log(data);
    var jsonTable = jsonToHtmlTable(data);
    $('#csvTableContainer').empty().append(jsonTable);
  });
}
