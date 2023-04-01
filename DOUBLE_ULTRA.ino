#include <ESP8266WiFi.h>
#define trigPin D2
#define echoPin D3
#define trigPin1 D5
#define echoPin1 D6
 
const char* ssid="Bangladesh";
const char* password="yash1234";
const char* host="espnodewebsite.000webhostapp.com";
String ultrastatus =  "SAFE";
String ultrastatus1 = "SAFE";
int buzz = D8;
int motor = D1;

void setup() 
{

  Serial.begin(115200);
  delay(100);
  Serial.println();
  Serial.println();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(motor, OUTPUT);
  pinMode(buzz,OUTPUT);

 
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Netmask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway: ");
  Serial.println(WiFi.gatewayIP());
}


void loop() 
{
  long duration, inches, cm;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);
  
  // Take reading on echo pin
  duration = pulseIn(echoPin, HIGH);
  
  // convert the time into a distance
  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);
  
// Now adding all the code   

//Ultrasonic Sensor Code

Serial.println("DATA OF ULTRA1");
Serial.print(inches);
Serial.print("in, ");
Serial.print(cm);
Serial.print("cm");
Serial.println();



if(inches<10 && inches>=7)
{
  Serial.println("SAFE");
  ultrastatus = "SAFE";
  noTone(buzz);
  digitalWrite(motor,LOW);
}

else if(inches<7 && inches>=5)
{
  Serial.print("ALERT");
  ultrastatus="ALERT";
  noTone(buzz);
}
else if(inches<5 && inches>0)
{
  Serial.print("DANGER");
  ultrastatus="DANGER";
  tone(buzz,1000,500);   
  digitalWrite(motor,HIGH);
}

long duration1, inches1, cm1;
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin1, LOW);
  
  // Take reading on echo pin
  duration1 = pulseIn(echoPin1, HIGH);
  
  // convert the time into a distance
  inches1 = microsecondsToInches1(duration1);
  cm1 = microsecondsToCentimeters1(duration1);
  
// Now adding all the code   

//Ultrasonic Sensor Code

Serial.println("DATA OF ULTRA 2");
Serial.print(inches1);
Serial.print("in, ");
Serial.print(cm1);
Serial.print("cm");
Serial.println();



if(inches1<10 && inches1>=7)
{
  Serial.println("SAFE");
  ultrastatus1 = "SAFE";
  noTone(buzz);
}

else if(inches1<7 && inches1>=5)
{
  Serial.print("ALERT");
  ultrastatus1="ALERT";
  noTone(buzz);
}
else if(inches1<5 && inches1>0)
{
  Serial.print("DANGER");
  ultrastatus1="DANGER";
  tone(buzz,1000,500);   
}

}
 
long microsecondsToInches(long microseconds)
{
return microseconds/74/2;
}

long microsecondsToCentimeters(long microseconds)
{
return microseconds /29/2;
}
long microsecondsToInches1(long microseconds)
{
return microseconds/74/2;
}

long microsecondsToCentimeters1(long microseconds)
{
return microseconds /29/2;
}
