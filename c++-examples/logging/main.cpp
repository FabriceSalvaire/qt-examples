// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: GPL-3.0-only

/**************************************************************************************************/

#include <QtDebug>
#include <QLoggingCategory>
#include <QMessageLogContext>

/**************************************************************************************************/

Q_DECLARE_LOGGING_CATEGORY(my_category)
Q_LOGGING_CATEGORY(my_category, "my-category")

int main(int argc, char *argv[])
{
  // g++ -DQT_CORE_LIB -DQT_NO_DEBUG -I.../logging-build -I.../logging -isystem /opt/Qt/6.3.0/gcc_64/include/QtCore -isystem /opt/Qt/6.3.0/gcc_64/include -isystem /opt/Qt/6.3.0/gcc_64/mkspecs/linux-g++ -O2 -march=nocona -fPIC -pthread -MD -MT CMakeFiles/app.dir/main.cpp.o -MF CMakeFiles/app.dir/main.cpp.o.d -E -o out .../logging/main.cpp

  // QT_LOGGING_RULES="*.debug=false;*.info=true" ./app
  qInfo() << "Message ...";
  qCInfo(my_category) << "Message ...";

  for (QLoggingCategoryMacroHolder<QtInfoMsg> qt_category(my_category); // instanciate macro holder class
       qt_category; // bool test
       qt_category.control = false // to break for loop
       )
    QMessageLogger(nullptr, 0, nullptr, qt_category).info() << "Message ...";

  // versus

  QLoggingCategoryMacroHolder<QtInfoMsg> qt_category(my_category);
  if (qt_category)
    QMessageLogger(nullptr, 0, nullptr, qt_category).info() << "Message ...";
}
