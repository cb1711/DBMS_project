from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,get_object_or_404,render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.context_processors import auth
from django.db import connection,transaction
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from .viewClasses import *
from .essentials import *
import smtplib
from email.mime.text import MIMEText
# Create your views here.

weight=10
def home(request):
	return render(request,'home.html')
def catalog(request):
	data=None
	with connection.cursor() as cursor:
		cursor.execute('select x.PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,x.ord,coalesce(x.Cost,0),coalesce(x.Transport,0),coalesce(x.Loading,0),coalesce(y.total,0) from (select x.pd as PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,y.ord,y.cost,y.Transport,y.Loading from (select * from (select x.PID as pd,x.Price,x.BID as brand,y.C_GST,y.S_GST,y.Type from Pricing as x,Feed as y where x.FID=y.FID) as x,Brand as y where x.brand=y.BID) as x left join(select * from (select a.ord,a.PID,b.Cost from (select max(OID) as ord,PID from OrderFill group by(PID)) as a,(select OID,PID,Cost from OrderFill) as b where a.ord=b.OID and a.PID=b.PID) as x,(select Transport,Loading,OID as od from SupplyOrder) as y where x.ord=y.od) as y on x.pd=y.PID) as x left join (select x.PID,(x.filled-coalesce(y.removed,0)) as total from(select coalesce(Sum(Quantity),0) as filled,PID from OrderFill group by(PID)) as x left join (select coalesce(sum(o.Quantity),0) as removed,o.PID from CustomerOrder as c,OrderRemove as o where c.Approved="Y" and c.OID=o.OID group by o.PID) as y on x.PID=y.PID) as y on x.PID=y.PID')
		data=cursor.fetchall()
	products=[]
	for i in data:
		products.append(salesTemplate(i))
	return render(request,'catalog.html',{"products":products})
def customers(request):
	data=None
	with connection.cursor() as cursor:
		cursor.execute('select * from (select * from (select c.CID,a.first_name,a.last_name,c.Address,a.email from Customer as c,auth_user as a where c.User=a.id) as x left join (select min(Phone),CID as pnid from CustomerPhones group by CID) as y on x.CID=y.pnid) as a left join (select CID as id,sum(Sum),sum(Paid),sum(discount) from CustomerOrder where Approved="Y" group by (CID)) as b on a.CID=b.id') 
		data=cursor.fetchall()
	#print data
	customers=[]
	for i in data:
		customers.append(customerCompleteTemplate(i))
	return render(request,'Customers.html',{"customer":customers})
def suppliers(request):
	data=None
	with connection.cursor() as cursor:
		cursor.execute('select * from (select * from Supplier as s left join (select sum(Sum),sum(Paid),SID from SupplyOrder group by (SID)) as p on s.UID=p.SID) as x left join (select SID,min(Phone) from SupplierPhones group by(SID)) as y on x.UID=y.SID') 
		data=cursor.fetchall()
	suppliers=[]
	for i in data:
		suppliers.append(supplierTemplate(i))
	return render(request,'Suppliers.html',{"supplier":suppliers})
@login_required
def pending(request):
	if not request.user.is_superuser:
		cid=0
		id=request.user.id
		data=[]
		with connection.cursor() as cursor:
			cursor.execute('select CID from Customer where User=%d'%(id))
			id=cursor.fetchone()
			cid=id[0]
			print cid
			cursor.execute('select CID,first_name,last_name,Address,phone,(sum-paid-discount) as balance from (select * from (select c.CID,a.first_name,a.last_name,c.Address,a.email from Customer as c,auth_user as a where c.User=a.id and c.CID=%d) as x left join (select min(Phone) as phone,CID as pnid from CustomerPhones where CID=%d group by CID) as y on x.CID=y.pnid) as a left join (select CID as id,sum(Sum) as sum,sum(Paid) as paid,sum(discount) as discount from CustomerOrder where Approved="Y" and CID=%d group by (CID)) as b on a.CID=b.id where (sum-paid-discount)>0;' %(int(cid),int(cid),int(cid)))
			data=cursor.fetchone()
		if(data==None):
			return render(request,"redirect.html",{"title":pending,"message":"No payments to show for you"})
		customer=balance(data)
		return render(request,"repay.html",{"user":customer,"flag":0,"id":customer.cid})
	if request.method=="POST":
		if "customer" in request.POST:
			cid=request.POST.get("cid")
			data=[]
			with connection.cursor() as cursor:
				cursor.execute('select CID,first_name,last_name,Address,phone,(sum-paid-discount) as balance from (select * from (select c.CID,a.first_name,a.last_name,c.Address,a.email from Customer as c,auth_user as a where c.User=a.id and c.CID=%d) as x left join (select min(Phone) as phone,CID as pnid from CustomerPhones where CID=%d group by CID) as y on x.CID=y.pnid) as a left join (select CID as id,sum(Sum) as sum,sum(Paid) as paid,sum(discount) as discount from CustomerOrder where Approved="Y" and CID=%d group by (CID)) as b on a.CID=b.id where (sum-paid-discount)>0;' %(int(cid),int(cid),int(cid)))
				data=cursor.fetchone()
			customer=balance(data)
			return render(request,"repay.html",{"user":customer,"flag":0,"id":customer.cid})
		else:
			sid=request.POST.get("sid")
			data=[]
			with connection.cursor() as cursor:
				cursor.execute('select UID,Name,Address,phone,balance from (select * from (select * from Supplier where UID=%d)as s left join (select (sum(Sum)-sum(Paid)) as balance,SID from SupplyOrder where SID=%d group by (SID)) as p on s.UID=p.SID) as x left join (select SID,min(Phone) as phone from SupplierPhones where SID=%d group by(SID)) as y on x.UID=y.SID where balance>0' %(int(sid),int(sid),int(sid)))
				data=cursor.fetchone()
			suppl=supplier(data)
			return render(request,"repay.html",{"user":suppl,"flag":1,"id":suppl.sid}) 
	else:
		data=[]
		data2=[]
		with connection.cursor() as cursor:
			cursor.execute('select CID,first_name,last_name,Address,phone,(sum-paid-discount) as balance from (select * from (select c.CID,a.first_name,a.last_name,c.Address,a.email from Customer as c,auth_user as a where c.User=a.id) as x left join (select min(Phone) as phone,CID as pnid from CustomerPhones group by CID) as y on x.CID=y.pnid) as a left join (select CID as id,sum(Sum) as sum,sum(Paid) as paid,sum(discount) as discount from CustomerOrder where Approved="Y" group by (CID)) as b on a.CID=b.id where (sum-paid-discount)>0;')
			data=cursor.fetchall()
			cursor.execute('select UID,Name,Address,phone,balance from (select * from Supplier as s left join (select (sum(Sum)-sum(Paid)) as balance,SID from SupplyOrder group by (SID)) as p on s.UID=p.SID) as x left join (select SID,min(Phone) as phone from SupplierPhones group by(SID)) as y on x.UID=y.SID where balance>0')
			data2=cursor.fetchall()
		customers=[]
		suppliers=[]
		for i in data:
			customers.append(balance(i))
		for i in data2:
			suppliers.append(supplier(i))
	return render(request,'Pending.html',{"debitors":customers,"creditors":suppliers})
