#ifndef __GRID_H__
#define __GRID_H__

#include "config.hpp"
#include <bitset>

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



#endif
