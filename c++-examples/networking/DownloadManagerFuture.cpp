// Copyright (C) 2022 Fabrice Salvaire
// from https://code.qt.io/cgit/qt/qtbase.git/tree/examples/network/download?h=6.4
//   Copyright (C) 2017 The Qt Company Ltd.
//   SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

/**************************************************************************************************/

#include <QFuture>

#include "DownloadManagerFuture.h"

/**************************************************************************************************/

DownloadManagerFuture::DownloadManagerFuture()
{}

void
process(QByteArray data) {
  qInfo() << "Process" << data.size();
}

void
DownloadManagerFuture::get(const QUrl &url)
{
  QNetworkRequest request(url);
  request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
  QNetworkReply *reply = m_manager.get(request);
  // QFuture<T>
  auto future = QtFuture::connect(reply, &QNetworkReply::finished)
    .then([reply] {
      // if (reply->error() == QNetworkReply::NoError)
      return reply->readAll();
      // else
    })
    .then(QtFuture::Launch::Async, process)
    .onFailed([](QNetworkReply::NetworkError) {
      // handle network errors
    });
}

QFuture<QByteArray>
DownloadManagerFuture::download(const QList<QUrl> &urls)
{
  // The download() method takes a list of URLs and returns a QFuture.
  // The QFuture stores the byte array data received for each download.
  // To store the data inside the QFuture, we create a QPromise object
  //   and report that it has started to indicate the start of the download.

  // Since the promise object is shared between handlers connected to each network reply,
  // we need to copy and use the promise object in multiple places simultaneously.

  // The QSharedPointer class holds a strong reference to a shared pointer.
  // The QSharedPointer is an automatic, shared pointer in C++.
  // It behaves exactly like a normal pointer for normal purposes, including respect for constness.
  // QSharedPointer will delete the pointer it is holding when it goes out of scope, provided no other QSharedPointer objects are referencing it.
  QSharedPointer<QPromise<QByteArray>> promise(new QPromise<QByteArray>());
  auto future = promise->future();
  // notifies QFuture that the computation is started
  promise->start();

  for (auto url : urls) {
    qInfo() << "Get..." << url;
    QNetworkRequest request(url);
    request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
    QSharedPointer<QNetworkReply> reply(m_manager.get(request));
    m_replies.push_back(reply);

    // Instead of connecting to QNetworkReply's signals using the QObject::connect() method, we use QtFuture::connect().
    // It works similar to QObject::connect(), but returns a QFuture object, that becomes available as soon as the
    //   QNetworkReply::finished() signal is emitted.
    // This allows us to attach continuations and failure handlers.

    // In the continuation attached via .then(), we check if the user has requested to cancel the download.
    // If that's the case, we stop processing the request.
    // By calling the QPromise::finish() method, we notify the user that processing has been finished.
    // In case the network request has ended with an error, we throw an exception.
    // The exception will be handled in the failure handler attached using the .onFailed() method.
    // Note that we have two failure handlers:
    //   the first one captures the network errors,
    //   the second one all other exceptions thrown during the execution.
    // Both handlers save the exception inside the promise object (to be handled by the caller of the download() method)
    //   and report that the computation has finished.
    // Also note that, for simplicity, in case of an error we interrupt all pending downloads.

    QtFuture::connect(reply.get(), &QNetworkReply::finished)
        .then([=] {
          if (promise->isCanceled()) {
            qInfo() << "Get finished: but promise canceled";
            if (!future.isFinished())
              // notifies QFuture that the computation is finished
              // Reports that the computation is finished. Once finished, no new results will be added when calling addResult()
              promise->finish();
            return;
          }

          if (reply->error() != QNetworkReply::NoError) {
            qInfo() << "Get failed" << url;
            if (!future.isFinished())
              throw reply->error(); // of type: enum QNetworkReply::NetworkError
          }

          // If the request has not been canceled and no error occurred, we read the data from the network reply
          //  and add it to the list of results of the promise object.
          qInfo() << "Get succeeded" << url;
          promise->addResult(reply->readAll());

          // If the number of results stored inside the promise object is equal to the number of the urls to be downloaded,
          //   there are no more requests to process, so we also report  that the promise has finished.
          // Report finished on the last download
          if (future.resultCount() == urls.size()) {
            promise->finish();
          }
        })
        .onFailed([=](QNetworkReply::NetworkError error) {
          // Creates an std::exception_ptr that holds a reference to a copy of e
          // template< class E > std::exception_ptr make_exception_ptr( E e ) noexcept;
          promise->setException(std::make_exception_ptr(error));
          promise->finish();
        })
        .onFailed([=] {
          const auto ex = std::make_exception_ptr(std::runtime_error("Unknown error occurred while downloading."));
          promise->setException(ex);
          promise->finish();
        });
  }

  // The future associated with the promise is returned to the caller.
  return future;
}

void
DownloadManagerFuture::update_status(const QString &msg)
{
  qInfo() << msg;
}

void
DownloadManagerFuture::cancel()
{
  qInfo() << "Canceling...";
  m_download_future.cancel();
  abort_download();
}

void
DownloadManagerFuture::abort_download()
{
  qInfo() << "Abort all pending requests";
  for (auto reply : m_replies)
    reply->abort();
}

QList<qsizetype>
DownloadManagerFuture::get_size()
{
  QList<qsizetype> sizes;
  const auto results = m_download_future.results();
  for (auto data : results)
    data.push_back(data.size());
  return sizes;
}

void
DownloadManagerFuture::run_download(const QList<QUrl> &urls)
{
  m_download_future = download(urls);
  qInfo() << "Downloading...";

  m_download_future
    // first then must be [...](auto) to take the QByteArray result
    // Since it may be computationally heavy, and we don't want to block the main thread,
    //   we pass the QtFuture::Launch::Async option, to launch the scaling step in a new thread.
    // Note that updateStatus() is called through QMetaObject::invokeMethod(),
    //   because it updates the UI and needs to be invoked from the main thread.
    .then(QtFuture::Launch::Async,
          [this](auto) {
            QMetaObject::invokeMethod(this, [this] { update_status(tr("Processing...")); });
            return get_size();
          })
    // For the same reason, it also needs to be invoked from the main thread, so we pass this as a context to .then().
    //   By default, .then() is launched in the parent's thread, but if a context object is specified, it is launched in the context object's thread.
    .then(this, [this](const QList<qsizetype> &sizes) {
      update_status("Finished");
    })
    // Then we add cancellation and failure handlers.
    // We don't need to specify the context anymore, because .onCanceled() and the next handlers will be launched in their parent's context.
    .onCanceled([this] {
      update_status("Download has been canceled");
    })
    // template <typename Function, typename> QFuture<T> QFuture::onFailed(Function &&handler)
    .onFailed([this](QNetworkReply::NetworkError error) {
      update_status(QString("Download finished with error: %1").arg(error));
      // Abort all pending requests
      abort_download();
    })
    .onFailed([this](const std::exception& ex) {
      update_status(ex.what());
    });
}
