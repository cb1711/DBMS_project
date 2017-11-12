
profit=5.0
class salesTemplate:
	def __init__(self,li):
		self.pid=li[0]
		self.brand=li[4]
		self.type=li[5]
		cost=li[7]
		extra=li[8]+li[9]
		self.s_gst=li[3]
		self.c_gst=li[2]
		self.stock=li[10]
		price=(float(cost)+float(extra))*(1+profit/100)*(1+(self.s_gst+self.c_gst)/100)
		if price ==0:
			price=li[1]
		self.price=price
		if len(li)>11:
			self.Address=li[11]
			self.phone=li[12]
	def __str__(self):
		return self.brand+" "+self.type	

class productTemplate:
	def __init__(self,li):
		self.pid=li[0]
		self.brand=li[1]
		self.type=li[2]
		self.price=li[3]
		self.C_GST=li[4]
		self.S_GST=li[5]
		if len(li)>6:
			cost=li[9]
			extras=li[6]+li[7]
			if cost is not None:
				self.price=(cost+extras)*(1+profit/100)*(1+(self.C_GST+self.S_GST)/100)


	def __str__(self):
		return self.brand +" "+ self.type


class customerTemplate:
	def __init__(self,li):
		self.id=li[0]
		self.FName=li[1]
		self.LName=li[2]	
		self.email=li[4]
		self.address=li[3]

	def __str__(self):
		return self.FName+" "+self.LName
class godownTemplate:
	def __init__(self,li):
		self.id=li[0]
		self.capacity=li[1]
		self.address=li[2]
		self.occupied=li[3]

	def __str__(self):
		return self.id+" "+self.capacity

class supplierTemplate:
	def __init__(self,li):
		self.id=li[0]
		self.name=li[1]
		self.address=li[2]
		if len(li)>3:
			sum=li[3]
			if sum is None:
				sum=0
			paid=li[4]
			if paid is None:
				paid=0
			self.balance=float(sum)-float(paid)
			self.phone=li[7]
	def __str__(self):
		return self.name+" "+self.address

class customerCompleteTemplate:
	def __init__(self,li):
		self.id=li[0]
		self.FName=li[1]
		self.LName=li[2]
		self.address=li[3]
		self.email=li[4]
		self.phone=li[5]
		
		total=li[8]
		paid=li[9]
		discount=li[10]
		if total==None:
			total=0	
		if paid==None:
			paid=0
		if discount==None:
			discount=0
		self.balance=float(total)-float(paid)-float(discount)
	def __str__(self):
		return self.FName+" "+self.LName
class completeProductDetail:
	def __init__(self,li):
		self.id=li[0]
		self.brand=li[3]
		self.cAddress=li[4]
		self.price=li[5]
		self.type=li[6]
		self.sgst=li[7]
		self.cgst=li[8]
		self.phone=li[9]

class customerTransactions:
	def __init__(self,li):
		self.OrderID=li[0]
		self.CustomerID=li[1]
		self.Sum=li[2]
		self.Paid=li[3]
		self.Date=li[4]
		self.Time=li[5]
		self.Discount=li[6]
		self.Quantity=li[9]
		self.Brand=li[11]
		self.Type=li[12]


class brandTemplate:
	def __init__(self,li):
		self.bid=li[0]
		self.name=li[1]
		self.phone=li[2]
		self.address=li[3]

class feedTemplate:
	def __init__(self,li):
		self.fid=li[0]
		self.type=li[3]
		self.sgst=li[1]
		self.cgst=li[2]
class approveTemplate:
	def __init__(self,li):
		self.oid=li[0][0]
		self.customer=li[0][3]+" "+li[0][4]
		self.date=li[0][1]
		self.address=li[0][6]
		self.sum=li[0][5]
		self.time=li[0][2]
		self.products=[]
		for i in li:
			self.products.append(i[7]+" "+i[8]+"  Quantity-"+ str(i[9]))
class statTemplate:
	def __init__(self,li):
		self.pid=li[0]
		self.brand=li[1]
		self.type=li[2]
		self.cgst=li[3]
		self.sgst=li[4]
		self.purchase=round(li[5],2)
		self.sale=round(li[6],2)
		self.profit=round(li[7],2)
		self.tax=round(li[8],2)
		self.quantity=li[9]
class balance:
	def __init__(self,li):
		self.cid=li[0]
		self.name=li[1]+" "+li[2]
		self.address=li[3]
		self.phone=li[4]
		self.balance=li[5]
class supplier:
	def __init__(self,li):
		self.sid=li[0]
		self.name=li[1]
		self.address=li[2]
		self.phone=li[3]
		self.balance=li[4]

class supplierTransactions:
	def __init__(self,li):
		self.OrderID=li[0]
		self.SupplierID=li[1]
		self.Sum=li[2]
		self.Paid=li[3]
		self.Date=li[4]
		self.Time=li[5]
		self.Expected=li[6]
		self.Loading=li[7]
		self.Transport=li[8]
		self.Quantity=li[11]
		self.Brand=li[13]
		self.Type=li[14]