@login_required
def sale(request):
	data=None
	with connection.cursor() as cursor:
		cursor.execute('select x.PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,x.ord,coalesce(x.Cost,0),coalesce(x.Transport,0),coalesce(x.Loading,0),coalesce(y.total,0) from (select x.pd as PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,y.ord,y.cost,y.Transport,y.Loading from (select * from (select x.PID as pd,x.Price,x.BID as brand,y.C_GST,y.S_GST,y.Type from Pricing as x,Feed as y where x.FID=y.FID) as x,Brand as y where x.brand=y.BID) as x left join(select * from (select a.ord,a.PID,b.Cost from (select max(OID) as ord,PID from OrderFill group by(PID)) as a,(select OID,PID,Cost from OrderFill) as b where a.ord=b.OID and a.PID=b.PID) as x,(select Transport,Loading,OID as od from SupplyOrder) as y where x.ord=y.od) as y on x.pd=y.PID) as x left join (select x.PID,(x.filled-coalesce(y.removed,0)) as total from(select coalesce(Sum(Quantity),0) as filled,PID from OrderFill group by(PID)) as x left join (select coalesce(sum(o.Quantity),0) as removed,o.PID from CustomerOrder as c,OrderRemove as o where c.Approved="Y" and c.OID=o.OID group by o.PID) as y on x.PID=y.PID) as y on x.PID=y.PID')
		data=cursor.fetchall()
	products=[]
	for i in data:
		products.append(salesTemplate(i))
	return render(request,'sales.html',{"products":products})
@login_required
def cart(request):
	if request.method=='POST':
		items=request.POST.getlist('items')
		data=None
		with connection.cursor() as cursor:
			cursor.execute('select x.PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,x.ord,coalesce(x.Cost,0),coalesce(x.Transport,0),coalesce(x.Loading,0),coalesce(y.total,0) from (select x.pd as PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,y.ord,y.cost,y.Transport,y.Loading from (select * from (select x.PID as pd,x.Price,x.BID as brand,y.C_GST,y.S_GST,y.Type from Pricing as x,Feed as y where x.FID=y.FID) as x,Brand as y where x.brand=y.BID) as x left join(select * from (select a.ord,a.PID,b.Cost from (select max(OID) as ord,PID from OrderFill group by(PID)) as a,(select OID,PID,Cost from OrderFill) as b where a.ord=b.OID and a.PID=b.PID) as x,(select Transport,Loading,OID as od from SupplyOrder) as y where x.ord=y.od) as y on x.pd=y.PID) as x left join (select x.PID,(x.filled-coalesce(y.removed,0)) as total from(select coalesce(Sum(Quantity),0) as filled,PID from OrderFill group by(PID)) as x left join (select coalesce(sum(o.Quantity),0) as removed,o.PID from CustomerOrder as c,OrderRemove as o where c.Approved="Y" and c.OID=o.OID group by o.PID) as y on x.PID=y.PID) as y on x.PID=y.PID')
			data=cursor.fetchall()
		li=[p for p in data if str(p[0]) in items]
		products=[]
		#select x.Loading,x.Transport,y.PID,y.Cost from SupplyOrder as x,(select x.PID,x.OID,x.Cost from OrderFill as x,(select max(OID) as OID,PID from OrderFill group by(PID)) as y where x.OID=y.OID and x.PID=y.PID) as y where x.OID=y.OID
		for i in li:
			products.append(salesTemplate(i))
		data=None
		print request.user.id
		with connection.cursor() as cursor:
			cursor.execute('select c.CID,a.first_name,a.last_name,a.email,c.Address from Customer as c,auth_user as a where c.User=a.id')
			data=cursor.fetchall()
		users=[]
		for i in data:
			users.append(customerTemplate(i))
		return render(request,'cart.html',{"item":products,"ulist":users})
def inventory(request):
	data=None
	with connection.cursor() as cursor:
		cursor.execute("select * from Godown as x left join (select (x.filled-y.removed) as total,x.GID from(select Sum(Quantity) as filled,GID from OrderFill group by(GID)) as x,(select sum(o.Quantity) as removed,o.GID from CustomerOrder as c,OrderRemove as o where c.Approved='Y' and c.OID=o.OID group by o.GID) as y where x.GID=y.GID) as y on x.GodownNum=y.GID")
		data=cursor.fetchall()
	godowns=[]
	for i in data:
		godowns.append(godownTemplate(i))
	return render(request,'inventory.html',{'godowns':godowns})
