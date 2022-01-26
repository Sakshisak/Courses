all: geometry

geometry: obj/geometry.o obj/triangle.o obj/circle.o
	$(CC) -o geometry -Iinclude $^ -lm

obj/geometry.o: src/geometry.c include/circle.h include/triangle.h
	$(CC) -o obj/geometry.o -c -Iinclude src/geometry.c

obj/circle.o: src/circle.c include/circle.h 
	$(CC) -o obj/circle.o -c -Iinclude src/circle.c

obj/triangle.o: src/triangle.c include/triangle.h 
	$(CC) -o obj/triangle.o -c -Iinclude src/triangle.c
