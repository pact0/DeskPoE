cmake_minimum_required(VERSION 3.5)

project(DeskPoe)

message(${CMAKE_SYSTEM_NAME})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

set(CMAKE_INSTALL_PREFIX ${PROJECT_SOURCE_DIR})
set(INSTALL_LIB_DIR ${PROJECT_SOURCE_DIR}/lib)
set(EXTERNALS_DIR ${PROJECT_SOURCE_DIR}/externals)
set(ROOT_SRC_DIR ${PROJECT_SOURCE_DIR}/src)

set(QT_VERSION 6)


include_directories(${INSTALL_LIB_DIR})

if(WIN32)
    set(CMAKE_PREFIX_PATH "${INSTALL_LIB_DIR}/Qt6/lib/cmake")
    add_subdirectory(${INSTALL_LIB_DIR}/SpdLog)
    include_directories(${INSTALL_LIB_DIR}/SpdLog/include)
elseif(UNIX AND NOT APPLE)
    message("Make sure you have installed needed packages")
    find_package(spdlog REQUIRED)
elseif(APPLE)
    message(FATAL_ERROR "Not supported OS")
endif()


add_subdirectory(${INSTALL_LIB_DIR}/googletest)

add_subdirectory(${INSTALL_LIB_DIR}/BoostConfig)
add_subdirectory(${INSTALL_LIB_DIR}/BoostAssert)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostDateTime)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostException)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostSpirit)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostArray)
add_subdirectory(${INSTALL_LIB_DIR}/BoostStaticAssert)
add_subdirectory(${INSTALL_LIB_DIR}/BoostCore)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostEndian)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostFunction)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostBind)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostFunctionTypes)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostPreprocessor)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostFusion)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostAlgorithm)
add_subdirectory(${INSTALL_LIB_DIR}/BoostThrowException)
#add_subdirectory(${INSTALL_LIB_DIR}/BoostSmartPtr)



add_subdirectory(src)
add_subdirectory(test)


