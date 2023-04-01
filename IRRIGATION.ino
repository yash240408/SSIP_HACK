#include <ESP8266WiFi.h>
#include <DHT.h>
#define trigPin D2
#define echoPin D3
#define DHTPIN D7

DHT dht(DHTPIN, DHT11);
 
const char* ssid="Bangladesh";
const char* password="yash1234";
const char* host="espnodewebsite.000webhostapp.com";
String ultrastatus ="SAFE";
String irstatus = "NO_OBSTACLE";
String sstatus = "NO_WATER_REQUIRED";
String wstatus = "TANK_FULL";
int sensor_pin = D5;
int water = A0;
int watervalue=0;
int buzz = D8;
int ir = D6;
int motor = D1;
void setup() 
{

  Serial.begin(115200);
  dht.begin();
  delay(100);
  Serial.println();
  Serial.println();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(sensor_pin,INPUT);
  pinMode(ir,INPUT);
  pinMode(water,INPUT);
  pinMode(DHTPIN,INPUT);
  pinMode(buzz,OUTPUT);
  pinMode(motor,OUTPUT);

 
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

  int irval=digitalRead(ir);
  float h;
  float t; 
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


//Obstacle detection Code 
//
if (irval==1)
{
  Serial.println("NO_OBSTACLE DETECTED");
  irstatus="NO_OBSTACLE";
//  digitalWrite(motor,LOW);
}
else
{
//  digitalWrite(motor,LOW);
  Serial.println("OBSTACLE DETECTED");
  irstatus ="OBSTACLE_DETECTED";
  Serial.print("connecting to ");
  Serial.println(host);
  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort))
{
    Serial.println("connection failed");
    return;
}
 
  String url =  "/API2/irsensorapi.php?irsensor=" + String(irval)+"&irstatus=" + String(irstatus);
  Serial.print("Requesting URL: ");
  Serial.println(url);
  
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);

while(client.available())
{
  String line = client.readStringUntil('\r');
  Serial.print(line);
}
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
}
//

//Ultrasonic Sensor Code


Serial.print(inches);
Serial.print("in, ");
Serial.print(cm);
Serial.print("cm");
Serial.println();



if(inches<10 && inches>=7)
{
  Serial.println("SAFE");
  ultrastatus = "SAFE";
//  digitalWrite(motor,LOW);
  noTone(buzz);
  Serial.print("connecting to ");
  Serial.println(host);
  
  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort)) 
{
  Serial.println("connection failed");
  return;
}

  String url2 = "/API2/ultrasonicapi.php?ussensor=" +String(inches)+"&ultrastatus=" + String(ultrastatus);
  Serial.print("Requesting URL: ");
  Serial.println(url2);
  
  client.print(String("GET ") + url2 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);
 
while(client.available())
{
  String line2 = client.readStringUntil('\r');
  Serial.print(line2);
}
 
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
}

else if(inches<7 && inches>=5)
{
  Serial.print("ALERT");
  ultrastatus="ALERT";
//  digitalWrite(motor,LOW);
  noTone(buzz);
  Serial.print("connecting to ");
  Serial.println(host);

  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort)) 
{
  Serial.println("connection failed");
  return;
}
  String url2 = "/API2/ultrasonicapi.php?ussensor=" +String(inches)+"&ultrastatus=" + String(ultrastatus);
  Serial.print("Requesting URL: ");
  Serial.println(url2);
 
  client.print(String("GET ") + url2 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);
 
while(client.available())
{
  String line2 = client.readStringUntil('\r');
  Serial.print(line2);
}
 
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
 
}

else if(inches<5 && inches>0)
{
  Serial.print("DANGER");
  ultrastatus="DANGER";
//  digitalWrite(motor,HIGH);
  tone(buzz,1100,500);
  Serial.print("connecting to ");
  Serial.println(host);

  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort)) 
{
  Serial.println("connection failed");
  return;
}
  String url2 = "/API2/ultrasonicapi.php?ussensor=" +String(inches)+"&ultrastatus=" + String(ultrastatus);
  Serial.print("Requesting URL: ");
  Serial.println(url2);
 
  client.print(String("GET ") + url2 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);
 
while(client.available())
{
  String line2 = client.readStringUntil('\r');
  Serial.print(line2);
}
 
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
  
}
 delay(200);


//WATER  SENSOR

