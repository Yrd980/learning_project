#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class counter {
public:
  counter();
  counter(counter &&) = default;
  counter(const counter &) = default;
  counter &operator=(counter &&) = default;
  counter &operator=(const counter &) = default;
  ~counter();

  void registerVariable(const std::string &name, int initialValue = 0) {
    variables[name] = initialValue;
    locks[name] = false;
  }

  void registerVector(const std::string &name) {
    vectors[name] = std::vector<int>();
    locks[name] = false;
  }

  void registerVector2D(const std::string &name) {
    vectors2d[name] = std::vector<std::pair<int, int>>();
    locks[name] = false;
  }

  void push_back(const std::string &name, int value) {
    if (vectors.find(name) != vectors.end() && !locks[name]) {
      vectors[name].push_back(value);
    }
  }

private:
  std::unordered_map<std::string, int> variables;
  std::unordered_map<std::string, bool> locks;
  std::unordered_map<std::string, std::vector<int>> vectors;
  std::unordered_map<std::string, std::vector<std::pair<int, int>>> vectors2d;
};

counter::counter() {}

counter::~counter() {}
