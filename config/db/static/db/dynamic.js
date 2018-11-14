var dict = {};



function myFunction(clicked_id, desc, weight) {

  if(!(clicked_id in dict))
    dict[clicked_id] = 1;
  else
    dict[clicked_id]++;

  qty = dict[clicked_id];

  htmltext = '<div class="col-md-12 col-sm-12 col-xs-12" id = "item'+clicked_id+ '">' +
    '<div class="row justify-content-md-center mb-1">'+
    '<div class="col-md-3 col-sm-3 col-xs-3 pl-1 ml-2">' +
    '<strong>Item : </strong>'+clicked_id+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    'Qty : '+ qty +
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '</div>'+
    '<div class="col-md-2 col-sm-2 col-xs-2 pl-5 ml-4">'+
    '<button type = "button dropdown-toggle dropdown-left" data-toggle = "dropdown"  class = "btn btn-default btn-danger btn-circle crossorder">'+
    'X'+
    '</button>'+
    '</div>'+
    '</div>'+
    '<div class="row justify-content-md-center pt-2">'+
    '<div class="col-md-3 col-sm-3 col-xs-3 pl-1 ml-2">'+
    '<strong>ORDER WEIGHT</strong>'+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '<strong>Item</strong>'+
    '</div>'+ 
    '<div class="col-md-2 col-sm-2 col-xs-2 pl-3 ml-4">'+
    '<strong>DELIVER FROM</strong>'+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '</div>'+
    '</div>'+
    '<div class="row justify-content-md-center mb-3 pt-1">'+
    '<div class="col-md-3 col-sm-3 col-xs-3 pl-1 ml-2">'+
    weight+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    desc+
    '</div>'+ 
    '<div class="col-md-2 col-sm-2 col-xs-2 pl-3 ml-4">'+
    'QMH'+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '</div>'+
    '</div>'+
    '<hr>'+
    '</div>';

    htmltext2 = 
    '<div class="row justify-content-md-center mb-1">'+
    '<div class="col-md-3 col-sm-3 col-xs-3 pl-1 ml-2">' +
    '<strong>Item : </strong>'+clicked_id+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    'Qty : '+ qty +
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '</div>'+
    '<div class="col-md-2 col-sm-2 col-xs-2 pl-5 ml-4">'+
    '<button type = "button dropdown-toggle dropdown-left" data-toggle = "dropdown"  class = "btn btn-default btn-danger btn-circle crossorder">'+
    'X'+
    '</button>'+
    '</div>'+
    '</div>'+
    '<div class="row justify-content-md-center pt-2">'+
    '<div class="col-md-3 col-sm-3 col-xs-3 pl-1 ml-2">'+
    '<strong>ORDER WEIGHT</strong>'+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '<strong>Item</strong>'+
    '</div>'+ 
    '<div class="col-md-2 col-sm-2 col-xs-2 pl-3 ml-4">'+
    '<strong>DELIVER FROM</strong>'+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '</div>'+
    '</div>'+
    '<div class="row justify-content-md-center mb-3 pt-1">'+
    '<div class="col-md-3 col-sm-3 col-xs-3 pl-1 ml-2">'+
    weight+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    desc+
    '</div>'+ 
    '<div class="col-md-2 col-sm-2 col-xs-2 pl-3 ml-4">'+
    'QMH'+
    '</div>'+
    '<div class = "col-md-3 col-sm-3 col-xs-3">'+
    '</div>'+
    '</div>'+
    '<hr>';

    if(dict[clicked_id] == 1)
    {
        $('#cartdiv').append(htmltext);
    }
    else
        $('#item'+clicked_id).html(htmltext2);
}


function sendData()
{
    data = [];
    i = 0;
    
    for (var key in dict) {
        data[i] = {};
        data[i]['itemNo'] = key;
        data[i]['quantity'] = dict[key];
        i++;
    }

    url = "send/";

    var json = JSON.stringify(data);
    $.post(url, json)
    .done(function() {
        window.location.href='';
    })
    .fail(function() {
    })
    .always(function() {
     });

}


