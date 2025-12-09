// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: GPL-3.0-only

/**************************************************************************************************/

#include <stdlib.h>

// #include <QByteArray>
// #include <QCoreApplication>
#include <QApplication>
#include <QDebug>
// #include <QFuture>
// #include <QNetworkAccessManager>
#include <QNetworkInformation>
// #include <QNetworkReply>
// #include <QPromise>
// #include <QThread>
#include <QThreadPool>
 #include <QUrl>
// #include <QtConcurrent>

/**************************************************************************************************/

#include "DownloadManager.h"
#include "DownloadManagerQueue.h"
#include "DownloadManagerFuture.h"

/**************************************************************************************************/


/**************************************************************************************************/

int
main(int argc, char *argv[])
{
  // QCoreApplication app(argc, argv);
  // if an event loop is required
  QApplication app(argc, argv);

  qInfo() << "Start...";

  // https://doc.qt.io/qt-6/qnetworkinformation.html
  if (QNetworkInformation::loadDefaultBackend()) {
    QNetworkInformation *network_information = QNetworkInformation::instance();
    qInfo() << "Network Backend: " << network_information->backendName();
    qInfo() << "  reachability: " << network_information->reachability();
    qInfo() << "  features: " << network_information->supportedFeatures();
  } else {
    qInfo() << "Failed to load network backend";
  }

  // https://doc.qt.io/qt-6/qthreadpool.html
  QThreadPool *global_thread_pool = QThreadPool::globalInstance();
  qInfo() << "Global Thread Pool:" << global_thread_pool->maxThreadCount();

  QUrl url1("http://qt-project.org");
  QUrl url2("https://tile.openstreetmap.org/14/8303/5660.png");
  QUrl bad_url("http://foo");
  QList<QUrl> urls = {url1, url2, bad_url};

  // DownloadManager manager;
  // DownloadManagerQueue manager_queue;
  // QTimer::singleShot(0, &app, [&] {
  //   for (auto url: urls)
  //     manager.get(url);
  //     manager_queue.append(url);
  // });
  // QObject::connect(&manager_queue, &DownloadManagerQueue::finished, &app, &QCoreApplication::quit);

  DownloadManagerFuture manager_future;
  // manager_future.download(urls);
  manager_future.run_download(urls);
  manager_future.cancel();
  // must be killed

  // QTimer::singleShot(0, &app, [&url, &app]{
  //   auto future = QtConcurrent::run(download2, url)
  //     .then(process_image)
  //     .onFailed([&url](QNetworkReply::NetworkError) {
  //       qWarning() << "Get failed " << url;
  //     })
  //     .then([&app]{
  //       app.exit(EXIT_SUCCESS);
  //     });
  // });

  // return EXIT_SUCCESS;
  return app.exec();
}
