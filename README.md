QuoraLite 📝
A Quora Clone Web Application
Built with Django by Pratik Agnihotri

#####################################################################################################################

🔥 About the Project
QuoraLite is a lightweight web-based Q&A platform inspired by Quora. It replicates core functionality including:

User Registration & Authentication

Posting Questions

Answering Questions

Liking Answers

View All Questions & Answers

All core features specified in the assignment email are implemented.

#####################################################################################################################

🚀 Getting Started
✅ Prerequisites
Make sure the following are installed:

Python 3.x

pip (Python package manager)

🛠️ Installation Steps
1️⃣ Clone the Repository

git clone git@github.com:King0311/QuoraLite.git
cd QuoraLite

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Navigate to Project Directory (where manage.py is located)
4️⃣ Run Migrations (if needed)

python manage.py makemigrations
python manage.py migrate

5️⃣ Create a Superuser

python manage.py createsuperuser

Follow the prompts to create an admin account.

6️⃣ Start the Development Server

python manage.py runserver

Visit http://127.0.0.1:8000 in your browser.

#####################################################################################################################

🧭 App Flow
Land on the Login/Register page.

Register as a new user and you'll be redirected to the login page. 
{can consider "Nagendra" and "Pratik0311@" as demo username and password OR you can make it as per your choice}

Login using your credentials.

You’ll land on the Home Page, which will be empty if there are no questions.

Click on "Your Questions" to post your first question.

Once posted, questions and answers will appear on the homepage and your profile.

#####################################################################################################################

📂 Admin Panel Access
Access the admin panel at( Open in incognito mode ):

http://127.0.0.1:8000/admin

Login using the credentials from your createsuperuser step.

🤝 Author
Pratik Agnihotri
Feel free to reach out if you have any questions or suggestions!

