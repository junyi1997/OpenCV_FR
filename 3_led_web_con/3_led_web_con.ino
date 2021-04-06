/*
 *  This sketch demonstrates how to set up a simple HTTP-like server.
 *  The server will set a GPIO pin depending on the request
 *    http://192.168.100.10/gpio/R_off will set the Red_LED low,
 *    http://192.168.100.10/gpio/R_on will set the Red_LED high
 *    http://192.168.100.10/gpio/Y_off will set the Yellow_LED low,
 *    http://192.168.100.10/gpio/Y_on will set the Yellow_LED high
 *    http://192.168.100.10/gpio/G_off will set the Green_LED low,
 *    http://192.168.100.10/gpio/G_on will set the Green_LED high
 *  server_ip is the IP address of the ESP8266 module, will be 
 *  printed to Serial when the module is connected.
 */

#include <ESP8266WiFi.h>

const char* ssid = "mmlab";
const char* password = "jjchen6669";
//const char* ssid = "19-1H5F";
//const char* password = "2268159779";

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);
int Step=0;
int LED_R=16;
int LED_Y=5;
int LED_G=4;

void setup() {
  Serial.begin(115200);
  delay(10);

  // prepare GPIO2
  pinMode(LED_R, OUTPUT);
  pinMode(LED_Y, OUTPUT);
  pinMode(LED_G, OUTPUT);
  digitalWrite(LED_R, 0);
  digitalWrite(LED_Y, 0);
  digitalWrite(LED_G, 0);
  
  Connect_to_WiFi_network();
  
}

void loop() {
  // Check if a client has connected
  if(digitalRead(4)==1){
    if(Step==0){
      Serial.println(WiFi.localIP());
      Step=1;
      delay(10);

  }}
  else{if(Step==1){Step=0;}}
  
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();
  
  // Match the request
  int val;
  if (req.indexOf("/gpio/R_off") != -1)
    // Set GPIO2 according to the request
    digitalWrite(LED_R, 0);
  else if (req.indexOf("/gpio/R_on") != -1)
    // Set GPIO2 according to the request
    digitalWrite(LED_R, 1);  
  else if (req.indexOf("/gpio/Y_off") != -1)
    // Set GPIO2 according to the request
    digitalWrite(LED_Y, 0);
  else if (req.indexOf("/gpio/Y_on") != -1)
    // Set GPIO2 according to the request
    digitalWrite(LED_Y, 1);
  else if (req.indexOf("/gpio/G_off") != -1)
    // Set GPIO2 according to the request
    digitalWrite(LED_G, 0);
  else if (req.indexOf("/gpio/G_on") != -1)
    // Set GPIO2 according to the request
    digitalWrite(LED_G, 1);    
  else if (req.indexOf("/gpio/stay") != -1){
    // Set GPIO2 according to the request

      digitalWrite(LED_Y, 1); 
      delay(500);
      digitalWrite(LED_Y, 0); 
      delay(500); 
    
    
    }
        
  else {
    Serial.println("invalid request");
    client.stop();
    return;
  }

  
  
  client.flush();

  // Prepare the response
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\nGPIO is now ";
  s += (val)?"high":"low";
  s += "</html>\n";

  // Send the response to the client
  client.print(s);
  delay(1);
  Serial.println("Client disonnected");

  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}

void Connect_to_WiFi_network(){
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
  digitalWrite(LED_R, 1);
  digitalWrite(LED_Y, 1);
  digitalWrite(LED_G, 1);
  delay(500);
  digitalWrite(LED_R, 0);
  digitalWrite(LED_Y, 0);
  digitalWrite(LED_G, 0);
}
