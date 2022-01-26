//#include<circle.h>
#include<donut.h>
#include<math.h>
#include <stdio.h>

void read_donut(donut *d){
	float ri, ro;
	printf("Enter radius of inner cricle");
	scanf("%f",&ri);
	scanf("%f",&ro);
	if(ri>=ro){
	printf("ERROR: inner radius should be smaller than outer radius\n");
	return;}
	
	d->outer.rad = ro;
	d->inner.rad = ri;
	return;
}

float donut_area(donut *d){
	Circle c1,c2;
	c1 = d->inner;
	c2 = d->outer;
	float area = circ_area(&c2) - circ_area(&c2);
	return area;
}

float donut_peri(donut *d){
	float peri = circ_perimtr(&d->outer) + circ_perimtr(&d->inner);
	return peri;
}
