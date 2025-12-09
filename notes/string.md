# Qt String Support

```
u"String" // C++11 Unicode literal UTF-16
```

In Qt5, the default decoding for the char* strings is UTF-8.

* [QByteArray](https://doc.qt.io/qt-6/qbytearray.html)
* [QChar](https://doc.qt.io/qt-6/qchar.html) provides a 16-bit Unicode character
* [QString](https://doc.qt.io/qt-6/qstring.html) stores a string of 16-bit `QChar`
* [QStringList](https://doc.qt.io/qt-6/qstringlist.html)
* [QLatin1StringView](https://doc.qt.io/qt-6/qlatin1stringview.html) provides a thin wrapper around an US-ASCII/Latin-1 encoded string literal
* [QLatin1String](https://doc.qt.io/qt-6/qlatin1string.html) is the same as `QLatin1StringView`

* [QStringLiteral explained](https://woboq.com/blog/qstringliteral.html)

## String at compile time

* [QStringLiteral(str)](https://doc.qt.io/qt-6/qstring.html#QStringLiteral)

The `QStringLiteral` macro generates the data for a QString at compile time.  Creating a QString
from it is free in this case, and the generated string data is stored in the read-only segment of
the compiled object file. It avoids to create a temporary `QString`.

A slightly less efficient way is to use `QLatin1StringView`. This class wraps a C string literal,
precalculates it length at compile time and can then be used for faster comparison with QStrings and
conversion to QStrings than a regular C string literal.

`QLatin1StringView` can still be more efficient than `QStringLiteral` when the string is passed to a
function that has an overload taking `QLatin1StringView` and this overload avoids conversion to
`QString`. For instance, `QString::operator==()` can compare to a `QLatin1StringView` directly.

For `QByteArray` use `QByteArrayLiteral`.

```
QStringLiteral(u"...") // encoded in UTF-16
const QString COLUMN = QStringLiteral("...");
static const QString COLUMN = QStringLiteral("...");

QByteArray a_byte_array = QByteArrayLiteral("...");

if (a_qstring) == "..."_L1) // QLatin1StringView
```
