#include "iostream"

using namespace std;

int main() {
    int i = 6;
    
    // 类比 Go 中的 fallthrough
    switch(i) {
        case 4: cout<<"was <= 4"<<endl;
        case 5: cout<<"was <= 5"<<endl;
        case 6: cout<<"was <= 6"<<endl;
        case 7: cout<<"was <= 7"<<endl;
        case 8: cout<<"was <= 8"<<endl;
        default: cout<<"default case"<<endl;        
    }

    return 0;
}