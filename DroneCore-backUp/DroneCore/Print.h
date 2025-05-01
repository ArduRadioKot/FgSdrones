#ifndef PRINT_H
#define PRINT_H

// Класс для работы с последовательной печатью.
class MyPrint {
public:
    // Печать текста без переноса строки.
    static void printSerial(const String &params) {
        if (Assign::find_var(params) != -1) {
            Serial.print(variable[Assign::find_var(params)].var);
        } else if (params.startsWith("\"") && params.endsWith("\"")) {
            Serial.print(params.substring(1, params.length() - 1));
        } else {
            Serial.print(params);
        }
    }

    // Печать текста с переносом строки.
    static void printlnSerial(const String &params) {
        if (Assign::find_var(params) != -1) {
            Serial.println(variable[Assign::find_var(params)].var);
        } else if (params.startsWith("\"") && params.endsWith("\"")) {
            Serial.println(params.substring(1, params.length() - 1));
        } else {
            Serial.println(params);
        }
    }
};

MyPrint myPrint;
#endif