def purchase(request):
	if not request.user.is_superuser:
		return render(request,"redirect.html",{"message":"You can't view this page"})
	data=None
	with connection.cursor() as cursor:
		cursor.execute('select x.PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,x.ord,coalesce(x.Cost,0),coalesce(x.Transport,0),coalesce(x.Loading,0),coalesce(y.total,0) from (select x.pd as PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,y.ord,y.cost,y.Transport,y.Loading from (select * from (select x.PID as pd,x.Price,x.BID as brand,y.C_GST,y.S_GST,y.Type from Pricing as x,Feed as y where x.FID=y.FID) as x,Brand as y where x.brand=y.BID) as x left join(select * from (select a.ord,a.PID,b.Cost from (select max(OID) as ord,PID from OrderFill group by(PID)) as a,(select OID,PID,Cost from OrderFill) as b where a.ord=b.OID and a.PID=b.PID) as x,(select Transport,Loading,OID as od from SupplyOrder) as y where x.ord=y.od) as y on x.pd=y.PID) as x left join (select x.PID,(x.filled-coalesce(y.removed,0)) as total from(select coalesce(Sum(Quantity),0) as filled,PID from OrderFill group by(PID)) as x left join (select coalesce(sum(o.Quantity),0) as removed,o.PID from CustomerOrder as c,OrderRemove as o where c.Approved="Y" and c.OID=o.OID group by o.PID) as y on x.PID=y.PID) as y on x.PID=y.PID')

		data=cursor.fetchall()
	products=[]
	for i in data:
		products.append(salesTemplate(i))
	return render(request,'purchase.html',{"products":products})
def addFeed(request):
	if not request.user.is_superuser:
		return render(request,"redirect.html",{"message":"You can't view this page"})
	if request.method=='POST':
		s_gst=request.POST.get('sgst')
		c_gst=request.POST.get('cgst')
		type=request.POST.get('type')
		with connection.cursor() as cursor:
			cursor.execute('insert into Feed (S_GST,C_GST,Type) values(%s,%s,"%s")' %(s_gst,c_gst,type))
		return HttpResponseRedirect("/catalog/add")
	else:
		return render(request,"feed.html")
def addBrand(request):
	if not request.user.is_superuser:
		return render(request,"redirect.html",{"message":"You can't view this page"})
	if request.method=='POST':
		address=request.POST.get('address')
		name=request.POST.get('name')
		phone=request.POST.get('phone')
		try:
			with connection.cursor() as cursor:
				cursor.execute('insert into Brand (Name,Phone,Address) values("%s","%s","%s")' %(name,phone,address))
			return HttpResponseRedirect("/catalog/add")
		except DataError:
			return render(request,"brand.html",{"message":"Add valid informat"})
	else:
		return render(request,"brand.html")
def order(request):
	if request.method=='POST':
		items=request.POST.getlist('items')
		if len(items)==0:
			return HttpResponseRedirect('/purchase')
		data=None
		with connection.cursor() as cursor:
			cursor.execute('select a.PID,a.Name,f.Type,a.Price,f.C_GST,f.S_GST from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID')
			data=cursor.fetchall()

		li=[p for p in data if str(p[0]) in items]
		products=[]
		for i in li:
			products.append(productTemplate(i))

		users=[]
		data=None
		with connection.cursor() as cursor:
			cursor.execute('select * from Supplier')
			data=cursor.fetchall()
		for i in data:
			users.append(supplierTemplate(i))

		return render(request,'pOrder.html',{"item":products,"ulist":users})
	else:
		return render(request,"redirect.html",{"message":"You have been denied access to this page"})
def productDetails(request,num):
	data=None
	num=int(num)
	with connection.cursor() as cursor:
		cursor.execute("select x.PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,x.ord,coalesce(x.Cost,0),coalesce(x.Transport,0),coalesce(x.Loading,0),coalesce(y.total,0),x.Address,x.Name from (select x.pd as PID,x.Price,x.C_GST,x.S_GST,x.Name,x.Type,x.Address,y.ord,y.cost,y.Transport,y.Loading,x.Phone from (select * from (select x.PID as pd,x.Price,x.BID as brand,y.C_GST,y.S_GST,y.Type from (select * from Pricing where PID=%d) as x,Feed as y where x.FID=y.FID) as x,Brand as y where x.brand=y.BID) as x left join(select * from (select a.ord,a.PID,b.Cost from (select max(OID) as ord,PID from OrderFill where PID=%d) as a,(select OID,PID,Cost from OrderFill where PID=%d) as b where a.ord=b.OID) as x,(select Transport,Loading,OID as od from SupplyOrder) as y where x.ord=y.od) as y on x.pd=y.PID) as x left join (select x.PID,(x.filled-coalesce(y.removed,0)) as total from(select coalesce(Sum(Quantity),0) as filled,PID from OrderFill where PID=%d) as x left join (select coalesce(Sum(b.Quantity),0) as removed,b.PID from CustomerOrder as a,OrderRemove as b where a.Approved='Y' and a.OID=b.OID and b.PID=%d) as y on x.PID=y.PID) as y on x.PID=y.PID" %(num,num,num,num,num))
		data=cursor.fetchone()
	products=salesTemplate(data)
	#print mobiles
	return render(request,'product_details.html',{"product":products})
def customerDetails(request,num):
	data=None
	num=int(num)
	with connection.cursor() as cursor:
		cursor.execute('select * from (select c.CID,a.first_name,a.last_name,c.Address,a.email from (select * from Customer where CID=%d) as c, auth_user as a where c.User=a.id) as a left join (select CID as id,sum(Sum),sum(Paid),sum(discount) from CustomerOrder where CID=%d and Approved="Y") as b on a.CID=b.id ' %(num,num)) 
		data=cursor.fetchone()
	phones=None
	if data[6] is None:
		total=0
	else:
		total=float(data[6])
	if data[7] is None:
		paid=0
	else:
		paid=float(data[7])
	if data[8] is None:
		discount=0
	else:
		discount=float(data[8])
	balance=total-paid-discount
	with connection.cursor() as cursor:
		cursor.execute('select Phone from CustomerPhones where CID=%d' %(num))
		phones=cursor.fetchall()

	customer=customerTemplate(data)
	mobiles=[]
	orders=[]
	with connection.cursor() as cursor:
		cursor.execute('select * from (select * from (select * from CustomerOrder where CID=%d) as x left join (select PID as prId,OID as ordId,Quantity from OrderRemove) as y on x.OID=y.ordId) as x,(select a.PID,a.Name,f.Type from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID) as y where x.PrId=y.PID' %(num))
		orders=cursor.fetchall()
	transactions=[]
	for i in orders:
		transactions.append(customerTransactions(i))
	for i in range(len(phones)):
		mobiles.append(phones[i][0])
	
	return render(request,'customer_details.html',{"phone":mobiles,"balance":balance,"customer":customer,"transactions":transactions})
