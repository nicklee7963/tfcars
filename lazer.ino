int lazer = 8;
void setup(){
    pinMode(lazer,8);

}
void loop(){
    digitalWrite(lazer,1);
    delay(1000);
    digitalWrite(lazer,0);
    delay(1000);
}
