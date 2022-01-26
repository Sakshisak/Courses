.mode column
.header on

select *
from student;

select *
from student
where name like "Ra%";

select *
from student
where dept = 12
order by name;

select dept, count(roll)
from student
group by dept;

select code, max(yr)
from offering
group by code
having count(yr) > 1;

select dept, count(roll)
from student
where name like "Ra%"
group by dept;

select *
from student, department;

select *
from student, department
where student.dept = department.dept;

select *
from registration natural join offering;

select *
from registration, offering
where registration.code = offering.code;

select *
from registration join offering on registration.code = offering.code;

