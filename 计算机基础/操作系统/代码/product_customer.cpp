// 生产者消费者模型
// Work On Linux: g++ product_customer.cpp -o product_customer.out && ./product_customer.out
#include "iostream"
#include <unistd.h>

#define N 20

using namespace std;

// 信号量结构体定义
struct SemData {
    int Sem;
};

// 生产者代码
int funcProductWrite(SemData* mutex, SemData* fullBuffer, SemData* emptyBuffer){
    
    if (emptyBuffer->Sem > 0) {

        if (mutex->Sem != 0) {
            // 缓冲区没有锁 栈未满
            mutex->Sem = 0;
            cout << "生产者开始写..." << endl;
            sleep(1);
            mutex->Sem = 1;
            fullBuffer->Sem += 1;
            emptyBuffer->Sem -= 1;
            return 0;
        } else {
            cout << "缓冲区有锁！" << endl;
            return 1;
        }
        
    } else {
        cout << "栈溢出！" << endl;
        return 1;
    }
}

// 消费者代码
int funcCustomerRead(SemData* mutex, SemData* fullBuffer, SemData* emptyBuffer){

    if (fullBuffer->Sem > 0) {

        if (mutex->Sem != 0) {
            // 缓冲区没有锁 栈非空
            mutex->Sem = 0;
            cout << "消费者开始读..." << endl;
            sleep(1);
            mutex->Sem = 1;
            fullBuffer->Sem -= 1;
            emptyBuffer->Sem += 1;
            return 0;
        } else {
            cout << "缓冲区有锁！" << endl;
            return 1;
        }

    } else {
        cout << "栈为空！" << endl;
        return 1;
    }
    
}

int main(){
    // 信号量初始化
    SemData* mutex = new SemData;
    SemData* fullBuffer = new SemData;
    SemData* emptyBuffer = new SemData;
    int flag = 0;

    mutex->Sem = 1;
    fullBuffer->Sem = 0;
    emptyBuffer->Sem = N;

    // 正常情况
    cout << "正常情况..." << endl;
        
    flag = funcProductWrite(mutex, fullBuffer, emptyBuffer);
    printf("Flag is %d, Mutex:%d, FullBuffer:%d, EmptyBuffer:%d \n", flag, mutex->Sem, fullBuffer->Sem, emptyBuffer->Sem);
    
    flag = funcCustomerRead(mutex, fullBuffer, emptyBuffer);
    printf("Flag is %d, Mutex:%d, FullBuffer:%d, EmptyBuffer:%d \n", flag, mutex->Sem, fullBuffer->Sem, emptyBuffer->Sem);

    // 无数据读
    cout << "无数据读..." << endl;

    flag = funcCustomerRead(mutex, fullBuffer, emptyBuffer);
    printf("Flag is %d, Mutex:%d, FullBuffer:%d, EmptyBuffer:%d \n", flag, mutex->Sem, fullBuffer->Sem, emptyBuffer->Sem);

    // 写满数据
    cout << "满数据写..." << endl;
    
    for(;;) {
        try {
            flag = funcProductWrite(mutex, fullBuffer, emptyBuffer);
            printf("Flag is %d, Mutex:%d, FullBuffer:%d, EmptyBuffer:%d \n", flag, mutex->Sem, fullBuffer->Sem, emptyBuffer->Sem);
            throw flag;
        }  
        catch (int f){
            if (f != 0){
                break;
            } else {
                continue;
            }
        }
    }

    // 读空数据
    cout << "空数据读..." << endl;
    
    for(;;) {
        try {
            flag = funcCustomerRead(mutex, fullBuffer, emptyBuffer);
            printf("Flag is %d, Mutex:%d, FullBuffer:%d, EmptyBuffer:%d \n", flag, mutex->Sem, fullBuffer->Sem, emptyBuffer->Sem);
            throw flag;
        }  
        catch (int f){
            if (f != 0){
                break;
            } else {
                continue;
            }
        }
    }
    
    return 0;
}