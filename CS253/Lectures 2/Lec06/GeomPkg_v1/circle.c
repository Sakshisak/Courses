#include<circle.h>
const double PI=3.14;

float circ_area(Circle *c) {
	return PI * c->rad * c->rad;
}

float circ_perimtr(Circle *c) {
	return 2 * PI * c->rad;
}
