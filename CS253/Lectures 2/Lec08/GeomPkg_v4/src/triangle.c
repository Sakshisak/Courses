#include<triangle.h>
#include<math.h>
#include<stdlib.h>
#include<stdio.h>

static void swap(float *v1, float *v2) {
	float tmp = *v1;
	*v1 = *v2;
	*v2 = tmp;
	return;
}

void read_triangle(Triangle *t) {
	// These will be kept in sorted order: s1 < s2 < s3
	float s1, s2, s3;
	printf("3 sides of triangle? ");
	scanf("%f", &t->a);
	s1 = t->a;

	scanf("%f", &t->b);
	s2 = t->b;
	if (s2 < s1) swap(&s1, &s2);

	scanf("%f", &t->c);
	s3 = t->c;
	if (s3 < s1) swap(&s1, &s3);
	if (s3 < s2) swap(&s2, &s3);

	// validate
	if (s1 + s2 <= s3) {
		fprintf(stderr, "Invalid Triangle. Try Again\n");
		exit(-1); // Can we again read_triangle(t);
	}
	return;
}

float tri_area(Triangle *t) {
	float s = tri_perimtr(t)/2.0;
	float peri_sq = s * (s - t->a) * (s - t->b) * (s - t->c);
	return sqrt(peri_sq);
}

float tri_perimtr(Triangle *t) {
	return t->a + t-> b + t->c;
}
