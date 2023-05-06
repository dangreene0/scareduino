/* This is for the scariest of projects */
#include <SoftwareSerial.h>
#define ARDUINO_RX 5 // TX - Arduino RX
#define ARDUINO_TX 6 // RX - Arduino TX
SoftwareSerial mySerial(ARDUINO_RX, ARDUINO_TX);
static int8_t Send_buf[8] = {0};

#define DEV_TF 0X02
#define CMD_SEL_DEV 0X09
#define CMD_PLAY_W_VOL 0X22

#define trigPin 13
#define echoPin 10


void setup() {
  pinMode(2, INPUT_PULLUP);
  Serial.begin (9600);
  mySerial.begin(9600);
  sendCommand(CMD_SEL_DEV, DEV_TF);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

int trackNum = 0;
void loop() {
  int pinValue = digitalRead(2);
  delay(10);
  Serial.print("pinValue is ");
  Serial.println(pinValue);
  if (pinValue == 0) {
    if (trackNum == 1) {
      trackNum = 0;
      Serial.println("track 0");
      delay(5000);
    } 
    else{
      trackNum = 1;
      Serial.println("track 1");
      delay(5000);
    }
  }
  
  float duration, distance;
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) * 0.0344;

  if (distance <= 100) {
     Serial.println("BEEP");
     Serial.print("Distance = ");
     Serial.print(distance);
     Serial.println(" cm");
     if (trackNum == 0) {
        sendCommand(CMD_PLAY_W_VOL, 0X1E01);
        delay(10000);
     }
     if (trackNum == 1) {
        sendCommand(CMD_PLAY_W_VOL, 0X1E02);
        delay(10000);
     } 
  }
  else {
    Serial.print("Distance = ");
    Serial.print(distance);
    Serial.println(" cm");
    delay(500);
  }
  Serial.print("trackNum is ");
  Serial.println(trackNum);
  delay(100);
}

void sendCommand(int8_t command, int16_t dat)
{
  delay(20);
  Send_buf[0] = 0x7e; //starting byte
  Send_buf[1] = 0xff; //version
  Send_buf[2] = 0x06; //the number of bytes of the command without starting byte and ending byte
  Send_buf[3] = command; //
  Send_buf[4] = 0x00;//0x00 = no feedback, 0x01 = feedback
  Send_buf[5] = (int8_t)(dat >> 8);//datah
  Send_buf[6] = (int8_t)(dat); //datal
  Send_buf[7] = 0xef; //ending byte
  for(uint8_t i=0; i<8; i++)//
  {
    mySerial.write(Send_buf[i]) ;
  }
}
