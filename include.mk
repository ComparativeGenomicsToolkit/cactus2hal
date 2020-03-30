BINDIR=${rootPath}bin/
LIBDIR=${rootPath}lib/

#Modify this variable to set the location of sonLib
sonLibRootDir=${rootPath}/../sonLib
sonLibDir=${sonLibRootDir}/lib

cactusRootPath=${rootPath}/../../

halRootPath=${rootPath}/../hal
halPath=${halRootPath}/lib

include  ${sonLibRootDir}/include.mk
ifeq (${CXX_ABI_DEF},)
    CXX_ABI_DEF = -D_GLIBCXX_USE_CXX11_ABI=1
endif

incls = -I ${sonLibDir} -I ${cactusRootPath}/api/inc -I ${halPath} ${tokyoCabinetIncl} ${kyotoTycoonIncl}

CFLAGS += ${incls}
CXXFLAGS += ${incls} -D__STDC_LIMIT_MACROS -Wno-deprecated -std=c++11 -Wno-sign-compare
LDLIBS = ${halPath}/halLib.a ${sonLibDir}/sonLib.a ${sonLibDir}/cuTest.a 
LIBDEPENDS = ${LDLIBS}

# hdf5 compilation is done through its wrappers.
# we can speficy our own (sonlib) compilers with these variables:
CXX = h5c++ ${h5prefix}
CC = h5cc ${h5prefix}


CXXFLAGS += -I ../hal/api/inc  ${CXX_ABI_DEF} -std=c++11
