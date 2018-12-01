
var dict = {};
var dict2 = {};
dictButtons = {};
totalweight = 0
function myFunction(clicked_id, desc, weight, image) {

  if(!(clicked_id in dict)){
    dict[clicked_id] = 1;
    dict2[clicked_id] = weight;
  }
  else
    dict[clicked_id]++;

  qty = dict[clicked_id];

  htmltext = '<div class="col-md-12 col-sm-12 col-xs-12" id = "item'+clicked_id+ '">' +
                '<div class="row justify-content-md-center mb-4 mt-4 ml-4">'+
                    '<div class="col-md-2 col-sm-2 col-xs-2 pl-5 ml-4 mb-3">'+
                        '<img src='+image+' class="img-fluid prodimg" alt="Responsive image">'+
                            ''+
                        '</img>'+
                    '</div>'+
                '<div class = "col-md-4 col-sm-4 col-xs-4 pl-5 ml-5" style = "margin-left:30px;margin-right:0px;">'+
                    '<strong>Description</strong> <br>'+
                        desc+
                    '<br><br>'+
                        '<button type = "button" onclick = qtychange('+clicked_id+',this.id) id = "minus" style = "padding:0;height:30px;width:30px;" class = "btn btn-sm btn-default btn-secondary btn-circle">'+
                            '-'+
                        '</button>'+
                            '<input type="text" value = "1" id = "qty'+clicked_id+'" name="usrname" class = "text-center ml-2 mr-2" style = "width:50px;" readonly>'
                        +
                        '<button type = "button" onclick = qtychange('+clicked_id+',this.id) id = "plus" style = "padding:0;height:30px;width:30px;" class = "btn btn-sm btn-default btn-secondary btn-circle">'+
                            '+'+
                        '</button>'+
                '</div>'+ 
                '<div class = "col-md-2 col-sm-3 col-xs-3" style = "margin-left:30px;">'+
                    '<strong>Weight</strong> <br>'+weight+
                '</div>'+
                '<div class = "col-md-3 col-sm-3 col-xs-3">'+
                   '<button class = "btn btn-secondary" style = "border:0;font-size: 15px;padding:10px;" onclick="remove('+clicked_id+')"><strong>REMOVE</strong></button>'+
                '</div>'+
            '</div>'+
            '<hr>';

    htmltext2 = 
                '<div class="row justify-content-md-center mb-4 mt-4 ml-4">'+
                    '<div class="col-md-2 col-sm-2 col-xs-2 pl-5 ml-4 mb-3">'+
                        '<img src='+image+' class="img-fluid prodimg" alt="Responsive image">'+
                            ''+
                        '</img>'+
                    '</div>'+
                '<div class = "col-md-4 col-sm-4 col-xs-4 pl-5 ml-5" style = "margin-left:30px;margin-right:0px;">'+
                    '<strong>Description</strong> <br>'+
                        desc+
                    '<br><br>'+
                        '<button type = "button" onclick = qtychange('+clicked_id+',"minus",this.id) id = "minus" style = "padding:0;height:30px;width:30px;" class = "btn btn-sm btn-default btn-secondary btn-circle">'+
                            '-'+
                        '</button>'+
                            '<input type="text" value = "1" id = "qty'+clicked_id+'" name="usrname" class = "text-center ml-2 mr-2" style = "width:50px;">'
                        +
                        '<button type = "button" onclick = qtychange('+clicked_id+',"plus",this.id) id = "plus" style = "padding:0;height:30px;width:30px;" class = "btn btn-sm btn-default btn-secondary btn-circle">'+
                            '+'+
                        '</button>'+
                '</div>'+ 
                '<div class = "col-md-2 col-sm-3 col-xs-3" style = "margin-left:30px;">'+
                    '<strong>Weight</strong> <br>'+weight+
                '</div>'+
                '<div class = "col-md-3 col-sm-3 col-xs-3">'+
                   '<button class = "btn btn-secondary" style = "border:0;font-size: 15px;padding:10px;" onclick="remove('+clicked_id+')"><strong>REMOVE</strong></button>'+
                '</div>'+
            '</div>'+
            '<hr>';

    if(dict[clicked_id] == 1)
    {
        $('#cartdiv').append(htmltext);
        $('#qty' +clicked_id).on('input',function(e){
            dict[clicked_id] = $('#qty' +clicked_id).val();
        });
    }
    else
    {
        $('#item'+clicked_id).html(htmltext2);
        $('#qty' +clicked_id).on('input',function(e){
            dict[clicked_id] = $('#qty' +clicked_id).val();
        });
    }

    qtychange(clicked_id,"plus",1);
}

function roundToTwo(num) {    
    return +(Math.round(num + "e+2")  + "e-2");
}

function qtychange(clicked_id, type, callType = 0)
{
    if(callType == 1)
        dict[clicked_id]--;
    if(type == "plus")
    {
        $('#qty' + clicked_id).val(++dict[clicked_id])
        totalweight += parseFloat(dict2[clicked_id])
    }
    else if(type == "minus" && dict[clicked_id] - 1 > 0)
    {
        $('#qty' + clicked_id).val(--dict[clicked_id])
        totalweight -= parseFloat(dict2[clicked_id])
    }

    totalweight = roundToTwo(totalweight)

    $('#totalweight').html('TOTAL WEIGHT: '+totalweight+' KGS');
    console.log(totalweight)

}

function remove(clicked_id)
{
    $('#item'+clicked_id).remove()
    totalweight -= dict[clicked_id]*parseFloat(dict2[clicked_id])
    $('#totalweight').html('TOTAL WEIGHT: '+totalweight+' KGS');
    dict[clicked_id] = 0

}
function sendData()
{
    data = [];
    priority = ''    
    for (var key in dictButtons) {
        if(dictButtons[key] == 1)
            priority = key
    }
    data[0] = {};
    data[0]['priority'] = priority

    i = 1;
    for (var key in dict) {
        if(dict[key] != 0)
        {
            data[i] = {};
            data[i]['itemNo'] = key;
            data[i]['quantity'] = dict[key];
            data[i]['weight'] = dict2[key];

            console.log(dict[key]);
            i++;
        }
    }

    url = "send/";
    var json = JSON.stringify(data);

    console.log(json);

    $.post(url, json)
    .done(function() {
        window.location.href='';
    })
    .fail(function() {
    })
    .always(function() {
     });
}

function priority(buttonID)
{
    for (var key in dictButtons) {
        dictButtons[key] = 0;
        $('#'+key).css('opacity', 0.5);
    }
    $('#'+'High').css('opacity', 0.5);
    $('#'+'Medium').css('opacity', 0.5);
    $('#'+'Low').css('opacity', 0.5);
    $('#'+buttonID).css('opacity', 1);
    dictButtons[buttonID] = 1;
}




