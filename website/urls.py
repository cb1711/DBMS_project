from django.conf.urls import url
from . import views


urlpatterns= [
	url(r'^home/$',views.home,name='home'),
	url(r'^catalog/$',views.catalog,name='catalog'),
	url(r'^customers/$',views.customers,name='customers'),
	url(r'^suppliers/$',views.suppliers,name='suppliers'),
	url(r'^pending/$',views.pending,name='pending'),
	url(r'^sale/$',views.sale,name='sale'),
	url(r'^cart/$',views.cart,name='cart'),
	url(r'^inventory/$',views.inventory,name='inventory'),
	url(r'^purchase/$',views.purchase,name='purchase'),
	url(r'^order/$',views.order,name='order'),
	url(r'^book/$',views.book,name='book'),
	url(r'^login/',views.user_login,name='login'),
	url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^register/$',views.register,name='register'),
	url(r'^catalog/(?P<num>[0-9]+)/$',views.productDetails,name='productDetails'),
	url(r'^customers/(?P<num>[0-9]+)/$',views.customerDetails,name='customerDetails'),
	url(r'^suppliers/(?P<num>[0-9]+)/$',views.supplierDetails,name='supplierDetails'),
	url(r'^catalog/add/$',views.addProduct,name='addProduct'),
	url(r'^suppliers/add/$',views.addSupplier,name='addSupplier'),
	url(r'^confirm/$',views.confirm,name='confirm'),
	url(r'^purchasedetails/$',views.purchaseDetails,name='purchaseDetails'),
	url(r'^approve/$',views.approval,name='approval'),
	url(r'^stats/$',views.stats,name='stats'),
	url(r'^repay/$',views.repay,name='repay'),
	url(r'^addfeed/$',views.addFeed,name='addFeed'),
	url(r'^addbrand/$',views.addBrand,name='addBrand'),
]	