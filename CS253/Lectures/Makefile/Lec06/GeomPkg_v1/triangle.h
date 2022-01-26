
typedef struct _triangle Triangle;

struct _triangle {
	float a;
	float b;
	float c;
};

float tri_area(Triangle *t);
float tri_perimtr(Triangle *t);
