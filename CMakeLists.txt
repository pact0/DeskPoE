cmake_minimum_required(VERSION 3.5)

project(DeskPoe)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

message(${CMAKE_SYSTEM_NAME})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


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

#set(INSTALL_LIB_BOOST_DIR ${INSTALL_LIB_DIR}/BoostModules)
#
#file(GLOB SUBDIRECTORIES RELATIVE ${INSTALL_LIB_BOOST_DIR} "${INSTALL_LIB_BOOST_DIR}/*")
#foreach(SUBDIR ${SUBDIRECTORIES})
#    if(IS_DIRECTORY "${INSTALL_LIB_BOOST_DIR}/${SUBDIR}")
#        add_subdirectory(${INSTALL_LIB_BOOST_DIR}/${SUBDIR})
#        message(STATUS "Added Boost module: ${SUBDIR}")
#    endif()
#endforeach()



add_subdirectory(src)



add_subdirectory(test)


