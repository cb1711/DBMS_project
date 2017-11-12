
create table if not exists Customer (CID INT NOT NULL AUTO_INCREMENT,
       	     		  Address VARCHAR(50),
			  		  User INT,
			  		  PRIMARY KEY(CID),
			 		  FOREIGN KEY(User) REFERENCES auth_user(id));

/* Create table for customer phone numbers*/
create table if not exists CustomerPhones(CID INT,
       	     			     Phone CHAR(10),
				     		 FOREIGN KEY(CID) REFERENCES Customer(CID) on delete cascade,
				     		 PRIMARY KEY(CID,Phone));
				

/*Create table for suppliers */
create table if not exists Supplier(UID INT NOT NULL AUTO_INCREMENT,
       	     		  Name VARCHAR(30),
			  		  Address VARCHAR(50),
			 		  PRIMARY KEY(UID));


/* Create table for customer phone numbers*/
create table if not exists SupplierPhones(SID INT,
       	     			Phone CHAR(10),
			     		FOREIGN KEY(SID) REFERENCES Supplier(UID) on delete cascade,
						PRIMARY KEY(SID,Phone));
				
/*Create table for feed types*/
create table if not exists Feed(FID INT NOT NULL AUTO_INCREMENT,
       	     	      S_GST FLOAT,
		      		  C_GST FLOAT,
		      		  Type CHAR(20),
		      		  PRIMARY KEY(FID));

/*Create table for brands*/
create table if not exists Brand(BID INT NOT NULL AUTO_INCREMENT,
       	     	       Name VARCHAR(30),
		       		   Phone CHAR(10),
		       		   Address VARCHAR(50),
		       		   PRIMARY KEY(BID));


/*Create table for pricing of feed*/
create table if not exists Pricing(PID INT NOT NULL AUTO_INCREMENT,
       	     		 FID INT,
			 		 BID INT,
			 		 Price INT default=0,
				 	 PRIMARY KEY(PID),
					 FOREIGN KEY(FID) REFERENCES Feed(FID) on delete restrict,
				 	 FOREIGN KEY(BID) REFERENCES Brand(BID) on delete restrict);

/*Create table for Godown*/
create table if not exists Godown(GodownNum INT NOT NULL AUTO_INCREMENT,
       	     		      Capacity INT,
			      Address VARCHAR(50),
			      PRIMARY KEY(GodownNum));

/*Customer Order*/
create table if not exists CustomerOrder(OID INT NOT NULL AUTO_INCREMENT,
       	     		      CID INT,
			      Sum INT,
			      Paid INT,
			      Date DATE,
			      Time TIME,
			      Discount FLOAT,
				  Approved CHAR(1) default='N';
			      PRIMARY KEY(OID),
			      FOREIGN KEY(CID) REFERENCES Customer(CID) on delete restrict);

/*Order Line*/
create table if not exists OrderRemove(OID INT,
       	     		     PID INT,
			     		Quantity INT,
			     		GID INT,
						Rate FLOAT default 0,
						PRIMARY KEY(OID,PID),
			     		FOREIGN KEY(PID) REFERENCES Pricing(PID) on delete restrict,
			     		FOREIGN KEY(OID) REFERENCES CustomerOrder(OID) on delete cascade,
			     		FOREIGN KEY(GID) REFERENCES Godown(GodownNum) on delete restrict);

/*Create table for Occupied */
/*
create table if not exists Occupied(Serial INT NOT NULL AUTO_INCREMENT,
			    GNum INT,
       	     	Capacity INT,
			    Feed INT,
			    PRIMARY KEY(Serial),
			    FOREIGN KEY(Feed) REFERENCES Pricing(PID) on delete cascade,
			    FOREIGN KEY(GNum) REFERENCES Godown(GodownNum) on delete cascade);
*/

/*Supply Order*/
create table if not exists SupplyOrder(OID INT NOT NULL AUTO_INCREMENT,
       	     		      SID INT,
			      Sum INT,
			      Paid INT,
			      Date DATE,
			      Time TIME,
			      DateExpected DATE,
				  Loading INT,
				  Transport INT,
			      PRIMARY KEY(OID),
			      FOREIGN KEY(SID) REFERENCES Supplier(UID) on delete restrict);

/*Order Line for Supply order*/
create table if not exists OrderFill(OID INT,
       	     		   PID INT,
			     	   Quantity INT,
			     	   GID INT,
					   Cost FLOAT,
					   PRIMARY KEY(OID,PID),
			           FOREIGN KEY(PID) REFERENCES Pricing(PID) on delete restrict,
			           FOREIGN KEY(OID) REFERENCES SupplyOrder(OID) on delete cascade,
			     	   FOREIGN KEY(GID) REFERENCES Godown(GodownNum) on delete cascade);

delimiter //

create trigger balanceCheck before insert on CustomerOrder for each row if new.Paid>new.Sum+new.Discount then set new.Paid=new.Sum+new.Discount; end if ;//

create trigger balanceUpdate before update on CustomerOrder for each row if new.Paid>new.Sum+new.Discount then set new.Paid=new.Sum+new.Discount; end if ;//

create trigger purchaseCheck before insert on SupplyOrder for each row if new.Paid>new.Sum then set new.Paid=new.Sum; end if ;// 

create trigger purchaseUpdate before update on SupplyOrder for each row if new.Paid>new.Sum then set new.Paid=new.Sum; end if ;//

delimiter ;
