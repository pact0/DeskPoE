set(SOURCE_FILES main.cpp)

set(REQUIRED_LIBS Core Gui Widgets)
set(REQUIRED_LIBS_QUALIFIED Qt6::Core Qt6::Gui Qt6::Widgets)
find_package(Qt${QT_VERSION} COMPONENTS ${REQUIRED_LIBS} REQUIRED)

add_executable(deskPoeTarget ${SOURCE_FILES})

if(WIN32)
    target_link_libraries(deskPoeTarget ${REQUIRED_LIBS_QUALIFIED} Boost::core spdlog::spdlog)
elseif(UNIX AND NOT APPLE)
    target_link_libraries(deskPoeTarget ${REQUIRED_LIBS_QUALIFIED} Boost::core spdlog::spdlog_header_only)
elseif(APPLE)
    message(FATAL_ERROR "Not supported OS")
endif()



