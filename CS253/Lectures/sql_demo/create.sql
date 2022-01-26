drop table if exists department;
create table department(dept integer primary key, name varchar(50) not null);

--drop table if exists coursetype;
--create table coursetype(ctype integer primary key, dept integer not null, foreign key (dept) references department(deptid));

--drop table if exists course;
--create table course(code varchar(8) primary key, title varchar(50) not null, ctype integer not null, webpage varchar(50), foreign key (ctype) references coursetype(ctype));

drop table if exists course;
create table course(code varchar(8) primary key, title varchar(50) not null, units integer not null, webpage varchar(50));

drop table if exists faculty;
create table faculty(fid integer primary key, name varchar(50) not null, dept integer not null, designation varchar(3) not null default "AP", foreign key (dept) references department(dept));

--drop table if exists semester;
--create table semester(yr integer not null, half integer not null, primary key(yr, half));

drop table if exists student;
create table student(roll integer primary key, name varchar(50) not null, dept integer not null, foreign key (dept) references department(dept));

--drop table if exists program;
--create table program(roll integer not null, ptype varchar(8) not null, primary key(roll), foreign key (roll) references student(roll));

drop table if exists offering;
create table offering(code varchar(8) not null, yr integer not null, half integer not null, instructor integer not null, primary key(code, yr, half, instructor), foreign key (code) references course(code), foreign key (yr, half) references semester(yr, half), foreign key (instructor) references faculty(fid));

--drop table if exists grade;
--create table grade(gradecode char(1) primary key, value integer not null, check (value >= 0), check (value < 10));

drop table if exists registration;
create table registration(code varchar(8) not null, roll integer not null, yr integer not null, half integer not null, gradecode char(1), primary key(code, roll), foreign key (code) references course(code), foreign key (roll) references student(roll), foreign key (yr, half) references semester(yr, half), foreign key (gradecode) references grade(gradecode));

--drop table if exists cpi;
--create table cpi(roll integer primary key, cpi real, foreign key (roll) references student(roll));