@login_required
def book(request):
	if request.method=='POST':
		customer_user=None
		if (request.user.is_superuser):
			customer_user=int(request.POST.get("customer"))
		else:
			uid=request.user.id;
			with connection.cursor() as cursor:
				cursor.execute('select CID from Customer where User=%d' %(uid))
				customer_user=int(cursor.fetchone()[0])

		items=request.POST.getlist("products")
		quantity=request.POST.getlist("inp")
		
		products=None
		customer=None
		with connection.cursor() as cursor:
			cursor.execute('select * from (select a.PID,a.Name,f.Type,a.Price,f.C_GST,f.S_GST from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID) as x left join (select x.Loading,x.Transport,y.PID,y.Cost from SupplyOrder as x,(select x.PID,x.OID,x.Cost from OrderFill as x,(select max(OID) as OID,PID from OrderFill group by(PID)) as y where x.OID=y.OID and x.PID=y.PID) as y where x.OID=y.OID) as y on x.PID=y.PID')
			products=cursor.fetchall()
		with connection.cursor() as cursor:
			cursor.execute('select c.CID,x.First_Name,x.Last_Name,x.email,c.Address from auth_user as x,(select * from Customer where CID=%d) as c where c.User=x.id' %(customer_user))
			customer=cursor.fetchall()
		with connection.cursor() as cursor:
			cursor.execute('select Phone from CustomerPhones where CID=%d' %(customer_user))
			phones=cursor.fetchall()
		phone=[]
		for i in phones:
			phone.append(i[0])
		li=[productTemplate(p) for p in products if str(p[0]) in items]
		customer=customerTemplate(customer[0])
		#print li
		cost_total=0
		costs=[]
		#taxes=[]
		totals=[]
		
		for i in range(len(li)):
			#rates.append(li[i].price)
			cst=li[i].price*float(quantity[i])/10
			costs.append(li[i].price*float(quantity[i])/10)
			cost_total+=cst
			#taxes.append(cst*li[i].C_GST/100)
			#totals.append(taxes[i]+cst)
			totals.append(cst)
		zip_list=zip(li,quantity,costs)
		#print rates	
		return render(request,'book.html',{"user":customer,"items":zip_list,"amount":cost_total,"phone":phone})
def user_login(request):
	context=RequestContext(request)
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/sale')
			else:
				return render(request,'redirect.html',{'title':'Error','message':"Your Account has been disabled."})

		else:
			return render(request,'loginpage.html',{"message":"Invalid username or password"})
	else:
		return render(request,'loginpage.html')


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/home')

def register(request):
	#registered=False
	if request.method=='POST':
		email=request.POST.get("email")
		FName=request.POST.get("fname")
		LName=request.POST.get("lname")
		password=request.POST.get("password")
		username=request.POST.get("uname")
		Addr=request.POST.get("address")
		Phone1=request.POST.get("phone1")
		Phone2=request.POST.get("phone2")
		Phone3=request.POST.get("phone3")
		Phones=[]
		Phones.append(Phone1)
		if len(Phone2)==10:
			Phones.append(Phone2)
		if len(Phone3)==10:
			Phones.append(Phone3)
		#do exception handling here
		sameEmail=()
		with connection.cursor() as cursor:
			cursor.execute('select id from auth_user where email="%s"' %(email))
			sameEmail=cursor.fetchall()
		if not isEmailID(email):
			return render(request,'register.html',{"message":"Invalid email id"})
		if len(sameEmail)!=0:
			return render(request,'register.html',{"message":"Username or email already exists"})
		with transaction.atomic():
			userID=User.objects.create_user(username=username,password=password,first_name=FName,last_name=LName,email=email)
			uid=None
			with connection.cursor() as cursor:
				cursor.execute('insert into Customer (Address,User) values ("%s", %d)' %(Addr, userID.id))
			with connection.cursor() as cursor:
				cursor.execute('select CID from Customer where User=%d' %(userID.id))
				uid=cursor.fetchone()
				for i in Phones:
					cursor.execute('insert into CustomerPhones (CID,Phone) values (%d, "%s")' %( uid[0],i))
		#registered=True
		if(request.user.is_superuser):
			return render(request,'home.html')
		user=authenticate(username=email, password=password)
		login(request,user)
		return render(request,'home.html')
	else:
		return render(request,'register.html')

def addSupplier(request):
	if request.method=='POST':
		Name=request.POST.get("name")
		Addr=request.POST.get("address")
		Phone1=request.POST.get("phone1")
		Phone2=request.POST.get("phone2")
		Phone3=request.POST.get("phone3")
		Phones=[]
		Phones.append(Phone1)
		if len(Phone2)==10:
			Phones.append(Phone2)
		if len(Phone3)==10:
			Phones.append(Phone3)
		with transaction.atomic():
			with connection.cursor() as cursor:
				cursor.execute('insert into Supplier (Name,Address) values ("%s", "%s")' %(Name,Addr))
				cursor.execute('select LAST_INSERT_ID()')
				ids=cursor.fetchone()
				print ids[0]
				print Phones
				for i in Phones:
					cursor.execute('insert into SupplierPhones values(%d,"%s")' %(ids[0],i))

		return render(request,'home.html')
	else:
		return render(request,'supplier_add.html')


