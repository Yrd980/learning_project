#ifndef __GRID_H__
#define __GRID_H__

#include "config.hpp"
#include "pos.hpp"
#include <bitset>
#include <deque>

struct Navigator {
  std::bitset<BitsetSize> visited;
  std::bitset<BitsetSize * 2> dirNext;
  Navigator() {
    visited.reset();
    dirNext.reset();
  }

  int getVisitedIndex(int x, int y) { return x * MAX_Col_Length + y; }
  int getDirIndex(int x, int y) { return x * MAX_Col_Length * 2 + y * 2; }
  void setVisited(int x, int y) { visited[getVisitedIndex(x, y)] = 1; }
  bool isVisited(int x, int y) { return visited[getVisitedIndex(x, y)]; }
  void setDir(int x, int y, int d) {
    int index = getDirIndex(x, y);
    if (d & 1)
      dirNext[index] = 1;
    if (d & 2)
      dirNext[index + 1] = 1;
  }
  int getDir(int x, int y) {
    int ans = 0;
    int index = getDirIndex(x, y);
    if (dirNext[index] == 1)
      ans += 1;
    if (dirNext[index + 1] == 1)
      ans += 2;
    return ans;
  }
};

struct Navigator_ship {
  std::bitset<BitsetSize * 4> visited;

  Navigator_ship() { visited.reset(); }

  int getVisitedIndex(int x, int y, int d) {
    return x * MAX_Col_Length * 4 + y * 4 + d;
  }

  int setVisited(int x, int y, int d) { visited[getVisitedIndex(x, y, d)]; }

  bool isVisited(int x, int y, int d) {
    return visited[getVisitedIndex(x, y, d)];
  }
};

#define BLANK 0b0000000000000001
#define SEA 0b0000000000000010
#define OBSTACLE 0b0000000000000100
#define BERTH 0b0000000000001000 // ROBOT_NOCOL // SJHIP_NOCOL

#define ROUTE 0b0000000000010000       // ROBOT_NOCOL
#define SEA_ROUTE 0b0000000000100000   // SHIP_NOCOL
#define ROBOT_BUYER 0b0000000001000000 // ROBOT_NOCOL
#define SHIP_BUYER 0b0000000010000000  // SHIP_NOCOL

#define BERTH_CENTER 0b0000000100000000 // SHIP_NOCOL
#define CROSS 0b0000001000000000
#define CROSS_ROUTE 0b0000100000000000 // ROBOT_NOCOL // SHIP_NOCOL
#define DELIVERY 0b0001000000000000    // SHIP_NOCOL

#define SHIP_NOCOL 0b0001100110101000
#define ROBOT_NOCOL 0b0000100001011000

#define ROBOT_ABLE 0b0000101001011001
#define SHIP_ABLE 0b0001101110101010

#define NOT_VALID_GRID(x, y)                                                   \
  (x < 0 or x >= MAX_Line_Length or y < 0 or y >= MAX_Col_Length)
#define IS_SHIP_NOCOL(x) (x & SHIP_NOCOL)
#define IS_ROBOT_NOCOL(x) (x & ROBOT_NOCOL)
#define IS_ROBOT_ABLE(x) (x & ROBOT_ABLE)
#define IS_SHIP_ABLE(x) (x & SHIP_ABLE)

struct Grid {
  Pos pos;
  int type;
  bool robotOnIt;
  Navigator *gridDir;
  int berthId;
  int bit_type;
  int shipAble[4];

  int belongToBerth;

  Grid() {
    this->pos = Pos(-1, -1);
    this->type = -1;
    this->gridDir = nullptr;
    this->robotOnIt = false;
    this->berthId = -1;
    this->bit_type = 0;
    this->belongToBerth = -1;
  }
  Grid(int x, int y, int type) : type(type) {
    this->pos = Pos(x, y);
    this->gridDir = nullptr;
    this->robotOnIt = false;
    this->berthId = -1;
    this->bit_type = 1 << type;
    this->belongToBerth = -1;
  }
};

Grid *grids[MAX_Line_Length + 1][MAX_Col_Length + 1];

bool checkPos(Pos pos) {
  return pos.x >= 0 && pos.x < MAX_Line_Length && pos.y >= 0 &&
         pos.y < MAX_Col_Length;
}

bool checkRobotAble(Pos pos) {
  if (checkPos(pos) == false)
    return false;
  auto type = grids[pos.x][pos.y]->type;
  return (type == 0 || type == 3 || type == 4 || type == 6 || type == 9 ||
          type == 11);
}

bool checkShipAble(Pos pos) {
  if (checkPos(pos) == false)
    return false;
  auto type = grids[pos.x][pos.y]->type;
  return (type == 1 || type == 3 || type == 5 || type == 7 || type == 8 ||
          type == 9 || type == 11 || type == 12);
}
int SHIPSHIFT[4][6][2] = {
    {{0, 0}, {1, 0}, {2, 0}, {0, 1}, {1, 1}, {2, 1}},
    {{0, 0}, {-1, 0}, {-2, 0}, {0, -1}, {-1, -1}, {-2, -1}},
    {{0, 0}, {1, 0}, {0, -1}, {1, -1}, {0, -2}, {1, -2}},
    {{0, 0}, {-1, 0}, {0, 1}, {-1, 1}, {0, 2}, {-1, 2}}};

