-- Data definition
create database if not exists parking;
-- DROP DATABASE parking;
use parking;

-- Driver table 
create table if not exists driver(
user_id int AUTO_INCREMENT not null,
first_name varchar(15) not null, 
last_name varchar(15) not null,
phone_no numeric(12) not null,
location varchar(50) not null,
no_of_people numeric(3) not null,
primary key(user_id)
);
ALTER TABLE driver AUTO_INCREMENT = 100;

-- admin table 
create table if not exists admin(
authority_id int AUTO_INCREMENT not null ,
admin_name  varchar(15) not null,
authority_post varchar(15) not null,
password varchar(15) not null,
primary key(authority_id)
);
ALTER TABLE admin AUTO_INCREMENT = 600;

-- vehicle type table
create table if not exists vehicle_type (
type_id int AUTO_INCREMENT not null,
vehicle_model varchar(20)not null,
primary key(type_id)
);
ALTER TABLE vehicle_type AUTO_INCREMENT = 20;

-- vehicle table 
create table if not exists vehicle (
vehicle_id int AUTO_INCREMENT not null,
company varchar(15)not null,
plate_no varchar(15)not null,
type_id int not null,
primary key(vehicle_id),
foreign key(type_id) references
vehicle_type(type_id)
);
ALTER TABLE vehicle AUTO_INCREMENT = 200;

-- vehicle and user  
create table if not exists transports(
parked_id int AUTO_INCREMENT not null,
user_id int not null,
vehicle_id int not null,
primary key(parked_id),
foreign key(vehicle_id) references
vehicle(vehicle_id),
foreign key(user_id) references
driver(user_id)
);
ALTER TABLE transports AUTO_INCREMENT = 300;

-- path table 
create table if not exists path(
path_id int AUTO_INCREMENT not null,
direction1 varchar(10)not null,
direction2 varchar(10),
direction3 varchar(10),
floor int not null,
primary key(path_id)
);
ALTER TABLE path AUTO_INCREMENT = 50;

-- slot and path 
create table if not exists slot(
slot_id int AUTO_INCREMENT not null,
status varchar(20)not null,
slot_type varchar(20)not null,
path_id  int not null,
primary key(slot_id),
foreign key (path_id) references 
path(path_id)
);
ALTER TABLE slot AUTO_INCREMENT = 500;

-- slot and vehicle 
create table if not exists allocates(
slot_id int not null,
vehicle_id int not null,
foreign key (slot_id) references 
slot(slot_id),
foreign key (vehicle_id) references 
vehicle(vehicle_id)
);
alter table allocates add primary key(slot_id,vehicle_id); 

-- parking table
create table if not exists parking (
ticket varchar (10) not null,
time_in varchar(15) not null,
time_out varchar(15) ,
authority_id int,
parked_id int not null,
primary key (ticket),
foreign key (authority_id) references
admin(authority_id),
foreign key (parked_id) references
transports(parked_id)
);

-- payment table
create table if not exists payment (
payment_id int auto_increment not null,
charges numeric(5,2) not null,
status varchar(10) not null,
duration numeric(10,2) not null,
authority_id int ,
ticket varchar(10) not null,
primary key (payment_id),
foreign key (authority_id) references
admin(authority_id),
foreign key(ticket) references
parking(ticket)
);
ALTER TABLE payment AUTO_INCREMENT = 1000;

-- Data manipulation

insert into driver values (101,'Shankar','Kumar',9072293668,'Alandur',2);
insert into driver values (null,'Paargav','Shankar',9072293887,'Beasant nagar',4);
insert into driver (first_name,last_name,phone_no,location,no_of_people) values ('Sergius','Infanto',9082293668,'Tambaram',3);
insert into driver values (104,'umar','ahmed',9073393668,'redrooms,tnagar',1);
insert into driver values (105,'vedanth','krishnan',9078465243,'skying india,alandur',2);
insert into driver values (106,'Usha','Varshini',9087465243,'Korattur',2);

alter table admin add column password varchar(15) not null after authority_post;
alter table admin modify password varchar(15) not null;

insert into admin  values (601,'Stark','Cheif Executive','12345');
insert into admin  (admin_name,authority_post,password) values ('Targaryen','Floor Manager','12345');
insert into admin values (603,'Lannister','floor manager','12345');
insert into admin values (604,'Bolton','Co-ordinator','12345');
insert into admin values (605,'Mormont','Co-ordinator','12345');

insert into vehicle_type values(21,'Electric Bike');
insert into vehicle_type values(22,'Two Wheelers');
insert into vehicle_type values(23,'Sedan');
insert into vehicle_type values(24,'Suv');
insert into vehicle_type values(25,'Minivan');


insert into vehicle values(201,'Nissan','TN05AD2415',23 );
insert into vehicle values(202,'Ather','TN05AD7777',21 );
insert into vehicle values(203,'renault','TN05AD1010',24 );
insert into vehicle values(204,'Triumph','TN05AD9999',21 );
insert into vehicle values(205,'Royal Enfield','TN05AD8888',22 );
insert into vehicle values(206,'skoda','TN05AD5555',25 );

