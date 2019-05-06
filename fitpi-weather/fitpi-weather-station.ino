#include <dht.h>
#include <LiquidCrystal.h>

#include <SoftwareSerial.h>
#define RX 10
#define TX 9
SoftwareSerial esp8266(RX,TX);

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

dht DHT;

#define DHT11_PIN 7

String AP = "DIGI-7sH7";
String PASS = "bb39ZbX7";
String API = "R3ZORA3750S0QXRN";
String HOST = "api.thingspeak.com";
String PORT = "80";
String field = "field1";
int countTrueCommand;
int countTimeCommand; 
boolean found = false; 
String valSensor = "";

void setup(){
  Serial.begin(9600);
  lcd.begin(16, 2);
  esp8266.begin(115200);
  esp8266.println("AT+CWMODE=1");
  //sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK");
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  lcd.setCursor(0,0); 
  lcd.print("Temp: ");
  lcd.print(DHT.temperature);
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  lcd.print(DHT.humidity);
  lcd.print("%");

  Serial.print(DHT.temperature);
  Serial.print("\t"); // for splitting
  Serial.print(DHT.humidity);
  Serial.print("\n"); // for new line

  //valSensor = getSensorData();
  //String getData = "GET /update?api_key="+ API +"&"+ field +"="+String(valSensor);
  //sendCommand("AT+CIPMUX=1",5,"OK");
  //sendCommand("AT+CIPSTART=0,\"TCP\",\""+ HOST +"\","+ PORT,15,"OK");
  //sendCommand("AT+CIPSEND=0," +String(getData.length()+4),4,">");
  //esp8266.println(getData);
  //delay(1500);
  //countTrueCommand++;
  //sendCommand("AT+CIPCLOSE=0",5,"OK");
 
  delay(3000);
}

String getSensorData() {
  return ""+String(DHT.temperature)+","+String(DHT.humidity)+"";
}

void sendCommand(String command, int maxTime, char readReplay[]) {
  Serial.print(countTrueCommand);
  Serial.print(". at command => ");
  Serial.print(command);
  Serial.print(" ");
  while(countTimeCommand < (maxTime*1))
  {
    esp8266.println(command);//at+cipsend
    if(esp8266.find(readReplay))//ok
    {
      found = true;
      break;
    }
  
    countTimeCommand++;
  }
  
  if(found == true)
  {
    Serial.println("OYI");
    countTrueCommand++;
    countTimeCommand = 0;
  }
  
  if(found == false)
  {
    Serial.println("Fail");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }
  
  found = false;
 }
