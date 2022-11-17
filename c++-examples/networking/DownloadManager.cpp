// Copyright (C) 2022 Fabrice Salvaire
// from https://code.qt.io/cgit/qt/qtbase.git/tree/examples/network/download?h=6.4
//   Copyright (C) 2017 The Qt Company Ltd.
//   SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

/**************************************************************************************************/

#include "DownloadManager.h"

/**************************************************************************************************/

DownloadManager::DownloadManager()
{
  connect(&m_manager,
          &QNetworkAccessManager::finished,
          this,
          &DownloadManager::get_finished);
}

void
DownloadManager::get(const QUrl &url)
{
  QNetworkRequest request(url);
  request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
  QNetworkReply *reply = m_manager.get(request);

#if QT_CONFIG(ssl)
  connect(reply, &QNetworkReply::sslErrors, this, &DownloadManager::ssl_errors);
#endif

  m_current_downloads.append(reply);
}

bool
DownloadManager::is_http_redirect(QNetworkReply *reply)
{
  int status_code = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
  return
    status_code == 301 || status_code == 302 || status_code == 303 ||
    status_code == 305 || status_code == 307 || status_code == 308;
}

void
DownloadManager::ssl_errors(const QList<QSslError> &sslErrors)
{
#if QT_CONFIG(ssl)
  for (const QSslError &error : sslErrors)
    qWarning() << "SSL error:" << error.errorString();
#else
  Q_UNUSED(sslErrors);
#endif
}

void
DownloadManager::get_finished(QNetworkReply *reply)
{
  QUrl url = reply->url();
  if (reply->error())
    qWarning() << "Request failed" << url << reply->errorString();
  else {
    if (is_http_redirect(reply))
      qInfo() << "Request was redirected" << url;
    else
      qInfo() << "Request succeeded" << url << reply->readAll().size() << "bytes";
  }

  m_current_downloads.removeAll(reply);
  reply->deleteLater();

  // Exit application if all downloads finished
  if (m_current_downloads.isEmpty())
    QCoreApplication::instance()->quit();
}
