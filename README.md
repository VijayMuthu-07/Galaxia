# Galaxia - A Space Enthusiasts' Hub

## Overview
Galaxia is a web application designed for space enthusiasts to connect, share, and stay updated with the latest developments in space exploration. Users can create an account, log in, and access various features, including posting multimedia content, chatting with other users, and reading the latest space news. 

## Features

### Authentication & User Management
- **User Registration**: New users can sign up using a simple and secure registration process.
- **User Login**: Registered users can log in using their credentials.
- **Password Management**: Users can change their password securely.
- **Account Deletion**: Users have the option to delete their accounts permanently.

### Social & Interactive Features
- **Chat System**: Users can chat with each other in real-time.
- **Multimedia Sharing**: Users can post photos and videos with captions.
- **News Feed**: A dedicated feed displaying user posts.
- **Space News Updates**: The latest space-related news fetched from an external API.

### Navigation Pages
- **Home (`index.html`)**: The main landing page of the website.
- **Login (`login.html`)**: A page for users to log in to their accounts.
- **Register (`register.html`)**: A page for new users to create an account.
- **About (`about.html`)**: Provides information about the web application and its purpose.
- **News (`news.html`)**: Displays space-related news using an API.
- **Feed (`feed.html`)**: Showcases user posts.
- **Chat (`chat.html`)**: Allows real-time communication between users.
- **Profile (`profile.html`)**: Displays user details and activity.
- **Settings (`settings.html`)**: Offers options such as change password, log out, about us, and delete account.
- **Change Password (`change.html`)**: Allows users to update their password securely.
- **Delete Account (`delete.html`)**: Provides an option to permanently remove a user account.

## Tech Stack
- **Frontend**:
  - HTML, CSS, JavaScript
  - Bootstrap for responsive design
- **Backend**:
  - Python (Flask framework)
  - SQLite3 for database management
- **APIs**:
  - External API for fetching space-related news

## Installation & Setup

### Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
- Flask
- SQLite3

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/galaxia.git
   cd galaxia
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```sh
   python setup_db.py  # This script initializes the database
   ```
5. Run the application:
   ```sh
   flask run
   ```
6. Open a browser and visit `http://127.0.0.1:5000/`

## Future Enhancements
- Implement a WebSocket-based real-time chat system
- Enable user profile customization with bio and profile picture
- Add a like and comment feature for posts
- Integrate OAuth for social media login

## License
This project is open-source and available under the MIT License.

## Contact
For any issues or contributions, feel free to reach out:
- Email: your-email@example.com

---

Enjoy exploring Galaxia and engaging with fellow space enthusiasts!

