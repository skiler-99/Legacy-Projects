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

## 🧠 Developer Journey: What I Learned
Building this project was a massive hands-on learning experience that pushed me past writing standard console applications and into the real-world software lifecycle. Here is a breakdown of the specific skills I leveled up today:

* **Advanced Java Swing (UI/UX):** Moved beyond basic grid layouts by implementing `CardLayout` for smooth screen transitions. I focused on modernizing the UI with custom hex color palettes, hover states, and using `javax.swing.Timer` to add professional pacing (victory pauses) to the gameplay loop.
* **The Maven Build Lifecycle:** Learned how to detach from IDE-dependent execution. I configured the `pom.xml` and utilized the `maven-assembly-plugin` to package the application and its environment into a standalone, executable "Fat JAR".
* **Debugging & Classpaths:** Successfully diagnosed and resolved `ClassNotFoundException` errors by aligning the project's package structure (`com.skiler`) with Maven's manifest configurations.
* **Version Control Management:** Mastered the process of migrating standalone Git projects into a larger portfolio monorepo (managing nested `.git` trackers) and pushing updates cleanly via GitHub Desktop.
* **Database Integration (Backend Prep):** Alongside this UI project, I successfully configured Java JDBC to connect to a local MySQL database, executing SQL queries (`ResultSet`) to securely retrieve and format inventory data.