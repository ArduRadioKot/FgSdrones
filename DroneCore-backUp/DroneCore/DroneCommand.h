#ifndef DRONE_COMMAND_H
#define DRONE_COMMAND_H

#include <basicMPU6050.h>

#define LU_Motor 7
#define RU_Motor 0
#define LD_Motor 5
#define RD_Motor 10
#define cnst 9.8

basicMPU6050<> imu;
bool start_drone;
float dev_x, dev_y;
int lu_cor, ru_cor, ld_cor, rd_cor;
class DroneComm {
public:
    void drone_init() {
        imu.setup();
        dev_x = imu.ax() * cnst;
        dev_y = imu.ay() * cnst;
        pinMode(LU_Motor, OUTPUT);
        pinMode(RU_Motor, OUTPUT);
        pinMode(LD_Motor, OUTPUT);
        pinMode(RD_Motor, OUTPUT);
        Serial.println(dev_x);
        Serial.println(dev_y);
        start_drone = true;
    }

    void check_accel_x() {
        Serial.println((imu.ax() * cnst) - dev_x);
    }

    void check_accel_y() {
        Serial.println((imu.ay() * cnst) - dev_y);
    }

    void check_accel_z() {
        Serial.println(imu.az() * cnst);
    }

    

    void check_up(String params, String comma) {
        unsigned long duration_ms = params.toInt();
        unsigned long start_time = millis();
        String type = comma;
        while (millis() - start_time < duration_ms) {
          if(type == "up"){
            up();
          } else if (type == "idle") {
              idle();
          } else if (type == "forward") {
              forward();
          } else if (type == "back"){
              back();
          }
        }
        idle();
        Serial.println("complete");
    }

private:
    void up() {
      lu_cor = 64 + (imu.ax() * 64) + (imu.ay() * 64);
      ru_cor = 64 + (imu.ax() * 64) - (imu.ay() * 64);
      ld_cor = 64 - (imu.ax() * 64) + (imu.ay() * 64);
      rd_cor = 64 - (imu.ax() * 64) - (imu.ay() * 64);
      analogWrite(LU_Motor, lu_cor);
      analogWrite(RU_Motor, ru_cor);
      analogWrite(LD_Motor, ld_cor);
      analogWrite(RD_Motor, rd_cor);
    }

    void idle() {
      while (start_drone) {
        lu_cor = 64 + (imu.ax() * 64) + (imu.ay() * 64) - ((imu.az() * 32) - 34.20  );
        ru_cor = 64 + (imu.ax() * 64) - (imu.ay() * 64) - ((imu.az() * 32) - 34.20  );
        ld_cor = 64 - (imu.ax() * 64) + (imu.ay() * 64) - ((imu.az() * 32) - 34.20  );
        rd_cor = 64 - (imu.ax() * 64) - (imu.ay() * 64) - ((imu.az() * 32) - 34.20  );
        analogWrite(LU_Motor, lu_cor);
        analogWrite(RU_Motor, ru_cor);
        analogWrite(LD_Motor, ld_cor);
        analogWrite(RD_Motor, rd_cor);
      }
    }

    void forward(){
        lu_cor = 64 + ((imu.ax() * 64) + (imu.ay() * 64)) - 30;
        ru_cor = 64 + ((imu.ax() * 64) - (imu.ay() * 64)) - 30;
        ld_cor = 64 - ((imu.ax() * 64) + (imu.ay() * 64)) + 25;
        rd_cor = 64 - ((imu.ax() * 64) - (imu.ay() * 64)) + 25;
        analogWrite(LU_Motor, lu_cor);
        analogWrite(RU_Motor, ru_cor);
        analogWrite(LD_Motor, ld_cor);
        analogWrite(RD_Motor, rd_cor);
    }

    void back(){
        lu_cor = 64 + ((imu.ax() * 64) + (imu.ay() * 64)) + 25;
        ru_cor = 64 + ((imu.ax() * 64) - (imu.ay() * 64)) + 25;
        ld_cor = 64 - ((imu.ax() * 64) + (imu.ay() * 64)) - 30;
        rd_cor = 64 - ((imu.ax() * 64) - (imu.ay() * 64)) - 30;
        analogWrite(LU_Motor, lu_cor);
        analogWrite(RU_Motor, ru_cor);
        analogWrite(LD_Motor, ld_cor);
        analogWrite(RD_Motor, rd_cor);
    }

};

DroneComm droneComm;

#endif
