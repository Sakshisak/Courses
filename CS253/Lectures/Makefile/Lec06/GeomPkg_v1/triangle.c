#include<triangle.h>
#include<math.h>

float tri_area(Triangle *t) {
	float s = tri_perimtr(t)/2.0;
	float peri_sq = s * (s - t->a) * (s - t->b) * (s - t->c);
	return sqrt(peri_sq);
}

float tri_perimtr(Triangle *t) {
	return t->a + t-> b + t->c;
}