def addProduct(request):
	if request.user.is_superuser:
		if(request.method=='POST'):
			Brand=int(request.POST.get("brand"))
			Type=int(request.POST.get("type"))
			Cost=int(request.POST.get("cost"))
			with connection.cursor() as cursor:
				cursor.execute('insert into Pricing (FID,BID,Price) values(%d,%d,%d)' %(Type,Brand,Cost))
				return HttpResponseRedirect('/catalog') 

		else:
			types=[]
			brands=[]

		with connection.cursor() as cursor:
			cursor.execute('select * from Feed')
			types=cursor.fetchall()
			cursor.execute('select * from Brand')
			brands=cursor.fetchall()
		Brands=[]
		Types=[]
		for i in brands:
			Brands.append(brandTemplate(i))
		for i in types:
			Types.append(feedTemplate(i))
		return render(request,'product_add.html',{"brands":Brands,"feed":Types})
	else:
		return render(request,"redirect.html",{"message":"You don't have access to this page"})


def purchaseDetails(request):
	if not request.user.is_superuser:
		return render(request,"redirect.html",{"message":"You can't view this page"})
	if request.method=='POST':
		products=request.POST.getlist("products")
		user=request.POST.get("supplier")
		rates=request.POST.getlist("rates")
		quantities=request.POST.getlist("quantity")
		loading=request.POST.get("loading")
		transport=request.POST.get("transport")
		date=request.POST.get("Date")
		paid=request.POST.get("paid")

		orderCost=0
		ItemCost=[]
		otherCost=[]
		#get the gst rate of the product
		tax_paid=[]
		total=0
		for i in range(len(products)):
			quantities[i]=int(quantities[i])
			ItemCost.append(float(rates[i])*float(quantities[i])/100)
			total=total+ItemCost[-1]
			loadingCost=float(rates[i])
		today=str(datetime.date.today())
		tm=str(datetime.datetime.now())
		tm=tm.split(' ')
		time=tm[1].split('.')
		time=time[0]
		gdns=[]
		godowns=[]
		with connection.cursor() as cursor:
			cursor.execute('select x.GodownNum,x.Capacity-y.total as rem,x.Address from Godown as x left join (select (x.filled-y.removed) as total,x.GID from(select Sum(Quantity) as filled,GID from OrderFill group by(GID)) as x,(select sum(o.Quantity) as removed,o.GID from CustomerOrder as c,OrderRemove as o where c.Approved="Y" and c.OID=o.OID group by o.GID) as y where x.GID=y.GID) as y on x.GodownNum=y.GID order by rem desc')
			gdns=cursor.fetchall()
		for i in gdns:
			godowns.append(list(i))
		placements=[]
		with connection.cursor() as cursor:
			cursor.execute('insert into SupplyOrder (SID,Sum,Paid,Date,Time,DateExpected,Loading,Transport) values(%d,%d,%d,"%s","%s","%s",%d,%d)' %(int(user),int(total),int(paid),today,time,date,int(loading),int(transport)))
			cursor.execute('select LAST_INSERT_ID()')
			oid=cursor.fetchone()
			indG=0
			#greedy approach is used here
			for i in range(len(products)):
				while quantities[i]>0:
					if godowns[indG][1]>quantities[i]:
						godowns[indG][1]-=quantities[i]
						placements.append([products[i],quantities[i],godowns[indG]])
						quantities[i]=0
					else:
						placements.append([products[i],godowns[indG][1],godowns[indG]])
						quantities[i]-=godowns[indG]
						godowns[indG][1]=0
						indG=indG+1
					cursor.execute('insert into OrderFill values(%d,%d,%d,%d,%d)' %(oid[0],int(placements[-1][0]),placements[-1][1],placements[-1][2][0],int(rates[i])))

		message="Place the ordered items as-\n "
		for i in placements:
			message=message+"Product id- "+str(i[0])+", quantity- "+str(i[1])+", godown- "+ str(i[2][2])+"\n"
		subject="New order "
		user=request.user.email

		if mail(user,message,subject):
			return render(request,'redirect.html',{"message":"Succesfully placed the order with mail sent to you"})
		else:
			return render(request,'redirect.html',{"message":"Succesfully placed the order but mail couldn't be sent"})		
		#for i in products
		#with connection.cursor() as cursor:
		#	cursor.execute('')

		return render(request,'redirect.html',{"message":"Succesfully placed the order"})
		#select sum(Quantity) as Quantity,GID,PID from OrderFill group by PID,GID order by PID,Quantity desc;
