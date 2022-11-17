// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: GPL-3.0-only

/**************************************************************************************************/

#include <cstdlib>
#include <stdlib.h>

#include <QByteArray>
#include <QCoreApplication>
#include <QApplication>
#include <QDebug>
#include <QFuture>
#include <QNetworkAccessManager>
#include <QNetworkInformation>
#include <QNetworkReply>
#include <QPromise>
#include <QThread>
#include <QThreadPool>
#include <QUrl>
#include <QtConcurrent>

/**************************************************************************************************/

#include "DownloadManager.h"
#include "DownloadManagerQueue.h"

/**************************************************************************************************/

void
process_image(QByteArray data) {
  qInfo() << "Received " << data.size();
}

QByteArray
download2(const QUrl &url) {
  QNetworkAccessManager manager;
  QNetworkRequest request;
  request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
  request.setUrl(url);
  QNetworkReply *reply = manager.get(request);
  reply->waitForReadyRead(-1); // no timeout ms
  uint count = 0;
  while (reply->isRunning() and count < 10) {
    qInfo() << "Network reply...";
    QThread::usleep(10000);
    count++;
  }
  qInfo() << "Network reply" << reply->isRunning() << reply->isFinished() << reply->error();
  reply->deleteLater();
  return reply->readAll();
}

void
download1(const QUrl &url) {
  QNetworkAccessManager manager;
  QNetworkReply *reply = manager.get(QNetworkRequest(url));
  auto future = QtFuture::connect(reply, &QNetworkReply::finished)
    .then([reply] {
      return reply->readAll();
    })
    .then(QtFuture::Launch::Async, process_image);
}

/*
QFuture<QByteArray>
download(const QUrl &url) {
  // The QPromise class provides a way to store computation results to be
accessed by QFuture
  // https://doc.qt.io/qt-6/qpromise.html
  QPromise<QByteArray> promise;
  QFuture<QByteArray> future = promise.future();

  promise.start(); // notify that download is started

  // https://doc.qt.io/qt-6/qnetworkaccessmanager.html
  QNetworkAccessManager manager;
  // https://doc.qt.io/qt-6/qnetworkreply.html
  QNetworkReply *reply = manager.get(QNetworkRequest(url));
  QObject::connect(reply,
                   &QNetworkReply::finished,
                   [reply, p = std::move(promise)] {
                     p.addResult(reply->readAll());
                     p.finish(); // notify that download is finished
                     reply->deleteLater();
                   });

  return future;
}
*/

/**************************************************************************************************/

int
main(int argc, char *argv[])
{
  // QCoreApplication app(argc, argv);
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

  DownloadManager manager;
  DownloadManagerQueue manager_queue;
  QTimer::singleShot(0, &app, [&] {
    for (auto url: urls)
      // manager.get(url);
      manager_queue.append(url);
  });
  QObject::connect(&manager_queue, &DownloadManagerQueue::finished, &app, &QCoreApplication::quit);

  // download1(url);

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
