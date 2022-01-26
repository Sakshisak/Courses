#include<circle.h>
#include<math.h>

float circ_area(Circle *c) {
	return M_PI * c->rad * c->rad;
}

float circ_perimtr(Circle *c) {
	return 2 * M_PI * c->rad;
}