@login_required
def confirm(request):
	if request.method=='POST':
		products=request.POST.getlist("products")
		user=request.POST.get("userId")
		quantities=request.POST.getlist("quantity")
		mode=request.POST.get("transactions")
		discount=request.POST.get("discount")
		paid=request.POST.get("paid")
		total=request.POST.get("amount")
		rates=request.POST.getlist("rates")
		for i in range(len(quantities)):
			quantities[i]=int(quantities[i])
		if paid==None:
			paid=0
		if discount==None or discount==u'':
			discount=0
		for i in range(len(rates)):
			rates[i]=float(rates[i])
		today=str(datetime.date.today())
		tm=str(datetime.datetime.now())
		tm=tm.split(' ')
		time=tm[1].split('.')
		time=time[0]
		gdns=[]
		approved='N'
		if request.user.is_superuser:
			approved='Y'
		godowns={}
		with connection.cursor() as cursor:
			cursor.execute('select sum(Quantity) as Quantity,GID,PID from OrderFill group by PID,GID order by PID,Quantity desc;')
			gdns=cursor.fetchall()
		for i in gdns:
			if i[2] in godowns:
				godowns[i[2]].append([i[0],i[1]])
			else:
				godowns[i[2]]=[[i[0],i[1]]]
		placements=[]
		su=None
		orderId=0
		with connection.cursor() as cursor:
			cursor.execute('select email from auth_user where is_superuser=1')
			su=cursor.fetchall()
			cursor.execute('insert into CustomerOrder (CID,Sum,Paid,Date,Time,Discount,Approved) values(%d,%d,%d,"%s","%s",%d,"%s")' %(int(user),float(total),float(paid),today,time,float(discount),approved))
			cursor.execute('select LAST_INSERT_ID()')
			oid=cursor.fetchone()
			orderId=oid[0]
			for i in range(len(products)):
				j=0
				while quantities[i]>0 and j<len(godowns[int(products[i])]):
					if 	godowns[int(products[i])][j][0]>quantities[i]:
						cursor.execute('insert into OrderRemove values(%d,%d,%d,%d,%f)' %(int(orderId),int(products[i]),int(quantities[i]),(godowns[int(products[i])])[j][1],rates[i]))
						placements.append((orderId,products[i],quantities[i],godowns[int(products[i])][j][1]))
						(godowns[int(products[i])])[j][0]-=quantities[i]
						quantities[i]=0
					else:
						cursor.execute('insert into OrderRemove values(%d,%d,%d,%d,%f)' %(int(orderId),int(products[i]),godowns[int(products[i])])[j][0],godowns[int(products[i])][j][1],rates[i])
						placements.append((orderId,products[i],quantities[i],godowns[int(products[i])][j][1]))
						quantities[i]-=(godowns[int(products[i])])[j][0]
						(godowns[int(products[i])])[j][0]=0
						j=j+1
		#Mail the client regarding the placements	
		if request.user.is_superuser:
			return render(request,"redirect.html",{"message":"Done"})
		else:
			if mode=="off":
				return render(request,'redirect.html',{"message":"Your order has been saved you will receive a confirmationcall regarding the same"})		
			else:
				subject="Payment made by %s %s" %(request.user.first_name,request.user.last_name)
				message="A payment has been made by %s %s for an order of amount %s. Please check and validate the order and reduce the amount paid afterwards" %(request.user.first_name,request.user.last_name,total)
				to=su[0][0]
				mail(to,message,subject)
				return render(request,"online.html",{"name":str(request.user.first_name)+" "+str(request.user.last_name),"amount":total,"time":datetime.datetime.now(),"orderId":orderId})

		
		#with connection.cursor() as cursor:
		#	cursor.execute('')
		return render(request,'redirect.html',{"message":"Your order has been confirmed you will receive a confirmation call regarding the same"})
@login_required
def approval(request):
	if request.user.is_superuser:
		if request.method=="POST":
			approvals=request.POST.getlist("approvals")
			with connection.cursor() as cursor:
				cursor.execute('select x.PID,(x.filled-coalesce(y.removed,0)) as total from(select coalesce(Sum(Quantity),0) as filled,PID from OrderFill group by(PID)) as x left join (select coalesce(sum(o.Quantity),0) as removed,o.PID from CustomerOrder as c,OrderRemove as o where c.Approved="Y" and c.OID=o.OID group by o.PID) as y on x.PID=y.PID')
				quantity=cursor.fetchall()
				quant={}
				for j in quantity:
					quant[j[0]]=j[1]

				for i in approvals:
					cursor.execute('select PID,GID,Quantity from CustomerOrder natural join OrderRemove where OID=%d' %(int(i)))
					order=cursor.fetchall()
					flag=True
					for j in order:
						if quant[j[0]]>=j[2]:
							quant[j[0]]-=j[2]
						else:
							flag=False
					if flag:
						cursor.execute('update CustomerOrder set Approved="Y" where oid=%d' %(int(i)))
					else:
						cursor.execute("select c.OID,c.Date,c.Time,c.first_name,c.last_name,c.Sum, c.Address,d.Name, d.Type, c.Quantity from (select * from(select c.OID,o.PID,c.CID,c.Sum,o.Quantity,c.Time,c.Date from CustomerOrder as c,OrderRemove as o where c.Approved='N' and o.OID=c.OID and c.Date>(sysdate() -interval 7 day)) as c,(select a.first_name,a.last_name,b.Address,b.CID as x from Customer as b,auth_user as a where a.id=b.User) as d where c.CID=d.x) as c,(select a.PID as y,a.Name,f.Type, f.C_GST,f.S_GST from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID) as d where c.PID=d.y order by c.OID")
						data=cursor.fetchall()
						li=[]
						curr_oid=-1
						for i in data:
							if i[0]==curr_oid:
								li[-1].append(i)
							else:
								li.append([i])
								curr_oid=i[0]
						pending=[]
						for i in li:	
							pending.append(approveTemplate(i))
						return render(request,"approve.html",{"pending":pending,"message":' Some order(s) could not be approved due to shortage of feed'})
			return render(request,"redirect.html",{"message":"The orders have been confirm	ed with confirmation sent to the customers. The remaining names will be removed from the list after 1 week of order."})
		data=None
		with connection.cursor() as cursor:
			cursor.execute("select c.OID,c.Date,c.Time,c.first_name,c.last_name,c.Sum,c.Address,d.Name,d.Type,c.Quantity from (select * from(select c.OID,o.PID,c.CID,c.Sum,o.Quantity,c.Time,c.Date from CustomerOrder as c,OrderRemove as o where c.Approved='N' and o.OID=c.OID and c.Date>(sysdate()-interval 7 day)) as c,(select a.first_name,a.last_name,b.Address,b.CID as x from Customer as b,auth_user as a where a.id=b.User) as d where c.CID=d.x) as c,(select a.PID as y,a.Name,f.Type,f.C_GST,f.S_GST from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID) as d where c.PID=d.y order by c.OID")
			data=cursor.fetchall()
		li=[]
		curr_oid=-1
		for i in data:
			if i[0]==curr_oid:
				li[-1].append(i)
			else:
				li.append([i])
				curr_oid=i[0]
		pending=[]
		for i in li:	
			pending.append(approveTemplate(i))
		
		return render(request,"approve.html",{"pending":pending})

	else:
		return render(request,"redirect.html",{"message":"You don't have access to this page"})

#Add functionality to mail daily sales and to return quarterly sales to the owner whenever asked