watervalue = analogRead(water);
Serial.println("Water value is:");
Serial.println(watervalue);

if (watervalue <= 200)
{
  Serial.println("FILL_TANK");
  wstatus="FILL_TANK";
//  digitalWrite(motor,LOW);
}
else
{
  Serial.println("TANK_FULL");
  wstatus="TANK_FULL";
//  digitalWrite(motor,LOW);
  Serial.print("connecting to ");
  Serial.println(host);
  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort))
{
    Serial.println("connection failed");
    return;
}
 
  String url3 = "/API2/watersensorapi.php?wsensor=" + String(watervalue)+"&wstatus=" + String(wstatus);
  Serial.print("Requesting URL: ");
  Serial.println(url3);
  
  client.print(String("GET ") + url3 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);

while(client.available())
{
  String line3 = client.readStringUntil('\r');
  Serial.print(line3);
}
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
}

//DHT SENSOR CODE

h = dht.readHumidity();
t = dht.readTemperature();

if (isnan(h) || isnan (t))
{
Serial.println("Failed to read the DHT sensor");
return;  
//digitalWrite(motor,LOW);
 }
else
{
Serial.println("humidity value is:");
Serial.println(h);
Serial.println("temprature value is:");
Serial.println(t);
//digitalWrite(motor,LOW);
  Serial.print("connecting to ");
  Serial.println(host);
  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort))
{
    Serial.println("connection failed");
    return;
}
 
  String url4 =  "/API2/tempapi.php?temp=" + String(t)+"&hum=" + String(h);
  Serial.print("Requesting URL: ");
  Serial.println(url4);
  
  client.print(String("GET ") + url4 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);

while(client.available())
{
  String line4 = client.readStringUntil('\r');
  Serial.print(line4);
}
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
}


//soil moisture code
//int moisture_percentage;
int moisturevalue=digitalRead(sensor_pin);
// 
//  moisture_percentage = ( 100.00 - ( (digitalRead(sensor_pin)/1023.00) * 100.00 ) );
 
//    Serial.println("Soil Moisture(in Percentage) = ");
//    Serial.println(moisture_percentage);
//    Serial.print("%");
//    Serial.println("Soil Moisture Monitor");
//    Serial.println(moisture_percentage);

Serial.println("Soil Moisture=");
Serial.println(moisturevalue);
if (moisturevalue==0)
{
  Serial.println("NO_WATER_REQUIRED");
  sstatus="NO_WATER_REQUIRED";
//  digitalWrite(motor,LOW);
}
else
{
  Serial.println("WATER_REQUIRED");
  sstatus="WATER_REQUIRED";
//  digitalWrite(motor,HIGH);
  Serial.print("connecting to ");
  Serial.println(host);
  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort))
{
    Serial.println("connection failed");
    return;
}
 
  String url5 =  "/API2/soilapi.php?ssensor=" + String(moisturevalue)+"&sstatus=" + String(sstatus);
  Serial.print("Requesting URL: ");
  Serial.println(url5);
  
  client.print(String("GET ") + url5 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);

while(client.available())
{
  String line5 = client.readStringUntil('\r');
  Serial.print(line5);
}
  Serial.println();
  Serial.println("closing connection");
  delay(3000);
}

 Serial.print("connecting to ");
  Serial.println(host);
  WiFiClient client;
  const int httpPort = 80;
  
if (!client.connect(host, httpPort))
{
    Serial.println("connection failed");
    return;
}
 
  String url6 =  "/API2/warningapi.php?ustatus=" + String(ultrastatus)+"&dhth=" + String(h) +"&dhtt=" + String(t)+"&irstatus=" + String(irstatus)+"&sstatus=" + String(sstatus)+"&wstatus=" + String(wstatus);
  Serial.print("Requesting URL: ");
  Serial.println(url6);
  
  client.print(String("GET ") + url6 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(500);

while(client.available())
{
  String line6 = client.readStringUntil('\r');
  Serial.print(line6);
}
  Serial.println();
  Serial.println("closing connection");
  delay(3000);

if((moisturevalue==1 || moisturevalue==0) && watervalue <= 100)
{
Serial.println("THE WATER IS PROCESSING FOR");
digitalWrite(motor,HIGH);
}
else if((moisturevalue==1 || moisturevalue==0) && watervalue >=150)
{
  digitalWrite(motor,LOW);
}
else
{
  digitalWrite(motor,LOW);
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