bool checkShipAble_with_dir_main(Pos pos, int dir) {
  for (int i = 0; i < 6; i++) {
    Pos next = pos + Pos(SHIPSHIFT[dir][i][1], SHIPSHIFT[dir][i][0]);
    auto type = grids[next.x][next.y]->type;
    if (checkShipAble(next) == false)
      return false;
  }
  return true;
}

bool checkRobotNoColl(Pos pos) {
  if (checkPos(pos) == false)
    return false;
  auto type = grids[pos.x][pos.y]->type;
  return (type == 3 || type == 4 || type == 6 || type == 11);
}

bool checkShipNoColl(Pos pos) {
  if (checkPos(pos) == false)
    return false;
  auto type = grids[pos.x][pos.y]->type;
  return (type == 3 || type == 5 || type == 7 || type == 8 || type == 11 ||
          type == 12);
}

ShipPos calShipRotPos(Pos pos, int dir, int rot) {
  if (rot == 0) {
    if (dir == 0) {
      return ShipPos(pos + Pos(0, 2), 3);
    } else if (dir == 1) {
      return ShipPos(pos + Pos(0, -2), 2);
    } else if (dir == 2) {
      return ShipPos(pos + Pos(-2, 0), 0);
    } else if (dir == 3) {
      return ShipPos(pos + Pos(2, 0), 1);
    }
  } else {
    if (dir == 0) {
      return ShipPos(pos + Pos(1, 1), 2);
    } else if (dir == 1) {
      return ShipPos(pos + Pos(-1, -1), 3);
    } else if (dir == 2) {
      return ShipPos(pos + Pos(-1, 1), 1);
    } else if (dir == 3) {
      return ShipPos(pos + Pos(1, -1), 0);
    }
  }
  return ShipPos(-1, -1, -1);
}

std::vector<Pos> getShipAllPos(Pos pos, int dir) {
  std::vector<Pos> ret;
  if (dir == 0) {
    ret.push_back(pos);
    ret.push_back(pos + Pos(0, 1));
    ret.push_back(pos + Pos(0, 2));
    ret.push_back(pos + Pos(1, 0));
    ret.push_back(pos + Pos(1, 1));
    ret.push_back(pos + Pos(1, 2));
  } else if (dir == 1) {
    ret.push_back(pos);
    ret.push_back(pos + Pos(0, -1));
    ret.push_back(pos + Pos(0, -2));
    ret.push_back(pos + Pos(-1, 0));
    ret.push_back(pos + Pos(-1, -1));
    ret.push_back(pos + Pos(-1, -2));
  } else if (dir == 2) {
    ret.push_back(pos);
    ret.push_back(pos + Pos(-1, 0));
    ret.push_back(pos + Pos(-2, 0));
    ret.push_back(pos + Pos(0, 1));
    ret.push_back(pos + Pos(-1, 1));
    ret.push_back(pos + Pos(-2, 1));
  } else if (dir == 3) {
    ret.push_back(pos);
    ret.push_back(pos + Pos(1, 0));
    ret.push_back(pos + Pos(2, 0));
    ret.push_back(pos + Pos(0, -1));
    ret.push_back(pos + Pos(1, -1));
    ret.push_back(pos + Pos(2, -1));
  }
  return ret;
}

int checkShipAllAble(Pos pos, int dir) {
  auto allPos = getShipAllPos(pos, dir);
  int ret = 1;
  for (auto &p : allPos) {
    if (checkShipAble(p) == false)
      return 0;
    if (checkShipNoColl(p))
      ret = 2;
  }
  return ret;
}
void PreproShipAllAble() {
  for (int x = 0; x < MAX_Line_Length; x++) {
    for (int y = 0; y < MAX_Col_Length; y++) {
      for (int i = 0; i < 4; i++) {
        grids[x][y]->shipAble[i] = checkShipAllAble(Pos(x, y), i);
      }
    }
  }
}

int _dis_s[MAX_Line_Length + 1][MAX_Col_Length + 1][4];
ShipPos _pre_s[MAX_Line_Length + 1][MAX_Col_Length + 1][4];
int _pre_dir_s[MAX_Line_Length + 1][MAX_Col_Length + 1][4];

ShipPos _queue_ship[120010];

