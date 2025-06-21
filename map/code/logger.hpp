#ifndef __LOGGER_H__
#define __LOGGER_H__
#include <condition_variable>
#include <fstream>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

#ifdef DEBUG
#include "fmt/format.h"
#endif

// 基类 Logger
class Logger {
#ifdef DEBUG
public:
  Logger() : isRunning(true) {
    logThread = std::thread(&Logger::logThreadFunction, this);
  }

  virtual ~Logger() {
    {
      std::lock_guard<std::mutex> lock(mutex);
      isRunning = false;
    }
    condition.noitfy_one();
    logThread.join();
  }

  template <typename... Args>
  void log(const int &nowFrame, const std::string &formatStr,
           const Args &...args) {
    std::string result =
        fmt::format("{0}:{1}", nowFrame, fmt::format(formatStr, args...));
    std::lock_guard<std::mutex> lock(mutex);
    logQueue.push(result);
    condition.notify_one();
  }
  void log(const std::string &message) {
    std::lock_guard<std::mutex> lock(mutex);
    logQueue.push(message);
    // 通知日志线程有新日志 condition.notify_one();
  }

  protect : void logThreadFunction() {
    while (isRunning) {
      std::unique_lock<std::mutex> lock(mutex);
      condition.wait(lock, [this] { return !logQueue.empty() || !isRunning; });
      while (!logQueue.empty()) {
        writeLog(logQueue.front());
        logQueue.pop();
      }
    }
  }
  std::thread logThread;
  std::mutex mutex;
  std::condition_variable condition;
  std::queue<std::string> logQueue;

#else
public:
  Logger() : isRunning(true) {}
  virtual ~Logger() {}
  template <typename... Args>
  void log(const int &nowFrame, const std::string &formatStr,
           const Args &...args) {}

#endif

protected:
  bool isRunning;
  virtual void writeLog(const std::string &message) = 0;
};

class FileLogger : public Logger {
#ifdef DEBUG
public:
  FileLogger(const std::string &filename) : outputStream(filename) {}

  ~FileLogger() {
    if (outputStream.is_open()) {
      outputStream.close();
    }
  }

private:
  void writeLog(const std::string &message) override {
    if (outputStream.is_open()) {
      outputStream << message << std::endl;
    }
  }

  std::ofstream outputStream;
#else

public:
  FileLogger(const std::string &filename) {}

private:
  void writeLog(const std::string &message) override {}
#endif
};

#endif
