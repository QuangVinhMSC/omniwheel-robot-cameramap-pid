#include "mbed.h"
#include "DigitalInOut.h"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include "USBSerial.h"
#include "string.h"

//Pin
PwmOut pwm1(D9);//D9
PwmOut pwm2(D1);//D1
PwmOut pwm3(D10);//D0
DigitalOut motor_dr1(A0);//A0
DigitalOut motor_dr2(A1);//A1
DigitalOut motor_dr3(A3);
InterruptIn encoder1A(D5);
InterruptIn encoder2A(D6);  
InterruptIn encoder3A(D2);
DigitalOut led(LED1);
static BufferedSerial pc(USBTX, USBRX);
//variable timertimer
using namespace std::chrono;
Timer t1,t2,t3;
long long unsigned int countTime1,countTime2,countTime3=0;
float current1,current2,current3;
float countTime11,countTime12;
float countTime21,countTime22;
float countTime31,countTime32;
const float Kp = 0.005;   // Hệ số P
const float Ki = 0.0025;  // Hệ số I
const float Kd = 0.00000005;  // Hệ số D
const float dt = 0.05;  // Thời gian lấy mẫu
int cr_direct = 0;
float targetVelocity1 = 100,targetVelocity2 = 100,targetVelocity3 = 100; // Target speed in RPM
float errorSum = 0.0;      // Error sum for integral term
float lastError = 0.0;     // Last error for derivative term


char buffer[18] = {};
char buffer_cpy[36] = {};
//variable serial
void read_serial()
{
    char buffer[18] = {};
    char buffer_cpy[36] = {};
        if (pc.readable()) {
            ThisThread::sleep_for(50ms);
            pc.read(buffer, 18);
            strcpy(buffer_cpy, buffer);
            sscanf(buffer_cpy, "%f,%f,%f", &targetVelocity1, &targetVelocity2,&targetVelocity3);
    }
}
float lowerthan1(float controlsignal)
{
    if (controlsignal>1) controlsignal = 1;
    else if (controlsignal<0) controlsignal = 0;
    return controlsignal;
}


float pidControl(float target, float current) {
    float error = target - current;
    float pTerm = Kp * error;
    errorSum += error * dt;
    float iTerm = Ki * errorSum;
    float dTerm = Kd * (error - lastError) ;
    lastError = error;
    double control_signal = pTerm + iTerm + dTerm;
    return control_signal;
}

void rpm1()
{
    t1.stop();
    countTime1 = duration_cast<microseconds>(t1.elapsed_time()).count();
    current1 = (60.0f/234.3f)/(countTime1/1000000.0f);
    countTime12=countTime11;
    countTime11=countTime1;
    countTime1 = (countTime12+countTime11+countTime1)/3;
    t1.reset();
    t1.start();
}
void rpm2()
{
    t2.stop();
    countTime2 = duration_cast<microseconds>(t1.elapsed_time()).count();
    current2 = (60.0f/234.3f)/(countTime1/1000000.0f);
    countTime22=countTime21;
    countTime21=countTime2;
    countTime2 = (countTime22+countTime21+countTime2)/3;
    t2.reset();
    t2.start();
}
void rpm3()
{
    t3.stop();
    countTime3 = duration_cast<microseconds>(t1.elapsed_time()).count();
    current3 = (60.0f/234.3f)/(countTime3/1000000.0f);
    countTime32=countTime31;
    countTime31=countTime3;
    countTime3 = (countTime32+countTime31+countTime3)/3;
    t3.reset();
    t3.start();
}
int main()
{
    pwm1.period_us(50);
    pwm2.period_us(50);
    pwm3.period_us(50);
    t1.start();
    t2.start();
    t3.start();
    encoder1A.rise(&rpm1);
    encoder2A.rise(&rpm2);
    encoder3A.rise(&rpm3);

    
    while (1){
    read_serial();
    float controlSignal1 = pidControl(targetVelocity1, current1);
    float controlSignal2 = pidControl(targetVelocity2, current2);
    float controlSignal3 = pidControl(targetVelocity3, current3);
    motor_dr1=cr_direct;
    motor_dr2=cr_direct;
    motor_dr3=cr_direct;
    pwm1.write(lowerthan1(controlSignal1));
    pwm2.write(lowerthan1(controlSignal1));
    pwm3.write(lowerthan1(controlSignal1));
    printf("rpm: %f %f %f \n",targetVelocity1,targetVelocity2,targetVelocity3);
    // uart.write(data,sizeof(data));
    // printf("buffer: %s\n", buffer);
    current1 =0;
    current2 =0;
    current3 =0;
    ThisThread::sleep_for(20ms);
    // if (targetVelocity1==150) led = 1;
    // else led = 0;
    }
}