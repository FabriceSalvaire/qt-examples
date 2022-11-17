cmake_minimum_required(VERSION 3.15)

project(app VERSION 0.1 LANGUAGES CXX)

# set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOMOC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6
  COMPONENTS
  Concurrent
  Core
  Network
  Widgets
  REQUIRED
)

set(PROJECT_SOURCES
  main.cpp
  DownloadManager.cpp
  DownloadManagerQueue.cpp
)

add_executable(${PROJECT_NAME}
  # MANUAL_FINALIZATION
  ${PROJECT_SOURCES}
)

# target_compile_definitions(${PROJECT_NAME}
#   PRIVATE $<$<OR:$<CONFIG:Debug>,$<CONFIG:RelWithDebInfo>>:QT_QML_DEBUG>)

target_link_libraries(${PROJECT_NAME}
  PRIVATE
  Qt6::Concurrent
  Qt6::Core
  Qt6::Network
  Qt6::Widgets
)

# set_target_properties(${PROJECT_NAME} PROPERTIES
#   MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
#   MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
#   MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
# )

# qt_import_qml_plugins(${PROJECT_NAME})
# qt_finalize_executable(${PROJECT_NAME})
