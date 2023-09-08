include_directories(${ROOT_SRC_DIR})
include_directories(${DIVISIBLE_INSTALL_LIB_DIR}/googletest/googletest/include)

add_executable(exampleTest main.cpp src/exampleTest.cpp)
target_link_libraries(exampleTest gtest)
