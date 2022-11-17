
* [Qt Concurrent](https://doc.qt.io/qt-6/qtconcurrent-index.html)
* [Concurrent Run](https://doc.qt.io/qt-6/qtconcurrentrun.html)
* [Concurrent Task](https://doc.qt.io/qt-6/qtconcurrenttask.html)
* [QFuture](https://doc.qt.io/qt-6/qfuture.html)
* [QPromise](https://doc.qt.io/qt-6/qpromise.html)
  QPromise provides a simple way to communicate progress and results of the user-defined computation to QFuture in an asynchronous fashion. 


* [Image Scaling Example](https://doc.qt.io/qt-6/qtconcurrent-imagescaling-example.html)

```
using NetworkReply = std::variant<QByteArray, QNetworkReply::NetworkError>;

enum class IOError { FailedToRead, FailedToWrite };
using IOResult = std::variant<QString, IOError>;

QFuture<IOResult> future = QtConcurrent::run([url] {
        ...
        return NetworkReply(QNetworkReply::TimeoutError);
}).then([](NetworkReply reply) {
    if (auto error = std::get_if<QNetworkReply::NetworkError>(&reply))
        return IOResult(IOError::FailedToRead);

    auto data = std::get_if<QByteArray>(&reply);
    // try to write *data and return IOError::FailedToWrite on failure
    ...
});

auto result = future.result();
if (auto filePath = std::get_if<QString>(&result)) {
    // do something with *filePath
else
    // process the error
```


```
QFuture<int> testFuture = ...;
auto resultFuture = testFuture.then([](int res) {
    // Block 1
}).onCanceled([] {
    // Block 2
}).onFailed([] {
    // Block 3
}).then([] {
    // Block 4
}).onFailed([] {
    // Block 5
}).onCanceled([] {
    // Block 6
});
```


The simplest case of promise and future collaboration would be a single result communication:
```
QPromise<int> promise;
QFuture<int> future = promise.future();

QScopedPointer<QThread> thread(
    QThread::create(
        [] (QPromise<int> promise) {
            promise.start();   // notifies QFuture that the computation is started
            promise.addResult(42);
            promise.finish();  // notifies QFuture that the computation is finished
        },
        std::move(promise)
    )
);
thread->start();

future.waitForFinished();  // blocks until QPromise::finish is called
future.result();  // returns 42
```

Here is an example of how a promise can be used in multiple threads:
```
QSharedPointer<QPromise<int>> sharedPromise(new QPromise<int>());
QFuture<int> future = sharedPromise->future();

// ...

// here, QPromise is shared between threads via a smart pointer
QScopedPointer<QThread> threads[] = {
    QScopedPointer<QThread>(
        QThread::create(
            [] (auto sharedPromise) {
                sharedPromise->addResult(0, 0);  // adds value 0 by index 0
            },
            sharedPromise
        )
    ),
    QScopedPointer<QThread>(
        QThread::create(
            [] (auto sharedPromise) {
                sharedPromise->addResult(-1, 1);  // adds value -1 by index 1
            },
            sharedPromise
        )
    ),
    QScopedPointer<QThread>(
        QThread::create(
            [] (auto sharedPromise) {
                sharedPromise->addResult(-2, 2);  // adds value -2 by index 2
            },
            sharedPromise
        )
    ),
    // ...
};
// start all threads
for (auto& t : threads)
    t->start();

// ...

future.resultAt(0);  // waits until result at index 0 becomes available. returns value  0
future.resultAt(1);  // waits until result at index 1 becomes available. returns value -1
future.resultAt(2);  // waits until result at index 2 becomes available. returns value -2
```
