binPath=${rootPath}bin/
libPath=${rootPath}lib/

#Modify this variable to set the location of sonLib
sonLibRootPath=${rootPath}/../sonLib
sonLibPath=${sonLibRootPath}/lib

cactusRootPath=${rootPath}/../../

halRootPath=${rootPath}/../hal
halPath=${halRootPath}/lib

include  ${sonLibRootPath}/include.mk
ifeq (${CXX_ABI_DEF},)
    CXX_ABI_DEF = -D_GLIBCXX_USE_CXX11_ABI=1
endif

incls = -I ${sonLibPath} -I ${cactusRootPath}/api/inc -I ${halPath} ${tokyoCabinetIncl} ${kyotoTycoonIncl}

cflags += ${incls}
cppflags += ${incls} -D__STDC_LIMIT_MACROS -Wno-deprecated -std=c++11 -Wno-sign-compare
basicLibs = ${halPath}/halLib.a ${sonLibPath}/sonLib.a ${sonLibPath}/cuTest.a 
basicLibsDependencies = ${basicLibs}

# hdf5 compilation is done through its wrappers.
# we can speficy our own (sonlib) compilers with these variables:
HDF5_CXX = ${cpp}
HDF5_CXXLINKER = ${cpp}
HDF5_CC = ${cxx}
HDF5_CCLINKER = ${cxx} 
cpp = h5c++ ${h5prefix}
cxx = h5cc ${h5prefix}


cppflags += -I ../hal/api/inc  ${CXX_ABI_DEF} -std=c++11
