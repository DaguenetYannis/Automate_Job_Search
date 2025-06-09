import yagmail
import datetime

# Your Gmail and App Password (store securely!)
yagmail.register('yannisdaguenet@gmail.com', 'qkucbouzqrnhwrni')

sender = "yannisdaguenet@gmail.com"
receiver = "yannisdaguenet@gmail.com"
subject = "🎯 Job Hunt Reminder"

# Get today
today = datetime.datetime.now().strftime("%A")

tasks = {
    "Monday": "🔍 Add job offers to your CSV or Google Sheet.",
    "Tuesday": "📇 Find recruiter or employee contacts for listed companies.",
    "Wednesday": "✍️ Write personalized pitches or messages.",
    "Thursday": "📞 Reach out and call / connect with contacts.",
    "Friday": "📤 Finalize and send job applications.",
    "Saturday": "🧘‍♂️ Rest or reflect on the week.",
    "Sunday": "🗂️ Plan the next week's job strategy."
}

body = tasks.get(today, "✅ No task today — take a breather or review your goals.")

# Utilisation du mot de passe stocké via yagmail.register
yag = yagmail.SMTP("yannisdaguenet@gmail.com")
yag.send(to=receiver, subject=subject, contents=body)

print(f"✅ Reminder sent for {today}.")