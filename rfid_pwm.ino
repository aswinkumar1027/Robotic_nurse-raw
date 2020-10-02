#include <SPI.h>

#include <MFRC522.h>



#define SS_PIN 10

#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

#define PWM_MOTOR_1 3
#define PWM_MOTOR_2 6

void setup() 

{

 Serial.begin(19200);   // Initiate a serial communication

 SPI.begin();      // Initiate  SPI bus

 mfrc522.PCD_Init();   // Initiate MFRC522

 //Serial.println("Approximate your card to the reader...");

 //Serial.println();
 
 pinMode(PWM_MOTOR_1, OUTPUT);
 pinMode(PWM_MOTOR_2, OUTPUT);
}

void loop() 
{

 analogWrite(PWM_MOTOR_1, 120);
 analogWrite(PWM_MOTOR_2, 120);
 // Look for new cards

 if ( ! mfrc522.PICC_IsNewCardPresent()) 

 {
   return;

 }

 // Select one of the cards

 if ( ! mfrc522.PICC_ReadCardSerial()) 

 {

   return;

 }

 //Show UID on serial monitor

 //Serial.print("UID tag :");

 //String content= "";

 byte letter;

 for (byte i = 0; i < mfrc522.uid.size; i++) 

 {

    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" :"");

    Serial.print(mfrc522.uid.uidByte[i], HEX);

    //content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));

    //content.concat(String(mfrc522.uid.uidByte[i], HEX));

 }
 Serial.println();
 delay(5);

 
}
