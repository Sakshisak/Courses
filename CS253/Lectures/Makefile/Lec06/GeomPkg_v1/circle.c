#include<circle.h>
int main(){
const double PI=3.14;

scanf("%d",&c );

float circ_area(Circle *c) {
	return PI * c->rad * c->rad;
}

float circ_perimtr(Circle *c) {
	return 2 * PI * c->rad;
}
}
