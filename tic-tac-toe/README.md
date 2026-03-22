# 🎮 Java Tic-Tac-Toe (Maven Project)

A modern, standalone desktop Tic-Tac-Toe game built entirely in Java. This project demonstrates core Object-Oriented Programming (OOP) principles, custom GUI design using Java Swing, and professional project management and packaging using Apache Maven.

## ✨ Features
* **Modern Dark-Mode UI:** Custom color palettes, hover effects, and clean typography.
* **Live Scoreboard:** Tracks Player X wins, Player O wins, and Draws in real-time.
* **Smart Win Detection:** Automatically highlights the winning row in neon green with a built-in victory pause before showing the final results screen.
* **Standalone Executable:** Packaged as a "Fat JAR" with the Maven Assembly Plugin, allowing the game to run flawlessly on any machine with Java installed.

## 🛠️ Tech Stack
* **Language:** Java
* **GUI Framework:** `javax.swing` / `java.awt`
* **Build Tool:** Apache Maven

## 🚀 How to Run

### Option 1: Run the Standalone .jar (Recommended)
You don't need an IDE to play the game! 
1. Navigate to the `target` folder.
2. Double-click the `tic-tac-toe-1.0-SNAPSHOT-jar-with-dependencies.jar` file.
*(Note: You must have the Java Runtime Environment installed on your system).*

### Option 2: Compile and Run from Source
If you want to build the project yourself using Maven:
1. Clone this repository to your local machine.
2. Open your terminal and navigate to the `tic-tac-toe` directory.
3. Run the following command to clean and build the executable:
   ```bash
   mvn clean package