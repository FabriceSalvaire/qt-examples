## Copyright (C) 2022 Fabrice Salvaire
## SPDX-License-Identifier: GPL-3.0-only

####################################################################################################
#
# To get full output use
#   make VERBOSE=1
#
####################################################################################################

cmake_minimum_required(VERSION 3.16)
project(scenegraph LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

####################################################################################################

find_package(Qt6 COMPONENTS
  Core
)

####################################################################################################

qt_add_executable(app
    main.cpp
)
target_link_libraries(app PUBLIC
    Qt::Core
)
