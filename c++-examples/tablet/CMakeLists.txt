cmake_minimum_required(VERSION 3.15)

project(test-tablet)

find_package(Qt6
  COMPONENTS
  Quick
  REQUIRED
)

add_executable(${PROJECT_NAME}
  main.cpp
  tabletcanvas.cpp
  tabletwindow.cpp
)

qt6_add_resources(${PROJECT_NAME} "qml_files"
  PREFIX "/"
  FILES
  main.qml
)

target_link_libraries(${PROJECT_NAME}
  PRIVATE
  Qt6::Quick
)
