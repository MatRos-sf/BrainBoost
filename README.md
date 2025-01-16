# BrainBoost

**Enhance Your Memory and Mental Math Skills**

BrainBoost is a desktop application designed to help you improve your memory and calculated skills. By incorporating engaging exercises and gamified activities, BrainBoost ensures that you can keep your brain sharp and track your progress over time.

---

## **Why I Created This Application**

After reading a book about memory, I was inspired to create a tool to practice and strengthen memory skills. The book emphasized the importance of exercising memory at any age. BrainBoost allows me to monitor my own progress while providing others with the same opportunity.

Additionally, this is my first GUI application. Through its development, I explored the Kivy framework and gained hands-on experience with database management using SQLAlchemy and Alembic.

---

## **Features**

### **User Authentication**
- Add new users to the database.
- Secure password hashing using **bcrypt**, ensuring that passwords are safely stored.
- Remember the last logged-in user for a seamless experience.

### **Language Support**
- Switch between Polish and English effortlessly with the built-in language toggle.

### **Session Management**
- Preserve user sessions and ensure game progress is saved.
- Automatically resume games at the appropriate difficulty level for each user.

### **Interactive Games**
- **Result Keeper**: A game focused on mental arithmetic and sequential memory.
- **Associative Changing**: An activity designed to improve creative memory techniques.
*(More details on the games can be found in the [Instructions](#instructions) section.)*

### **Other Features**
- Multi-screen navigation for a smooth user interface.
- Real-time data storage and management.
- Robust game logic to handle different difficulty levels and user progress.

---


## **Technologies Used**

This application was developed and tested on Linux using the following technologies:

- ![Python](https://img.shields.io/badge/Python-3.12-blue)
- ![Kivy](https://img.shields.io/badge/Kivy-Framework-brightgreen)
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange)
- ![Alembic](https://img.shields.io/badge/Alembic-Migrations-yellow)
- ![pytest](https://img.shields.io/badge/pytest-Testing-red)
- ![bcrypt](https://img.shields.io/badge/bcrypt-Security-lightblue)
- ![pre-commit](https://img.shields.io/badge/pre--commit-Code%20Style-yellowgreen)

---

## **Project Structure**

- **src**
    - `config`: Game configuration and language preferences.
    - `db`: Database management modules (`DBManager`) and user session logic.
    - `exceptions`: Custom exception handling.
    - `games`: Implementation of games and the scoring system.
    - `GUI`: The core of the application, including the main app logic and screen transitions.
    - `models`: Database models for structured data storage.
    - `users`: Password hashing and authentication mechanisms.

- **tests**
    - Basic unit tests to ensure application stability.

## **Installation**

To get started, clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/brainboost.git
cd brainboost
python3 -m venv .venv
pip install -r requirements.txt
```
---

## **Running the Application**

### **Method 1: Using Command Line**
1. Initialize the database:
```bash
alembic upgrade head
```
2. Run the main script:
```bash
python3 -m src.GUI.brain_boost_app
```

### **Method 2: Using Bash Script**
Simply execute the included script: `./run_app.sh`

---

## **Instructions**

### **Result Keeper Rules**
1. **Game Start:** A math operation is presented (e.g., 2 + 1). Calculate and remember the result (3).
2. **Next Steps:** A new operation appears, using the remembered number (e.g., remembered number × 2). Calculate the new result and provide the answer.
3. **Game End:** The game ends after 3 mistakes or 60 seconds.
4. **Difficulty Levels:** Answer 10 consecutive calculations correctly to increase the difficulty. Higher levels feature larger numbers and more complex operations.

### **Associative Changing Rules**
1. A list of nouns appears (e.g., Horse, Elephant, Eye).
2. Memorize and type the nouns in the correct order.
3. If you forget a word, replace it with “-” (e.g., Horse, -, Eye).
4. Scores are based on accuracy: perfect sequences yield maximum points, while placeholders reduce the score.

---
## **Future Plans**
* Add more games to further challenge users.
* Expand the test suite for improved reliability.
* Enhance the layout for a more modern and user-friendly design.

---
## **Contribute**
If you have suggestions or want to contribute to this project, feel free to reach out or create a pull request. Your feedback is welcome!



