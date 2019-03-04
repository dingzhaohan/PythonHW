#include <iostream>
#include <set>
using namespace std;
int m, n;
int depth;

class State {
public:
    int leftmissionaries;
    int leftcannibals;
    int boat;
    int depth_;
    State(int _m, int _c, int _b, int __depth):leftmissionaries(_m), leftcannibals(_c), boat(_b), depth_(10000) {
        depth_ = __depth;
    }

    State(State &s) {
        leftmissionaries = s.leftmissionaries;
        leftcannibals = s.leftcannibals;
        boat = s.boat;
        depth_ = s.depth_;
    }    

    State() {}

    bool judge() {
        //判断状态是否合法
        if(leftmissionaries < leftcannibals && leftmissionaries != 0) return false;
        if(m - leftmissionaries < m - leftcannibals && leftmissionaries != m) return false;
        return true;
    }

    bool operator == (State s) {
        return (boat == s.boat && leftmissionaries == s.leftmissionaries && leftcannibals == s.leftcannibals);
    }

    bool operator < (State s) {
        return (depth_ + leftmissionaries - 2 * boat) < (s.depth_ + s.leftmissionaries - 2 * s.boat);
    }

    void operator = (State s, int d) {
        leftmissionaries = s.leftmissionaries;
        leftcannibals = s.leftcannibals;
        boat = s.boat;
        depth_ = d;
    }
};

set<State> openset;
set<State> closeset;

void func(State s) {

    set<State> temset;

    for(int i = 0; i <= n; ++i) {
            for(int j = 0; j <= n; ++j) {
                //判断船上的是不是ok
                if(i + j == 0) continue;
                if(i + j > n) continue;
                if(i < j) continue;

                State current(s.leftmissionaries - i, s.leftcannibals - j, !s.boat, s.depth_);
                if(current.judge() && !closeset.insert(current).second) temset.insert(current);

            }
        }

    openset.insert(temset.begin());
}
int main() {

    cin >> m >> n;
    depth = 0;

    State init(m, m, 1, 0);
    State goal(0, 0, 0, 10000);

    State flag;

    openset.insert(init);

    State current(openset.begin());
    while(!(current == goal) && !openset.empty()) {
        //扩展子节点
        depth++;

        current = 
        flag.depth_ = openset.begin().depth_;
        openset.erase(openset.begin());

        func(current);

    }

    cout << depth << endl;

    return 0;
}