def current_cost(pid):
	cost=[]
	with connection.cursor as cursor:
		cursor.execute('select * from (select x.PID as pd,x.Price,y.C_GST,y.S_GST,y.Type from Pricing as x,Feed as y where x.FID=y.FID) as x,(select * from (select a.ord,a.PID,b.Cost from (select max(OID) as ord,PID from OrderFill group by(PID)) as a,(select OID,PID,Cost from OrderFill) as b where a.ord=b.OID and a.PID=b.PID) as x,(select Transport,Loading,OID as od from SupplyOrder) as y where x.ord=y.od) as y where x.pd=y.PID')

def stats(request):
	if request.method=='POST':
		purchase=[]
		sale=[]
		periodStart=request.POST.get("start")
		periodEnd=request.POST.get("end")
		with connection.cursor() as cursor:
			cursor.execute('select * from (select * from SupplyOrder as s natural join OrderFill order by s.Date) as x natural join (select PID,Name,Type,S_GST,C_GST from (select PID,FID,Type,S_GST,C_GST,BID from Pricing natural join Feed) as x natural join Brand as y )as y ;')
			purchase=cursor.fetchall()
			cursor.execute('select * from CustomerOrder as c,OrderRemove as r where c.OID=r.OID and c.Approved="Y" and c.Date<= "%s" order by c.Date' %(periodEnd))
			sale=cursor.fetchall()
		#purchases=[]
		sales={}
		purchases={}
		statistics=[]
		for i in purchase:
			if i[0] in purchases.keys():
				purchases[i[0]].append(list(i))
			else:
				purchases[i[0]]=[i]
		for i in sale:
			if i[9] in sales.keys():
				sales[i[9]].append(list(i))
			else:
				sales[i[9]]=[i]
		for j in purchases.keys():
			for i in range(1,len(purchases[j])):
				(purchases[j])[i][10]+=purchases[j][i-1][10]
		for j in sales.keys():
			for i in range(1,len(sales[j])):
				sales[j][i][10]+=sales[j][i-1][10]
		startDate=dateConvert(periodStart)
		#print startDate
		EndDate=dateConvert(periodEnd)
		indDict={}
		purchaseDict={}
		productSold={}
		productPurchased={}
		for j in sales.keys():
			start=0
			end=len(sales[j])
			#binary search for the required index
			pstart=0
			if startDate<=sales[j][-1][4]:
				while start<=end :
					pstart=(start+end)/2
					if sales[j][pstart][4]<startDate:
						start=pstart+1
					elif sales[j][pstart][4]==startDate:
						while(pstart>=1):
							if(sales[j][pstart-1][4]==startDate):
								pstart-=1
							else:
								break
						break
					else:
						end=pstart-1
				#print "Out of the first loop with pstart" + str(pstart)
				pend=0
				start=0
				end=len(sales[j])
				while start<end:
					
					pend=(start+end)/2
					#print pend
					if (sales[j])[pend][4]>EndDate:
						end=pend-1
					elif (sales[j])[pend][4]==EndDate:
						while pend<end:
							if(sales[j][pend][4]==EndDate):
								pend+=1
							else:
								break
						pend-=1
						break
					else:
						start=pend+1
				indDict[j]=(pstart,pend)
				start=0
				pstart=0
				end=len(purchases[j])
				while start<end:
					pstart=(start+end)/2
					if purchases[j][pstart][10]<sales[j][indDict[j][0]][10]:
						start=pstart+1
					else:
						end=pstart
				print indDict[j]
				purchaseDict[j]=(pstart)
				productSold[j]=[sales[j][indDict[j][1]][10]-(sales[j][indDict[j][0]-1][10] if indDict[j][0]>0 else 0)]
				salesWorth=0
				purchaseWorth=0
				k=(sales[j][indDict[j][0]-1][10] if indDict[j][0]>0 else 0)
				for i in range(indDict[j][0],indDict[j][1]+1):
					salesWorth=salesWorth+sales[j][i][12]*(sales[j][i][10]-(sales[j][i-1][10] if i>0 else 0))/10
				i=indDict[j][0]
				print productSold[j]
				left=productSold[j][0]
				startPt=(sales[j][i-1][10] if i>0 else 0)
				productSold[j].append(salesWorth)	
				l=purchaseDict[j]
				print "Yo"+ str(j)+" "+str(l)
				print len(purchases[j])
				print purchases[j][l][10]
				print startPt
				while left>0:
					print int(purchases[j][l][10])-int(startPt)
					print left 
					print str(purchases[j][l][10])+" purchased"						
					if ((int(purchases[j][l][10])-int(startPt))>=int(left)):
						purchaseWorth=purchaseWorth+left*purchases[j][l][12]/10.0
						left=0
					else:
						left=left-(purchases[j][l][10]-startPt)
						purchaseWorth=purchaseWorth+(purchases[j][l][10]-startPt)*purchases[j][l][12]/10.0
						startPt=purchases[j][l][10]
					l=l+1
				productPurchased[j]=purchaseWorth
				tax=salesWorth-(salesWorth*100)/(100+purchases[j][0][15]+purchases[j][0][16])
				taxPaid=purchaseWorth-(purchaseWorth*100)/(100+purchases[j][0][15]+purchases[j][0][16])
				taxDiff=tax-taxPaid
				profit=salesWorth-purchaseWorth-taxDiff
				statistics.append((purchases[j][0][0],purchases[j][0][13],purchases[j][0][14],purchases[j][0][15],purchases[j][0][16],purchaseWorth,salesWorth,profit,taxDiff,productSold[j][0]))
		#print purchases
		stat=[]
		net=[0,0,0,0,0]
		for i in statistics:
			stat.append(statTemplate(i))
			net[0]+=stat[-1].quantity
			net[1]+=stat[-1].sale
			net[2]+=stat[-1].purchase
			net[3]+=stat[-1].profit
			net[4]+=stat[-1].tax
		return render(request,"stats.html",{"stats":stat,"net":net})
	else:
		return render(request,"stats.html")