insert into transports values(301,101,201);
insert into transports values(302,102,202);
insert into transports values(303,103,203);
insert into transports values(304,104,204);
insert into transports values(305,105,205);
insert into transports values(306,106,206);

insert into path values(401,'straight','2nd left','3rd right',1);
insert into path values(402,'left','3rd left','2nd right',1);
insert into path values(403,'straight','2nd left','1st left',2);
insert into path values(404,'straight','1st left','straight',3);
insert into path values(405,'straight','2st left','1st right',1);
insert into path values(406,'straight','1st right','3rd right',1);
insert into path values(407,'left','1st left','1st right',2);
insert into path values(408,'left','1st right','2nd right',2);
insert into path values(409,'left','2nd right','2nd left',2);
insert into path values(410,'left','3rd left','3rd left',2);
insert into path values(411,'left','1st left','3rd right',3);
insert into path values(412,'left','2nd left','2nd right',3);
insert into path values(413,'left','1st right','straight',3);
insert into path values(414,'left','3rd right','last left',3);
insert into path values(null,'right','1st right','last left',3);
insert into path values(null,'right','2nd right','last left',4);
insert into path values(null,'right','3rd right','last left',4);
insert into path values(null,'right','4th right','last left',4);
insert into path values(null,'right','1st right','1st left',4);
insert into path values(null,'right','1st right','2nd left',4);
insert into path values(null,'right','1st right','3rd left',4);
insert into path values(null,'right','2nd right','1st left',4);
insert into path values(null,'right','2nd right','2nd left',4);
insert into path values(null,'right','2nd right','3rd left',4);
insert into path values(null,'left','3rd right','1st left',4);
insert into path values(null,'left','3rd right','2nd left',4);
insert into path values(null,'left','3rd right','3rd left',4);
insert into path values(null,'left','4th right','3rd left',4);


insert into slot (slot_id,status,slot_type,path_id) values(501,'Occupied','Electric Bike',401);
insert into slot (status,slot_type,path_id) values('Occupied','Electric Bike',402);
insert into slot (status,slot_type,path_id) values('Occupied','Sedan',403);
insert into slot (status,slot_type,path_id) values('Unoccupied','Sedan',404);
insert into slot (status,slot_type,path_id) values('Unoccupied','Sedan',405);
insert into slot (status,slot_type,path_id) values('Occupied','Two Wheelers',406);
insert into slot (status,slot_type,path_id) values('Unoccupied','Two Wheelers',407);
insert into slot (status,slot_type,path_id) values('Unoccupied','Two Wheelers',408);
insert into slot (status,slot_type,path_id) values('Occupied','Suv',409);
insert into slot (status,slot_type,path_id) values('Unoccupied','Suv',410);
insert into slot (status,slot_type,path_id) values('Unoccupied','Suv',411);
insert into slot (status,slot_type,path_id) values('Occupied','Minivan',412);
insert into slot (status,slot_type,path_id) values('Unoccupied','Minivan',413);

insert into slot (status,slot_type,path_id) values('Unoccupied','Electric Bike',414);
insert into slot (status,slot_type,path_id) values('Unoccupied','Electric Bike',415);
insert into slot (status,slot_type,path_id) values('Unoccupied','Electric Bike',416);
insert into slot (status,slot_type,path_id) values('Unoccupied','Two Wheelers',417);
insert into slot (status,slot_type,path_id) values('Unoccupied','Two Wheelers',418);
insert into slot (status,slot_type,path_id) values('Unoccupied','Two Wheelers',419);
insert into slot (status,slot_type,path_id) values('Unoccupied','Sedan',420);
insert into slot (status,slot_type,path_id) values('Unoccupied','Sedan',421);
insert into slot (status,slot_type,path_id) values('Unoccupied','Sedan',422);
insert into slot (status,slot_type,path_id) values('Unoccupied','Suv',423);
insert into slot (status,slot_type,path_id) values('Unoccupied','Suv',424);
insert into slot (status,slot_type,path_id) values('Unoccupied','Suv',425);
insert into slot (status,slot_type,path_id) values('Unoccupied','Minivan',426);
insert into slot (status,slot_type,path_id) values('Unoccupied','Minivan',427);
insert into slot (status,slot_type,path_id) values('Unoccupied','Minivan',428);

insert into allocates values(501,202);
insert into allocates values(502,204);
insert into allocates values(506,205);
insert into allocates values(503,201);
insert into allocates values(509,203);
insert into allocates values(512,206);


insert into parking values('CF101','21:00:00','22:00:00',601,301);
insert into parking values('SF225','18:00:00','21:00:00',602,302);
insert into parking values('AF312','02:00:00','04:00:00',603,303);
insert into parking values('BF406','16:15:26',null,null,304);
insert into parking values('HF528','12:00:01',null,null,305);
insert into parking values('DF639','12:30:06','13:45:29',603,306);


insert into payment values(901,30.00,'paid','60',601,'CF101');
insert into payment values(902,90.00,'paid','180',603,'SF225');
insert into payment values(903,60.00,'paid','120',602,'AF312');
insert into payment values(904,37.80,'unpaid','75',null,'DF639');

commit;





