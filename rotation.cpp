#include <iostream>
#include <cstring>
#include <string>
using namespace std;

int map[9][9];
int path[100000];
char rotation[8] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'};

void input() {
    memset(map, 0, sizeof(map));
    memset(path, -1, sizeof(path));
    cin >> map[1][3];
    if(map[1][3] == 0) return;
    cin >> map[1][5];
    cin >> map[2][3];
    cin >> map[2][5];
    for(int i = 1; i <= 7; ++i)
        cin >> map[3][i];
    cin >> map[4][3] >> map[4][5];

    for(int i = 1; i <= 7; ++i)
        cin >> map[5][i];

    for(int i = 6; i <= 7; ++i)
        cin >> map[i][3] >> map[i][5];

}

void print() {
    cout << number++ << endl;
    for(int i = 1; i <= 7; ++i) {
        for(int j = 1; j <= 7; ++j) {
            cout << map[i][j] << ' ';
        }
        cout << endl;
    }
}

//evaluate
int h() {
    
    int num[5];
    memset(num, 0, sizeof(num));

    for(int i = 3; i <= 5; ++i) {
        for(int j = 3; j <= 5; ++j) {
            if(!(i == 4 && j == 4)) num[map[i][j]]++;
        }
    }

    int maxnum = 0;
    for(int i = 1; i <= 3; ++i) {
        if(num[i] > maxnum) maxnum = num[i];
    }

    return 8 - maxnum;

}

bool judge() {

    int num[5];
    memset(num, 0, sizeof(num));

    for(int i = 3; i <= 5; ++i) {
        for(int j = 3; j <= 5; ++j) {
            if(!(i == 4 && j == 4)) num[map[i][j]]++;
        }
    }
    return (num[1] == 8 || num[2] == 8 || num[3] == 8);
}

void rotate(int i) {
    switch(i) {
        case 0:{//A
            for(int k = 0; k <= 6; ++k) {
                map[k][3] = map[k + 1][3];
            }
            map[7][3] = map[0][3];
        };break;
        case 1:{//B
            for(int k = 0; k <= 6; ++k) {
                map[k][5] = map[k + 1][5];
            }
            map[7][5] = map[0][5];
        };break;
        case 2:{//C
            for(int k = 8; k >= 2; --k) {
                map[3][k] = map[3][k - 1];
            }
            map[3][1] = map[3][8];
        };break;
        case 3:{//D
            for(int k = 8; k >= 2; --k) {
                map[5][k] = map[5][k - 1];
            }
            map[5][1] = map[5][8];
        };break;
        case 4:{//E
            for(int k = 8; k >= 2; --k) {
                map[k][5] = map[k - 1][5];
            }
            map[1][5] = map[8][5];
        };break;
        case 5:{//F
            for(int k = 8; k >= 2; --k) {
                map[k][3] = map[k - 1][3];
            }
            map[1][3] = map[8][3];
        };break;
        case 6:{//G
            for(int k = 0; k <= 6; ++k) {
                map[5][k] = map[5][k + 1];
            }
            map[5][7] = map[5][0];
        };break;
        case 7:{//H
            for(int k = 0; k <= 6; ++k) {
                map[3][k] = map[3][k + 1];
            }
            map[3][7] = map[3][0];
        };break;
        default:break;
    }

}
int value;

bool limited_depth_search(int depth, int bound) {

    if(judge()) return true;

    if(depth + h() > bound) return false;

    for(int i = 0; i < 8; ++i) {

        rotate(i);
        path[depth] = i;

        if(limited_depth_search(depth + 1, bound)) {
            value = map[3][3];
            return true;
        }
        switch(i) {
            case 0:rotate(5);break;
            case 1:rotate(4);break;
            case 2:rotate(7);break;
            case 3:rotate(6);break;
            case 4:rotate(1);break;
            case 5:rotate(0);break;
            case 6:rotate(3);break;
            case 7:rotate(2);break;
        }
        path[depth] = -1;
    }

    return false;

}
int main() {
    while(true) {
        input();
        if(map[1][3] == 0) break;
        if(judge()) {
            cout << "No moves needed" << endl;
            cout << map[3][3] << endl;
            continue;
        }
        for(int bound = 1; bound < 100; ++bound) {
            bool result = limited_depth_search(0, bound);
            if(result) {
                for(int i = 0; i < 100000; ++i) {
                    if(path[i] == -1) break;
                    cout << rotation[path[i]];
                }
                cout << endl;
                cout << value << endl;
                break;
            }
        }
    }
    return 0;
}






