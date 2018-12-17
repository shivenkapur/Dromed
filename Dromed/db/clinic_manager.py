from models import *

def updateStoredValues():
    orderNo = 0
    username = ""
    for value in StoredValues.objects.all():
        orderNo = value.latestOrderNo
        username = value.username
        value.latestOrderNo +=1
        value.save()
    return orderNo,username

def SaveOrder(putData):
    
    orderNo,username = updateStoredValues()
    
    
    quantity = 0
    weight = 0
    objects = json.loads(putData)
    items = Item.objects.all();
    
    i = 0
    priority = ''
    for obj in objects:
        if i == 0:
            priority = obj['priority']
            i+=1
        else:
            item_asoc_order = Item_Asoc_Order.create(itemNo= int(obj['itemNo']), orderNo = orderNo, qty = obj['quantity'])
            item_asoc_order.save();
            quantity += int(obj['quantity'])
            weight += int(obj['quantity']) * obj['weight']


    user = Users.objects.filter(username = username)
    
    order = Order.create(orderNo = orderNo, noOfItems = quantity, weight = weight,clinicManager_location =  user[0].clinic, priority = priority, username = username)
    order.date = datetime.datetime.now()
    order.time = datetime.datetime.now()
    order.save();