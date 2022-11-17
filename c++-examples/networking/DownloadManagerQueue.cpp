// Copyright (C) 2022 Fabrice Salvaire
// from https://code.qt.io/cgit/qt/qtbase.git/tree/examples/network/download?h=6.4
//   Copyright (C) 2017 The Qt Company Ltd.
//   SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

/**************************************************************************************************/

#include "DownloadManagerQueue.h"

// #include <QTextStream>

// #include <cstdio>

// using namespace std;

/**************************************************************************************************/

DownloadManagerQueue::DownloadManagerQueue(QObject *parent)
  : QObject(parent)
{}

void
DownloadManagerQueue::append(const QUrl &url) {
  if (m_download_queue.isEmpty())
    QTimer::singleShot(0, this, &DownloadManagerQueue::start_next_download);

  m_download_queue.enqueue(url);
  ++m_total_count;
}

void DownloadManagerQueue::start_next_download() {
  if (m_download_queue.isEmpty()) {
    qInfo() << m_downloaded_count << "/" << m_total_count << "files downloaded successfully";
    emit finished();
    return;
  }

  QUrl url = m_download_queue.dequeue();
  QNetworkRequest request(url);
  request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
  m_current_download = m_manager.get(request);
  connect(m_current_download, &QNetworkReply::downloadProgress, this, &DownloadManagerQueue::download_progress);
  connect(m_current_download, &QNetworkReply::finished, this, &DownloadManagerQueue::download_finished);
  connect(m_current_download, &QNetworkReply::readyRead, this, &DownloadManagerQueue::download_ready_read);

  // prepare the output
  qInfo() << "Downloading" << url.toEncoded().constData();
  m_download_timer.start();
}

void
DownloadManagerQueue::download_progress(qint64 bytes_received, qint64 bytes_total)
{
  // calculate the download speed
  double speed = bytes_received * 1000.0 / m_download_timer.elapsed();
  QString unit;
  if (speed < 1024) {
    unit = "bytes/sec";
  } else if (speed < 1024 * 1024) {
    speed /= 1024;
    unit = "kB/s";
  } else {
    speed /= 1024 * 1024;
    unit = "MB/s";
  }

  qInfo() << "progress" << speed << unit;
}

void
DownloadManagerQueue::download_finished()
{
  QUrl url = m_current_download->request().url();
  if (m_current_download->error()) {
    // download failed
    qWarning() << "Request failed" << url << m_current_download->errorString();
  } else {
    // let's check if it was actually a redirect
    if (is_http_redirect()) {
      report_redirect();
    } else {
      qInfo() << "Request succeeded" << url;
      ++m_downloaded_count;
    }
  }

  m_current_download->deleteLater();
  start_next_download();
}

void
DownloadManagerQueue::download_ready_read() {
  m_current_download->readAll();
}

bool
DownloadManagerQueue::is_http_redirect() const
{
  int statusCode = m_current_download->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
  return
    statusCode == 301 || statusCode == 302 || statusCode == 303 ||
    statusCode == 305 || statusCode == 307 || statusCode == 308;
}

void
DownloadManagerQueue::report_redirect()
{
  int status_code = m_current_download->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
  QUrl request_url = m_current_download->request().url();
  qWarning() << "Request:" << request_url.toDisplayString()
             << "was redirected with code:" << status_code;

  QVariant target = m_current_download->attribute(QNetworkRequest::RedirectionTargetAttribute);
  if (!target.isValid())
    return;
  QUrl redirect_url = target.toUrl();
  if (redirect_url.isRelative())
    redirect_url = request_url.resolved(redirect_url);
  qWarning() << "Redirected to:" << redirect_url.toDisplayString();
}
