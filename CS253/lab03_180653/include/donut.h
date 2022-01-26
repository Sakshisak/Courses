#include<circle.h>

typedef struct _donut donut;
struct _donut{
	Circle inner;
	Circle outer;
};

void read_donut(donut *d);
float donut_area(donut *d);
float donut_peri(donut *d);
int a;


