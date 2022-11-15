/**************************************************************************************************/

#include <QGuiApplication>
#include <QQmlEngine>
#include <QQmlFileSelector>
#include <QQuickView>

/**************************************************************************************************/

int main(int argc, char * argv[])
{
    QCoreApplication::setOrganizationName("QtExamples");

    QGuiApplication app(argc, argv);
    qInfo() << "Start Application";

    QQuickView view;
    view.connect(view.engine(), &QQmlEngine::quit, &app, &QCoreApplication::quit);
    view.setSource(QUrl("qrc:touch/touch.qml"));
    if (view.status() == QQuickView::Error)
        return -1;
    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.show();
    return app.exec();
}
