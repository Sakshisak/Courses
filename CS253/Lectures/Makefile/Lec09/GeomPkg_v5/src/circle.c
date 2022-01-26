#include<circle.h>
// const double PI=3.14159;
#include<math.h>

float circ_area(Circle *c) {
	return M_PI * c->rad * c->rad;
}

float circ_perimtr(Circle *c) {
	return 2 * M_PI * c->rad;
}
