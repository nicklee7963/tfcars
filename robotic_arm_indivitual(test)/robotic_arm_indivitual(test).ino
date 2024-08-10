#include <math.h>
int convertion = (180/3.1415);
int length1 = a;
int length2 = b;
void moveToPos(double x, double y, double z){
    double b = atan(y,x) * convertion;

    double l = sqrt(x*x + y*y);

    double h = sqrt(l*l + z*z);

    double phi = atan(z/l) * convertion;

    double theta = acos((a*a + h*h - b*b)/(2 * a * h)) * convertion;

    double lamda = acos((b * b + h * h - a * a) / (2 * b * h)) * conversion;

    double a1 = theta + phi;

    double a2 = phi - lamda;

    moveToAngle(b,a1,a2);
}


void setup()
{
    
}

void loop()
{
    
}