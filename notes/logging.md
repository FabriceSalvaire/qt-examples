# Qt Logging

* https://doc.qt.io/qt-6/testing-and-debugging.html#debugging-techniques
* https://doc.qt.io/qt-6/qtglobal.html#qInstallMessageHandler

* https://doc.qt.io/qt-6/qloggingcategory.html
* https://doc.qt.io/qt-6/qmessagelogger.html

## Macros

* https://doc.qt.io/qt-6/qtglobal.html

cf `.../Qt/6.3.0/gcc_64/include/QtCore/qlogging.h`

```
qDebug(const char *message, ...) // QT_NO_DEBUG_OUTPUT
qInfo(const char *message, ...) // This function does nothing if QT_NO_INFO_OUTPUT was defined during compilation.
qWarning(const char *message, ...) // QT_NO_WARNING_OUTPUT

qCritical(const char *message, ...) // It exits if the environment variable QT_FATAL_CRITICALS is not empty.
qFatal(const char *message, ...) // on Windows send message to debugger
```

cf `.../Qt/6.3.0/gcc_64/include/QtCore/qloggingcategory.h`

```
Q_DECLARE_LOGGING_CATEGORY(name)
Q_LOGGING_CATEGORY(name, string, msgType)
Q_LOGGING_CATEGORY(name, string)

qCDebug(category, const char *message, ...)
qCDebug(category)
qCInfo(category, const char *message, ...)
qCInfo(category)
qCWarning(category, const char *message, ...)
qCWarning(category)
qCCritical(category, const char *message, ...)
qCCritical(category)
```

```
#define QT_MESSAGE_LOGGER_COMMON(category, level) \
    for (QLoggingCategoryMacroHolder<level> qt_category(category); qt_category; qt_category.control = false) \
        QMessageLogger(QT_MESSAGELOG_FILE, QT_MESSAGELOG_LINE, QT_MESSAGELOG_FUNC, qt_category)

    // does compiler suppress the for loop if qt_category is always false ???

    QLoggingCategoryMacroHolder<level> qt_category(category);
    while (qt_category) {
       // QMessageLogger(const char *file, int line, const char *function, const char *category)
       QMessageLogger(QT_MESSAGELOG_FILE, QT_MESSAGELOG_LINE, QT_MESSAGELOG_FUNC, qt_category);
       qt_category.control = false;
    }

#define qCDebug(category, ...) QT_MESSAGE_LOGGER_COMMON(category, QtDebugMsg).debug(__VA_ARGS__)
```

## Config

```
$HOME/.config/QtProject/qtlogging.ini

QT_LOGGING_RULES="*.debug=false;*.info=true;alpine-toolkit.qtcarto.debug=true" app
```
