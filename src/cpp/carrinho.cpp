#include <iostream>		// Include all needed libraries here
#include <wiringPi.h>

using namespace std;		// No need to keep using “std”

int main()
{
wiringPiSetup();			// Setup the library
pinMode(0, OUTPUT);		// Configure GPIO0 as an output
pinMode(1, OUTPUT);		// Configure GPIO0 as an output
pinMode(2, OUTPUT);		// Configure GPIO0 as an output
pinMode(3, OUTPUT);		// Configure GPIO0 as an output


void frente()
{
	digitalWrite(0, 1);
    digitalWrite(1, 1);
    delay(500); 
    return
}

void direita()
{
    digitalWrite(0, 1);
    digitalWrite(1, 0);
    delay(500); 
    return;
}

void esquerda()
{
    digitalWrite(0, 0);
    digitalWrite(0, 0);
    delay(500); 
    return;
}

int count=0;
// Main program loop
while(count>10)
{
	frente():
    direita(); 
    esquerda();
    count++;
}
	return 0;
}