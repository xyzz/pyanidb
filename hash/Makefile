CC=gcc
CFLAGS=
CPP=g++
CPPFLAGS=
LD=gcc
LDFLAGS=-shared

OBJECTS=hash_wrapper.o hash.o crc32.o ed2k.o
TARGET=_hash.so
INCLUDE=-I /usr/include/python2.4/
LIB=-l boost_python -l ssl

all: $(TARGET)

clean:
	-rm $(TARGET) $(OBJECTS)

# Mål-regel
$(TARGET): $(OBJECTS) Makefile
	$(LD) $(LDFLAGS) -o $(TARGET) $(OBJECTS) $(LIB)

# Pseudoregler
%.o: %.c Makefile
	$(CC) $(CFLAGS) -o $@ -c $< $(INCLUDE)

%.o: %.cpp Makefile
	$(CPP) $(CPPFLAGS) -o $@ -c $< $(INCLUDE)