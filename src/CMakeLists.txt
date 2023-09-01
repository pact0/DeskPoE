set(SOURCE_FILES main.cpp)

set(REQUIRED_LIBS Core Gui Widgets)
set(REQUIRED_LIBS_QUALIFIED Qt6::Core Qt6::Gui Qt6::Widgets)
find_package(Qt${QT_VERSION} COMPONENTS ${REQUIRED_LIBS} REQUIRED)

add_executable(deskPoeTarget ${SOURCE_FILES})
target_link_libraries(deskPoeTarget ${REQUIRED_LIBS_QUALIFIED} Boost::core)