std::deque<int> *sovleShip_ori(Pos origin, int direction, Pos target,
                               bool needPath = true) {
  allPathLogger.log(nowTime, "sovleShip origin{},{} direction{} target{},{}",
                    origin.x, origin.y, direction, target.x, target.y);
  for (int i = 0; i < MAX_Line_Length; i++) {
    for (int j = 0; j < MAX_Col_Length; j++) {
      for (int k = 0; k < 4; k++) {
        _dis_s[i][j][k] = INT_MAX;
        _pre_s[i][j][k] = ShipPos(-1, -1, -1);
        _pre_dir_s[i][j][k] = -1;
      }
    }
  }
  int start = 0;
  int end = 0;
  _queue_ship[end++] = ShipPos(origin, direction);
  _dis_s[origin.x][origin.y][direction] = 0;
  while (start != end) {
    ShipPos now = _queue_ship[start++];

    if (start == 120010) {
      start = 0;
    }

    ShipPos next = now + dir[now.direction];
    auto checkRes = grids[next.x][next.y]->shipAble[next.direction];
    if (checkRes && _dis_s[next.x][next.y][next.direction] >
                        _dis_s[now.x][now.y][now.direction] + checkRes) {
      _dis_s[next.x][next.y][next.direction] =
          _dis_s[now.x][now.y][now.direction] + checkRes;
      _pre_s[next.x][next.y][next.direction] = now;
      _pre_dir_s[next.x][next.y][next.direction] = 2;
      _queue_ship[end++] = next;
      if (end == 120010)
        end = 0;
    }

    next = calShipRotPos(now.toPos(), now.direction, 0);
    checkRes = grids[next.x][next.y]->shipAble[next.direction];
    if (checkRes && _dis_s[next.x][next.y][next.direction] >
                        _dis_s[now.x][now.y][now.direction] + checkRes) {
      _dis_s[next.x][next.y][next.direction] =
          _dis_s[now.x][now.y][now.direction] + checkRes;
      _pre_s[next.x][next.y][next.direction] = now;
      _pre_dir_s[next.x][next.y][next.direction] = 0;
      _queue_ship[end++] = next;
      if (end == 120010)
        end = 0;
    }

    next = calShipRotPos(now.toPos(), now.direction, 1);
    checkRes = grids[next.x][next.y]->shipAble[next.direction];
    if (checkRes && _dis_s[next.x][next.y][next.direction] >
                        _dis_s[now.x][now.y][now.direction] + checkRes) {
      _dis_s[next.x][next.y][next.direction] =
          _dis_s[now.x][now.y][now.direction] + checkRes;
      _pre_s[next.x][next.y][next.direction] = now;
      _pre_dir_s[next.x][next.y][next.direction] = 1;
      _queue_ship[end++] = next;
      if (end == 120010)
        end = 0;
    }
  }

  std::deque<int> *result = new std::deque<int>;

  ShipPos now = ShipPos(target, 0);

  for (int i = 1; i < 4; i++) {
    if (_dis_s[target.x][target.y][i] < _dis_s[now.x][now.y][now.direction]) {
      now.direction = i;
    }
  }

  while (true && needPath) {
    result->push_front(_pre_dir_s[now.x][now.y][now.direction]);
    now = _pre_s[now.x][now.y][now.direction];
    if (now.toPos() == origin && now.direction == direction) {
      break;
    }
  }
  return result;
}

Pos _arr[40010];

Navigator *solveGrid(Pos origin) {
  Navigator *result = new Navigator;
  result->setVisited(origin.x, origin.y);
  Pos _arr[40010];
  int start = 0, end = 0;
  _arr[end++] = origin;
  while (start < end) {
    Pos &now = _arr[start++];
    for (int i = 0; i < 4; i++) {
      Pos next = now + dir[i];
      if (checkRobotAble(next) == false) {
        continue;
      }
      if (result->isVisited(next.x, next.y)) {
        continue;
      }
      result->setVisited(next.x, next.y);
      result->setDir(next.x, next.y, ((i == 0 || i == 2) ? i + 1 : i - 1));
      _arr[end++] = next;
    }
  }
  return result;
}

int _ship_map_front[120010];
int _ship_map_front_pos[120010];
std::deque<int> *return_path(int now);
std::deque<int> *sovleShip(Pos origin, int direction, Pos target,
                           bool needPath = true) {
  Navigator_ship *map = new Navigator_ship;
  Navigator_ship *map_main_channel = new Navigator_ship;
  int start = 0, end = 0;
  _queue_ship[end++] = ShipPos(origin, direction);
  while (start < end) {
    ShipPos now = _queue_ship[start++];
    if (grids[now.x][now.y]->shipAble[now.direction] == 2) {
      if (map_main_channel->isVisited(now.x, now.y, now.direction) == 0) {
        map_main_channel->setVisited(now.x, now.y, now.direction);
        _ship_map_front[end] = start - 1;
        _ship_map_front_pos[end] = 4;
        _queue_ship[end++] = now;
      }
    }
    ShipPos next[3] = {calShipRotPos(now.toPos(), now.direction, 0),
                       calShipRotPos(now.toPos(), now.direction, 1),
                       now + dir[now.direction]};
    for (int i = 0; i < 3; i++) {
      if (map->isVisited(next[i].x, next[i].y, next[i].direction))
        continue;
      if (grids[next[i].x][next[i].y]->shipAble[next[i].direction] == 0)
        continue;
      map->setVisited(next[i].x, next[i].y, next[i].direction);
      _ship_map_front[end] = start - 1; 
      _ship_map_front_pos[end] = i;     
      if (next[i].toPos() == target) {
        if (needPath) {
          return return_path(end);
        }
        return new std::deque<int>;
      }
      _queue_ship[end++] = next[i];
    }
  }
  return new std::deque<int>;
}
#endif
