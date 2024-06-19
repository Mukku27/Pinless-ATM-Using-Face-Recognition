#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <EEPROM.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Keypad setup
const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// EEPROM addresses for storing data
#define USER_COUNT_ADDR 0
#define USERS_START_ADDR 10
#define MAX_USERS 10
#define TRANSACTION_HISTORY_LENGTH 5

struct User {
  char name[10];
  float balance;
  float transactions[TRANSACTION_HISTORY_LENGTH];
  byte transactionIndex;
};

User users[MAX_USERS];
int userCount = 0;
int currentUserIndex = -1;
bool authenticated = false;

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");

  // Load user data from EEPROM
  userCount = EEPROM.read(USER_COUNT_ADDR);
  if (userCount > MAX_USERS) userCount = MAX_USERS;
  for (int i = 0; i < userCount; i++) {
    int addr = USERS_START_ADDR + sizeof(User) * i;
    EEPROM.get(addr, users[i]);
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Welcome to ATM");
}

void loop() {
  if (!authenticated) {
    authenticateUser();
  } else {
    showMainMenu();
  }
}

void authenticateUser() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Please Show Your Face");

  // Replace with face recognition logic

  // Simulating authentication for demonstration
  delay(2000);
  authenticated = true;
  currentUserIndex = 0;  // Assuming only one user for demonstration
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Welcome, ");
  lcd.print(users[currentUserIndex].name);
  delay(2000);
}

void showMainMenu() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("1.Balance 2.Withdraw");
  lcd.setCursor(0, 1);
  lcd.print("3.Deposit 4.More");

  char option = getKeypadInput();
  switch (option) {
    case '1':
      showBalance();
      break;
    case '2':
      withdrawMoney();
      break;
    case '3':
      depositMoney();
      break;
    case '4':
      showMoreOptions();
      break;
    default:
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Invalid Option");
      delay(2000);
      break;
  }
}

void showBalance() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Balance:");
  lcd.setCursor(0, 1);
  lcd.print(users[currentUserIndex].balance);
  delay(3000);
}

void withdrawMoney() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Enter Amount:");

  float amount = getAmountInput();
  if (amount <= 0) return;

  if (users[currentUserIndex].balance >= amount) {
    users[currentUserIndex].balance -= amount;
    addTransaction(-amount);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Withdrawn:");
    lcd.setCursor(0, 1);
    lcd.print(amount);
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Insufficient Funds");
  }
  delay(3000);
}

void depositMoney() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Enter Amount:");

  float amount = getAmountInput();
  if (amount <= 0) return;

  users[currentUserIndex].balance += amount;
  addTransaction(amount);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Deposited:");
  lcd.setCursor(0, 1);
  lcd.print(amount);
  delay(3000);
}

void showMoreOptions() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("1.Change PIN");
  lcd.setCursor(0, 1);
  lcd.print("2.Mini Statement");

  char option = getKeypadInput();
  switch (option) {
    case '1':
      changePIN();  // You may remove this section if not needed
      break;
    case '2':
      showMiniStatement();
      break;
    default:
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Invalid Option");
      delay(2000);
      break;
  }
}

void showMiniStatement() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Mini Statement");
  for (int i = 0; i < TRANSACTION_HISTORY_LENGTH; i++) {
    int index = (users[currentUserIndex].transactionIndex - i - 1 + TRANSACTION_HISTORY_LENGTH) % TRANSACTION_HISTORY_LENGTH;
    if (users[currentUserIndex].transactions[index] != 0) {
      lcd.setCursor(0, 1);
      lcd.print(users[currentUserIndex].transactions[index]);
      delay(2000);
    }
  }
}

void addTransaction(float amount) {
  users[currentUserIndex].transactions[users[currentUserIndex].transactionIndex] = amount;
  users[currentUserIndex].transactionIndex = (users[currentUserIndex].transactionIndex + 1) % TRANSACTION_HISTORY_LENGTH;
}

float getAmountInput() {
  float amountInput = 0.0;
  // Replace with keypad or other input method logic if needed
  return amountInput;
}

char getKeypadInput() {
  char key;
  // Replace with keypad input logic if needed
  return key;
}
