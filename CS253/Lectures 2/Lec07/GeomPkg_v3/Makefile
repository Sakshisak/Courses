geometry: obj/geometry.o obj/triangle.o obj/circle.o
	gcc -o geometry -Iinclude obj/geometry.o obj/triangle.o obj/circle.o -lm

obj/geometry.o: src/geometry.c include/circle.h include/triangle.h
	gcc -o obj/geometry.o -c -Iinclude src/geometry.c

obj/circle.o: src/circle.c include/circle.h 
	gcc -o obj/circle.o -c -Iinclude src/circle.c

obj/triangle.o: src/triangle.c include/triangle.h 
	gcc -o obj/triangle.o -c -Iinclude src/triangle.c


