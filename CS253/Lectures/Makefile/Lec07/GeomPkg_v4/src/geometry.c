#include <circle.h>
#include <triangle.h>
#include <stdio.h>

#ifdef TRI
float tri_area(Triangle *t) {
	printf("I am using an alternate area computation\n");
	return 0;
}
#endif
int main() {
	Circle c1;
	Triangle t1;

	printf("Radius of the circle? ");
	scanf("%f", &c1.rad);


	// printf("3 sides of the triangle? ");
	// scanf("%f", &t1.a);
	// scanf("%f", &t1.b);
	// scanf("%f", &t1.c);
	read_triangle(&t1);

	printf(" The area of circle is %f and its perimeter is %f\n",
			circ_area(&c1), circ_perimtr(&c1));
	printf(" The area of triangle is %f and its perimeter is %f\n",
			tri_area(&t1), tri_perimtr(&t1));

	return 0;
}
