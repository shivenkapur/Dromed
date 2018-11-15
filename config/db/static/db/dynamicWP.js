var dict = {};



function myFunction(clicked_id) {     
    
    for (var key in dict) {
        dict[key] = 0;
    }

    dict[clicked_id] = 1;



    htmltext = '{% for order in Order %}'+
        '{% if order.orderNo == '+clicked_id+ '%}'+
        '<div style = "padding-top: 20px;font-size: 20px;">ORDER DETAILS</div>'+
        '<hr>'+
        '<div style = "padding: 5px 0 5px 0;font-size: 15px;"><strong> ORDER PRIORITY</strong></div>'+
        '<div style = "padding: 20px 0px 5px 10px;">{{order.Priority}}</div>'+
        '<div style = "padding: 20px 0 5px 0;font-size: 15px;"><strong> ORDER NUMBER</strong></div>'+
        '<div style = "padding: 15px 0px 5px 10px;">{{order.orderNo}}</div>'+
        '<div style = "padding: 20px 0 5px 0;font-size: 15px;"><strong> ORDER STATUS</strong></div>'+
        '<div style = "padding: 15px 0px 5px 10px;">QUEUED FOR PROCESSING</div>'+
        '<div style = "padding: 20px 0 5px 0;font-size: 15px;"><strong> CLINIC MANAGER</strong></div>'+
        '<div style = "padding: 15px 0px 5px 10px;">Shiven Kapur</div>'+
        '<div style = "padding: 20px 0 5px 0;font-size: 15px;"><strong> DELIVERING TO</strong></div>'+
        '<div style = "padding: 15px 0px 5px 10px;">UHS</div>'+
        '{% endif %}'+
        '{% endfor %}';

    $('#orderdetails').append(htmltext);
}