cmake_minimum_required(VERSION 3.19)
project(app LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)

# if(NOT DEFINED INSTALL_EXAMPLESDIR)
#   set(INSTALL_EXAMPLESDIR "examples")
# endif()

# set(INSTALL_EXAMPLEDIR "${INSTALL_EXAMPLESDIR}/demos/touch")

# https://doc.qt.io/qt-5/qtquick-debugging.html
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DQT_QML_DEBUG -DQT_DECLARATIVE_DEBUG")
add_definitions(-DQT_QML_DEBUG)
add_definitions(-DQT_DECLARATIVE_DEBUG)

find_package(Qt6 REQUIRED COMPONENTS
  Core
  Gui
  Qml
  Quick
)

qt_add_executable(${PROJECT_NAME} WIN32 MACOSX_BUNDLE
  main.cpp
)

target_link_libraries(${PROJECT_NAME} PRIVATE
  Qt6::Core
  Qt6::Gui
  Qt6::Qml
  Qt6::Quick
)

# https://doc-snapshots.qt.io/qt6-dev/qt-add-qml-module.html
qt_add_qml_module(${PROJECT_NAME}
  URI touch
  VERSION 1.0
  QML_FILES
  "touch.qml"
  # RESOURCES
)

# install(TARGETS ${PROJECT_NAME}
#   RUNTIME DESTINATION "${INSTALL_EXAMPLEDIR}"
#   BUNDLE DESTINATION "${INSTALL_EXAMPLEDIR}"
#   LIBRARY DESTINATION "${INSTALL_EXAMPLEDIR}"
# )

if(ANDROID)
  MESSAGE("Build on Android")

  # https://doc.qt.io/qt-6/qt-android-add-apk-target.html
  # Generates the deployment settings file needed by androiddeployqt
  qt_android_generate_deployment_settings(${PROJECT_NAME})
  # Defines a build target that runs androiddeployqt to produce an APK
  qt_android_add_apk_target(${PROJECT_NAME})

  # https://doc.qt.io/qt-6/qt-android-apply-arch-suffix.html
  # Configures the target binary's name to include an architecture-specific suffix
  # qt_android_apply_arch_suffix(${PROJECT_NAME})

  # Handles various common platform-specific tasks associated with Qt targets
  # qt_finalize_target(${PROJECT_NAME})
endif(ANDROID)
