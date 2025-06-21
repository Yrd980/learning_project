#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class counter {
public:
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

  void push_back(const std::string &name, int value1, int value2) {
    if (vectors.find(name) != vectors.end() && !locks[name]) {
      vectors2d[name].push_back(std::make_pair(value1, value2));
    }
  }

  void add(const std::string &name, int value) {
    if (variables.find(name) != variables.end() && !locks[name]) {
      variables[name] += value;
    }
  }

  void subtract(const std::string &name, int value) {
    if (variables.find(name) != variables.end() && !locks[name]) {
      variables[name] -= value;
    }
  }

  void lock(const std::string &name) {
    if (variables.find(name) != variables.end()) {
      locks[name] = true;
    }
  }

  void max_put(const std::string &name, int value) {
    if (variables.find(name) != variables.end() && !locks[name]) {
      variables[name] = std::max(variables[name], value);
    }
  }

  void min_put(const std::string &name, int value) {
    if (variables.find(name) != variables.end() && !locks[name]) {
      variables[name] = std::min(variables[name], value);
    }
  }

  void unlock(const std::string &name) {
    if (variables.find(name) != variables.end()) {
      locks[name] = false;
    }
  }

  int getValue(const std::string &name) {
    if (variables.find(name) != variables.end()) {
      return variables[name];
    }
    return 0;
  }

  void writeToFile(const std::string &filename) {
    std::ofstream outFile(filename, std::ios::app);
    outFile << "============================================" << "\n";
    for (const auto &var : variables) {
      outFile << "Variable: " << var.first << ",\t Value: " << var.second
              << ",\t Locked: " << (locks[var.first] ? "Yes" : "No") << "\n";
    }
    outFile << "=====================" << "\n";
    outFile << "avg_robot_move_length: "
            << (getValue("robot_move_length") / getValue("robot_get_nums"))
            << "\n";
    outFile << "max_robot_move_length: " << getValue("robot_move_length_max")
            << "\n";
    outFile << "min_robot_move_length: " << getValue("robot_move_length_min")
            << "\n";
    outFile << "============================================" << "\n";
    outFile.close();
    for (const auto &vec : vectors) {
      std::ofstream outFile(filename + "_" + vec.first + ".txt");
      for (int i = 0; i < vec.second.size(); i++) {
        outFile << vec.second[i] << "\n";
      }
      outFile.close();
    }
    for (const auto &vec : vectors2d) {
      std::ofstream outFile(filename + "_" + vec.first + ".txt");
      for (int i = 0; i < vec.second.size(); i++) {
        outFile << vec.second[i].first << " " << vec.second[i].second << "\n";
      }
      outFile.close();
    }
  }

private:
  std::unordered_map<std::string, int> variables;
  std::unordered_map<std::string, bool> locks;
  std::unordered_map<std::string, std::vector<int>> vectors;
  std::unordered_map<std::string, std::vector<std::pair<int, int>>> vectors2d;
};

class Void_Counter {
public:
  void registerVariable(const std::string &name, int initialValue = 0) {
    return;
  }
  void registerVector(const std::string &name) { return; }
  void registerVector2D(const std::string &name) { return; }
  void push_back(const std::string &name, int value1, int value2) { return; }
  void push_back(const std::string &name, int value) { return; }
  void add(const std::string &name, int value) { return; }
  void max_put(const std::string &name, int value) { return; }
  void min_put(const std::string &name, int value) { return; }
  void subtract(const std::string &name, int value) { return; }
  void lock(const std::string &name) { return; }
  void unlock(const std::string &name) { return; }
  int getValue(const std::string &name) { return 0; }
  void writeToFile(const std::string &filename) { return; }
};
