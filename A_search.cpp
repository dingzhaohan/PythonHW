
#include <iostream>
#include <vector>
using namespace std;
int m, n;

class State {
public:
    int leftmissionaries;//左岸传教士人数
    int leftcannibals;//左岸食人族人数
    int boat;//0-船在右边，1-船在左边
    int depth;//已经花费的代价
    int f;//评估值

    State(int _m, int _c, int _b, int _depth):leftmissionaries(_m), leftcannibals(_c), boat(_b), depth(_depth), f(10000) {}

    State(const State &s) {
        leftmissionaries = s.leftmissionaries;
        leftcannibals = s.leftcannibals;
        boat = s.boat;
        depth = s.depth;
        f = s.f;
    }

    State() {}

    //判断相等的时候只判断状态，不用管评估值，不准...
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

    //计算评估值
    int evaluate() {
        return depth + leftmissionaries + leftcannibals - 2 * boat;
    }

};

vector<State> openset;
vector<State> closeset;
vector<State> subStateOfCurrent;//当前结点扩展出来的子节点

//计算open表中的评估值最小的一个，并返回，也就是下一步要走的地方
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

//判断该节点是否在open表里
bool judgeIsInOpenSet(State s) {

    for(vector<State>::iterator it = openset.begin(); it != openset.end(); it++) {
        if(s == *it) return true;
    }

    return false;
}

//判断该节点是否在close表里
bool judgeIsInCloseSet(State s) {

    for(vector<State>::iterator it = closeset.begin(); it != closeset.end(); it++) {
        if(s == *it) return true;
    }

    return false;
}

//扩展当前结点，合法即可扩展，不用考虑是否在open、close中，把合法的全部放到subStateOfCurrent容器里  
void expand(State s) {

    for(int i = 0; i <= n; ++i) {
        for(int j = 0; j <= n; ++j) {
            //判断船上的是不是ok
            if(i + j == 0) continue;//空船
            else if(i + j > n) continue;//超载
            else if(i < j) continue;//船上的传教士被吃了
            else if(s.boat == 1 && (i > s.leftmissionaries || j > s.leftcannibals)) continue;//船在左边，要往右走，船上的人不能比岸上的人多
            else if(s.boat == 0 && (i > m - s.leftmissionaries || j > m - s.leftcannibals)) continue;
            else if(s.boat == 1 && (s.leftmissionaries - i) < (s.leftcannibals - j) && (s.leftmissionaries - i) != 0) continue;//船往右，如果左岸还有传教士，那么左岸剩下的传教士不能比食人族少
            else if(s.boat == 0 && (m - s.leftmissionaries - i < m - s.leftcannibals - j && m - s.leftmissionaries - i!= 0)) continue;//船要往左,如果右岸还有传教士，那么剩下的传教士人数不能比食人族少
            else {
                //这就是一个合法的节点，不考虑是否重复了，把它放到subStateOfCurrent表里去，并且这一次访问到这个节点的depth是母节点depth+1
                State sons(s.leftmissionaries - i, s.leftcannibals - j, !s.boat, s.depth + 1);

                //算出该节点的评估值
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

        //拿出open表中评估值最小的节点
        State current(caculateminState());

        //如果是目标节点，输出即可
        if(current == goal) {

            cout << current.depth << endl;
            return 0;

        } else {

            //否则扩展当前结点
            expand(current);

            //对于每一个字节点，判断它是否在open表中，如果在，计算它这一次的评估值，小的话就更新open表，或者是否在close表中，如果在，计算它这一次的评估值，如果这次的评估值小于上一次，就把它拿出来放到open表里
            for(vector<State>::iterator it = subStateOfCurrent.begin(); it !=subStateOfCurrent.end(); ++it) {
                if(judgeIsInOpenSet(*it)) {

                    //如果该节点在open表中，找出是open表中的哪一个，做相应计算或者更新评估值
                    for(vector<State>::iterator it1 = openset.begin(); it1 != openset.end(); ++it1) {
                        if(*it1 == *it) {

                            
                            if(it->f < it1->f) {
                                it1->f = newEvaluation;//更新open表里该节点的评估值
                            }
                            break;
                        }
                    }

                } else if(judgeIsInCloseSet(*it)) {

                    for(vector<State>::iterator it1 = closeset.begin(); it1 != closeset.end(); ++it1) {
                        if(*it1 == *it) {
                           
                            if(it->f < it1->f) {

                                //加到open表里，并从close中删除
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

            //清空这次到subStateOfCurrent表

            subStateOfCurrent.clear();

            current.f = current.evaluate();
            closeset.push_back(current);


        }
    }
}

