CC=gcc
INC=include
SRC=src
OBJ=obj
LIB=lib
BIN=bin

.PHONY: all clean realclean

HDRS=$(shell ls $(INC)/*.h)
all: $(BIN)/geometry

$(BIN)/geometry: $(OBJ)/geometry.o $(OBJ)/donut.o $(LIB)/libGeom.so
	$(CC) -o $@ -I$(INC) $< -L$(LIB) -lGeom -lm

$(OBJ)/geometry.o: $(SRC)/geometry.c $(HDRS)
	$(CC) -c -I$(INC) $< -o $@

$(OBJ)/donut.o: $(SRC)/donut.c $(INC)/donut.h $(INC)/circle.h
	$(CC) -c -I$(INC) $< -o $@

$(OBJ)/%.o: $(SRC)/%.c $(INC)/%.h 
	$(CC) -fPIC -c -I$(INC) $< -o $@

$(LIB)/libGeom.so: $(OBJ)/circle.o $(OBJ)/triangle.o
	gcc -shared -o $@ $^ -lm

clean:
	$(RM) $(OBJ)/*.o $(LIB)/libGeom.*

realclean: clean
	$(RM) $(BIN)/geometry $(OBJ)/*.o $(LIB)/libGeom.*
