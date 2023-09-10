
set(SOURCE_FILES main.cpp qml.qrc userSettings/SettingsManager.cpp authorization/redditwrapper.cpp authorization/redditmodel.cpp)



set(REQUIRED_LIBS Gui Qml Quick Widgets NetworkAuth)
set(REQUIRED_LIBS_QUALIFIED Qt6::Core
        Qt6::Gui
        Qt6::Quick
        Qt6::Qml
        Qt6::Widgets
        Qt6::NetworkAuth

        )
find_package(Qt${QT_VERSION} COMPONENTS ${REQUIRED_LIBS} REQUIRED)


add_executable(deskPoeTarget ${SOURCE_FILES})

if(WIN32)
    target_link_libraries(deskPoeTarget ${REQUIRED_LIBS_QUALIFIED} spdlog::spdlog)
elseif(UNIX AND NOT APPLE)
    target_link_libraries(deskPoeTarget ${REQUIRED_LIBS_QUALIFIED} spdlog::spdlog_header_only)
elseif(APPLE)
    message(FATAL_ERROR "Not supported OS")
endif()
