#ifndef VECTOR_HPP
#define VECTOR_HPP

#include <cmath>
#include <cstddef>
#include <string>

struct Pos {
  int x, y;
  Pos(int x = -1, int y = -1) : x(x), y(y) {}
  Pos operator+(const Pos v) const { return Pos(x + v.x, y + v.y); }
  Pos operator-(const Pos v) const { return Pos(x - v.x, y - v.y); }
  bool operator==(const Pos v) const { return x == v.x && y == v.y; }
  bool operator!=(const Pos v) const { return x != v.x || y != v.y; }
  int length(const Pos v) const { return abs(x - v.x) + abs(y - v.y); }
};

namespace std {
template <> struct hash<Pos> {
  std::size_t operator()(const Pos &obj) const {
    std::string temp = std::to_string(obj.x) + std::to_string(obj.y);
    return std::hash<std::string>{}(temp);
  }
};
} // namespace std

struct ShipPos {
  int x, y, direction;

  ShipPos(int x = -1, int y = -1, int direction = -1)
      : x(x), y(y), direction(direction) {}
  ShipPos(Pos pos, int direction) : x(pos.x), y(pos.y), direction(direction) {}
  ShipPos operator+(const Pos v) const {
    return ShipPos(x + v.x, y + v.y, direction);
  }
  bool operator==(const ShipPos v) const {
    return x == v.x && y == v.y && direction == v.direction;
  }
  bool operator!=(const ShipPos v) const {
    return x != v.x || y != v.y || direction != v.direction;
  }
  Pos toPos() { return Pos(x, y); }
};

namespace std {
template <> struct hash<ShipPos> {
  std::size_t operator()(const ShipPos &obj) const {
    std::string temp = std::to_string(obj.x) + "_" + std::to_string(obj.y) +
                       "_" + std::to_string(obj.direction);
    return std::hash<std::string>{}(temp);
  }
};
} // namespace std

#endif
