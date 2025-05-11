from django.urls import path,include
from .views import PrivateShipment,SignIn,PrivateCRUDShipment



patchshipment = PrivateCRUDShipment.as_view({
    
    'patch': 'updateshipment'

})

getall = PrivateCRUDShipment.as_view({
    
    'get': 'getall'

})

deleteshipment = PrivateCRUDShipment.as_view({
    
    'delete': 'deleteshipment'

})

urlpatterns = [

    path('user/login',SignIn.as_view(),name='signin'),
    path('shipment/list',PrivateShipment.as_view(),name='Get Single shipment'),
    path('shipment/all',getall,name='get all shipment'),
    path('shipment/add',PrivateShipment.as_view(),name='add'),
    path('shipment/delete',deleteshipment,name='delete'),
    path('shipment/update/<int:id>',patchshipment,name='patch')

]