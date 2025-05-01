#ifndef AUXFUNC_H
#define AUXFUNC_H
class Aux{
public:
    bool isNumber(const String &str) {
        return str.length() > 0 && (str.toInt() != 0 || str == "0");
    }
};
Aux aux;
#endif