@login_required		
def repay(request):
	if request.method=="POST":
		flag=request.POST.get("flag")	
		id=request.POST.get("id")
		paid=request.POST.get("amount")
		paid=int(paid)
		amnt=paid
		user=[]
		if flag=='0':
			data=[]
			with connection.cursor() as cursor:
				cursor.execute('select email,first_name,last_name from auth_user as a,(select * from Customer where cid=%d) as c where c.user=a.id or a.is_superuser=1;' %(int(id)))
				user=cursor.fetchall()
				cursor.execute('select * from CustomerOrder where CID=%d and (Sum-Paid-Discount)>0' %(int(id)))
				data=cursor.fetchall()
			ln=len(data)
			i=0
			with connection.cursor() as cursor:
				while paid>0 and i<ln:
					already=int(data[i][3])
					sum=int(data[i][2])
					discount=int(data[i][6])
					to_pay=min(sum-discount-already,paid)
					cursor.execute('update CustomerOrder set Paid=Paid+%d where OID=%d' %(to_pay,int(data[i][0])))
					paid=paid-to_pay
					i=i+1
			subject=("Payment received from %s %s" %(user[1][1],user[1][2]))
			message=("Received a payment of Rs %d from %s %s to settle for previous balance" %(amnt,user[1][1],user[1][2]))
			to=str(user[0][0])
			response=mail(to,message,subject)
			if response:
				return render(request,"redirect.html",{"message":"payment has been settled and mail has been sent to you"})
			else:
				return render(request,"redirect.html",{"message":"payment has been settled but mail couldn't be sent"})
		else:
			data=[]
			with connection.cursor() as cursor:
				cursor.execute('select * from SupplyOrder where SID=%d and (Sum-Paid)>0' %(int(id)))
				data=cursor.fetchall()
			ln=len(data)
			i=0
			
			with connection.cursor() as cursor:
				cursor.execute('select email,name from auth_user as a ,(select name from Supplier where uid=%d) as s where is_superuser=1;' %(int(id)))
				user=cursor.fetchall()
				while paid>0 and i<ln:
					already=int(data[i][3])
					sum=int(data[i][2])
					to_pay=min(sum-already,paid)
					cursor.execute('update SupplyOrder set Paid=Paid+%d where OID=%d' %(to_pay,int(data[i][0])))
					paid=paid-to_pay
					i=i+1
			subject=("Payment made to %s " %(user[0][1]))
			message=("A payment of Rs %d has been made to %s  to settle for previous balance" %(amnt,user[0][1]))
			to=str(user[0][0])
			response=mail(to,message,subject)
		return render(request,"redirect.html",{"message":"Settled the payment"})
	else:
		return render(request,"redirect.html",{"message":"You can't view this page right now"})

def history(request):
	data=None
	cid=0
	id=request.user.id
	with connection.cursor() as cursor:
		cursor.execute('select CID from Customer where User=%d'%(id))
		id=cursor.fetchone()
		cid=id[0]
	num=int(cid)
	with connection.cursor() as cursor:
		cursor.execute('select * from (select c.CID,a.first_name,a.last_name,c.Address,a.email from (select * from Customer where CID=%d) as c, auth_user as a where c.User=a.id) as a left join (select CID as id,sum(Sum),sum(Paid),sum(discount) from CustomerOrder where CID=%d and Approved="Y") as b on a.CID=b.id ' %(num,num)) 
		data=cursor.fetchone()
	phones=None
	if data[6] is None:
		total=0
	else:
		total=float(data[6])
	if data[7] is None:
		paid=0
	else:
		paid=float(data[7])
	if data[8] is None:
		discount=0
	else:
		discount=float(data[8])
	balance=total-paid-discount
	with connection.cursor() as cursor:
		cursor.execute('select Phone from CustomerPhones where CID=%d' %(num))
		phones=cursor.fetchall()

	customer=customerTemplate(data)
	mobiles=[]
	orders=[]
	with connection.cursor() as cursor:
		cursor.execute('select * from (select * from (select * from CustomerOrder where CID=%d) as x left join (select PID as prId,OID as ordId,Quantity from OrderRemove) as y on x.OID=y.ordId) as x,(select a.PID,a.Name,f.Type from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID) as y where x.PrId=y.PID' %(num))
		orders=cursor.fetchall()
	transactions=[]
	for i in orders:
		transactions.append(customerTransactions(i))
	for i in range(len(phones)):
		mobiles.append(phones[i][0])
	
	return render(request,'PendingCustomer.html',{"phone":mobiles,"balance":balance,"customer":customer,"transactions":transactions})

def supplierDetails(request,num):
	data=None
	num=int(num)
	with connection.cursor() as cursor:
		cursor.execute('select UID,Name,Address,Phone,(Sum-Paid) from (select * from (select * from Supplier where UID=%d) as s left join (select sum(Sum) as Sum,sum(Paid) as Paid,SID from SupplyOrder where SID=%d group by (SID)) as p on s.UID=p.SID) as x left join (select SID,min(Phone) as phone from SupplierPhones where SID=%d group by(SID)) as y on x.UID=y.SID' %(num,num,num)) 
		data=cursor.fetchone()
	Supplier=[]
	Supplier=supplier(data)
	phones=None
	with connection.cursor() as cursor:
		cursor.execute('select Phone from SupplierPhones where SID=%d' %(num))
		phones=cursor.fetchall()
	mobiles=[]
	orders=[]
	with connection.cursor() as cursor:
		cursor.execute('select * from (select * from (select * from SupplyOrder where SID=%d) as x left join (select PID as prId,OID as ordId,Quantity from OrderFill) as y on x.OID=y.ordId) as x,(select a.PID,a.Name,f.Type from Feed as f,(select p.PID,p.FID,b.Name,p.Price from Pricing as p, Brand as b where b.BID=p.BID) as a where a.FID=f.FID) as y where x.PrId=y.PID' %(num))
		orders=cursor.fetchall()
	transactions=[]
	for i in orders:
		transactions.append(supplierTransactions(i))
	for i in range(len(phones)):
		mobiles.append(phones[i][0])
	
	return render(request,'supplier_details.html',{"phone":mobiles,"supplier":Supplier,"transactions":transactions})