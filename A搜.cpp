
#include <iostream>
#include <vector>
using namespace std;
int m, n;

class State {
public:
    int leftmissionaries;
    int leftcannibals;
    int boat;
    int depth;
    int f;

    State(int _m, int _c, int _b, int _depth):leftmissionaries(_m), leftcannibals(_c), boat(_b), depth(_depth), f(10000) {}

    State(const State &s) {
        leftmissionaries = s.leftmissionaries;
        leftcannibals = s.leftcannibals;
        boat = s.boat;
        depth = s.depth;
        f = s.f;
    }

    State() {}

    bool legal() {
        //判断状态是否合法

        return false;
        return true;
    }

    bool operator == (State s) {
        return (boat == s.boat && leftmissionaries == s.leftmissionaries && leftcannibals == s.leftcannibals);
    }

    void operator = (State s) {
        leftmissionaries = s.leftmissionaries;
        leftcannibals = s.leftcannibals;
        boat = s.boat;
        depth = s.depth;
        f = s.f;
    }
    int evaluate() {
        return depth + leftmissionaries + leftcannibals - 2 * boat;
    }

};

vector<State> openset;
vector<State> closeset;
vector<State> subStateOfCurrent;

State caculateminState() {
    vector<State>::iterator re;
    int minEvalueate = 100000;

    for(vector<State>::iterator it = openset.begin(); it != openset.end(); it++) {
        if(minEvalueate < it->f) {
            re = it;
            minEvalueate = it->f;

        }
    }
    return *re;

}

bool judgeIsInOpenSet(State s) {

    for(vector<State>::iterator it = openset.begin(); it != openset.end(); it++) {
        if(s == *it) return true;
    }

    return false;
}

bool judgeIsInCloseSet(State s) {

    for(vector<State>::iterator it = closeset.begin(); it != closeset.end(); it++) {
        if(s == *it) return true;
    }

    return false;
}

void expand(State s) {

    for(int i = 0; i <= n; ++i) {
        for(int j = 0; j <= n; ++j) {
            //判断船上的是不是ok
            if(i + j == 0) continue;
            else if(i + j > n) continue;
            else if(i < j) continue;
            else if(i > s.leftmissionaries || j > s.leftcannibals) continue;
            else if(s.leftmissionaries < s.leftcannibals && s.leftmissionaries != 0) continue;
            else if(m - s.leftmissionaries - i < m - s.leftcannibals - j && s.leftmissionaries + i != m) continue;
            else {

                State sons(s.leftmissionaries - i, s.leftcannibals - j, !s.boat, s.depth + 1);
                sons.f = sons.evaluate();
                subStateOfCurrent.push_back(sons);

            }
        }
    }

}

int main() {

    cin >> m >> n;

    State init(m, m, 1, 0);
    State goal(0, 0, 0, 10000);

    openset.push_back(init);

    while(!openset.empty()) {
        State current(caculateminState());

        current.f = current.evaluate();
        closeset.push_back(current);

        if(current == goal) {

            cout << current.depth << endl;
            return 0;

        } else {

            expand(current);

            for(vector<State>::iterator it = subStateOfCurrent.begin(); it !=subStateOfCurrent.end(); ++it) {
                if(judgeIsInOpenSet(*it)) {

                    for(vector<State>::iterator it1 = openset.begin(); it1 != openset.end(); ++it1) {
                        if(*it1 == *it) {
                            int newEvaluation = it->evaluate();
                            if(newEvaluation < it1->f) {
                                it1->f = newEvaluation;
                            }
                            break;
                        }
                    }

                } else if(judgeIsInCloseSet(*it)) {

                    for(vector<State>::iterator it1 = closeset.begin(); it1 != closeset.end(); ++it1) {
                        if(*it1 == *it) {
                            int newEvaluation = it->evaluate();
                            if(newEvaluation < it1->f) {

                                openset.push_back(*it);
                                closeset.erase(it1);
                                break;

                            }

                        }
                    }

                } else {

                    openset.push_back(*it);

                }
            }

            subStateOfCurrent.clear();

        }
    }
}


