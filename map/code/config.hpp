#ifndef __CONFIG_H__
#define __CONFIG_H__
#include "pos.hpp"
#include <chrono>
#include <functional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std::chrono;
#include "count.hpp"
#include "logger.hpp"

const int MAX_Line_Length = 200;
const int MAX_Col_Length = 200;
const int MAX_TIME = 5 * 60 * 50;
const int Item_Continue_Time = 1000;
#define BitsetSize 40000

int MAX_Robot_Num = 0;
int MAX_Ship_Num = 0;
int MAX_Berth_Num = 0;
int MAX_Capacity;
int money = 25000;
int nowTime = 0;
bool inputFlag = true;
std::vector<int> robotPriority;
int priorityTimeControl = -1;

auto programStart = high_resolution_clock::now();

int MAX_Berth_Control_Length = 160;
int MAX_Berth_Merge_Length = 80;
int Worst_Rate = 3;
double Sell_Rate = 0.7;
int Min_Next_Berth_Value = 1700;
int Only_Run_On_Berth_with_Ship = 350;
int lastRoundRuningTime = 600;

int Min_Next_Berth_Goods = 10;
int Last_Round_delay_time = 4500;

const int _maxRobotCnt = 17;
const int _maxShipCnt = 2;

const double _itemAtEnd = 4800;
const double _pulledItemAtEnd = 1900;

int exptRobotCnt = 0;

Pos dir[4] = {Pos(0, 1), Pos(0, -1), Pos(-1, 0), Pos(1, 0)};
std::unordered_map<Pos, int> Pos2move = {
    {Pos(0, 1), 0}, {Pos(0, -1), 1}, {Pos(-1, 0), 2}, {Pos(1, 0), 3}};

FileLogger shipLogger("../log/ship_log.txt");
FileLogger robotLogger("../log/robot_log.txt");
FileLogger berthLogger("../log/berth_log.txt");
FileLogger itemLogger("../log/item_log.txt");
FileLogger centerLogger("../log/center_log.txt");

FileLogger flowLogger("../log/flow_log.txt");
FileLogger bcenterlogger("../log/bcenter_log.txt");
FileLogger pathLogger("../log/path_log.txt");
FileLogger allPathLogger("../log/allPath_log.txt");
FileLogger estimatorLogger("../log/estimator_log.txt");

#ifdef DEBUG
#define TEST(x) x
std::ofstream fout("output.txt");
std::ofstream tout("time.txt");
#else
#define TEST(x)
#endif

#ifdef DEBUG
Counter counter;
#else
Void_Counter counter;
#endif

#ifdef CREATE
#define CREATEMAP(x) x
std::ofstream mapOut("../genMap/path.txt");
#else
#define CREATEMAP(x)
#endif

template <typename T> void bugs_output(T x) {
#ifdef DEBUG
  fout << x << " ";
#endif
}

template <typename... Args> void bugs(Args... args) {
#ifdef DEBUG
  (..., bugs_output(args));
  fout << std::endl;
#endif
}

class Timer {
public:
#ifdef DEBUG
  template <typename Func, typename... Args>
  static auto measure(const std::string &description, Func func,
                      Args &&...args) {
    auto start = std::chrono::high_rehigh_resolution_clock::now();
    if constexpr (std::is_same_v < std::invoke_result_t<Func, Args...>, void) {
      func(std::forward<Args>(args)...);
      auto end = std::chrono::highhigh_resolution_clock::now();
      std::chrono::duduration<double> elapsed = end - start;
      tout << nowTime << " " << description << "\t - Elapsed time: \t"
           << elapsed.count() * 1000 << "\tmirco seconds.\n";
    } else {
      auto result = func(std::forward<Args>(args)...);
      auto end = std::chrono::high_resolution_clock::now();
      std::chrono::duration<double> elapsed = end - start;
      tout << nowTime << " " << description << "\t - Elapsed time: \t"
           << elapsed.count() * 1000 << "\tmicro seconds.\n";
      return result;
    }
  }
#else
  template <typename Func, typename... Args>
  static auto measure(const std::string &description, Func func, Args &&...args)
      -> decltype(func(std::forward<Args>(args)...)) {
    return func(std::forward<Args>(args)...);
  }
#endif
};

#ifdef DEBUG
void measureAndExecute(const std::string &description,
                       const std::function<void()> &action) {
  auto start = std::chrono::high_resolution_clock::now();
  action();
  auto end = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> elapsed = end - start;
  tout << description << " - Elapsed time: " << elapsed.count() << " ms\n";
}
#else
void measureAndExecute(const std::string &description,
                       const std::function<void()> &action) {
  action();
}
#endif

#endif
