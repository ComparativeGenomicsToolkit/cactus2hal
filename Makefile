rootPath = ./
include ./include.mk

libSources = src/*.cpp
EXCLUDE=$(subst src/halAppendCactusSubtree.cpp,,${libSources})
libHeaders = inc/*.h 
libTests = tests/*.cpp
libTestsHeaders = tests/*.h 

all : ${LIBDIR}/cactus2halLib.a ${BINDIR}/halAppendCactusSubtree ${BINDIR}/cactus2hal.py #${BINDIR}/importCactusTests 

clean : 
	rm -f ${LIBDIR}/cactus2halLib.a ${BINDIR}/halAppendCactusSubtree ${BINDIR}/cactus2hal.py ${BINDIR}/importCactusTests *.o

test: all
#	${PYTHON} tests/allTests.py

${LIBDIR}/cactus2halLib.a : ${libSources} ${libHeaders} ${LIBDEPENDS} 
	${CXX} ${CPPFLAGS} ${CXXFLAGS} -I inc -I src -c ${libSources}
	${AR} rc cactus2halLib.a *.o
	${RANLIB} cactus2halLib.a 
	mv cactus2halLib.a ${LIBDIR}/

${BINDIR}/halAppendCactusSubtree : ${LIBDIR}/cactus2halLib.a src/halAppendCactusSubtree.cpp
	${CXX} ${CPPFLAGS} ${CXXFLAGS} ${LDFLAGS} -I inc -I src -o ${BINDIR}/halAppendCactusSubtree src/halAppendCactusSubtree.cpp ${LIBDIR}/cactus2halLib.a ${LDLIBS} ${LIBS}

${BINDIR}/cactus2hal.py : src/cactus2hal.py
	cp src/cactus2hal.py ${BINDIR}/cactus2hal.py
	chmod +x ${BINDIR}/cactus2hal.py
