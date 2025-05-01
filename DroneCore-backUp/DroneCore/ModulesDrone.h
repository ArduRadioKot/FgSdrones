#include "AuxFunc.h"
#include "Assign.h"
#include "Del.h"
#include "Pin.h"
#include "Print.h"
#include "DroneCommand.h"
// Парсер команд.
class CommandParser {
public:
    void parse(String args) {
        int startParams = args.indexOf('(');
        int endParams = args.lastIndexOf(')');
        String commands = args.substring(0, startParams);
        String command_1, command_2;

        // Разделение команды на основные и подкоманды.
        if (commands.indexOf(".") != 1) {
            int dot = commands.indexOf('.');
            command_1 = commands.substring(0, dot);
            command_2 = commands.substring(dot + 1);
        } else {
            command_1 = commands;
        }

        String params = args.substring(startParams + 1, endParams);
        // Обработка команд.
        //Print.h
        if (command_1 == "print") {
            if (command_2 == "Serial") {
                MyPrint::printSerial(params);
            } else if (command_2 == "lnSerial") {
                MyPrint::printlnSerial(params);
            } else {
                Serial.println("Error: command not found");
            }
        //Pin.h
        } else if (command_1 == "pin") {
            if (command_2 == "read") {
                Pin::read(params);
            } else if (command_2 == "write") {
                Pin::write(params);
            } else if (command_2 == "init") {
                Pin::init(params);
            } else {
                Serial.println("Error: command not found");
            }
        //Assign.h
        } else if (command_1 == "assign") {
            Assign::tramit_var(params);
        //Del.h
        } else if (command_1 == "delay"){
            del.Delay(params);
        //DroneCommand.h
        } else if (command_1 == "drone"){
            if (command_2 == "init"){
              droneComm.drone_init();
            } else if (command_2 == "check_x"){
              droneComm.check_accel_x();
            } else if (command_2 == "check_y"){
              droneComm.check_accel_y();
            } else if (command_2 == "check_z"){
              droneComm.check_accel_z();
            } else if (command_2 == "up"){
              droneComm.check_up(params, "up");
            } else if(command_2 == "idle"){
              droneComm.check_up(params, "idle");
            } else if(command_2 == "forward") {
              droneComm.check_up(params, "forward");
            } else if (command_2 == "back"){
              droneComm.check_up(params, "back");
            }
            else {
              Serial.println("Error: command not found");
            }
        } else {
          Serial.println("Error: command not found");
        }
    }
};

// Глобальные объекты.
CommandParser commandParser;
