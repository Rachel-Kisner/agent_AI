import platform
import os
import json
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
from myproject.agent import get_system_prompt

load_dotenv()
client = OpenAI()

def detect_shell():
    """זיהוי סוג ה-Shell שבו הפרויקט רץ."""

    os_name = platform.system()

    if os_name == "Windows":
        if os.environ.get("PSModulePath"):
            return "powershell"
        return "cmd"


    shell_path = os.environ.get("SHELL")

    if shell_path:
        return os.path.basename(shell_path).lower()

    return "unknown"

def generate_command(user_request):

    # זיהוי מערכת ההפעלה
    os_name = platform.system()

    # זיהוי ה-Shell
    shell_name = detect_shell()

    # יצירת ה-System Prompt
    system_prompt = get_system_prompt(os_name, shell_name)

    # שליחת הבקשה ל-OpenAI
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_request}
        ],
        response_format={"type": "json_object"}
    )
    # קבלת התשובה
    result = response.choices[0].message.content

# המרת מחרוזת JSON לאובייקט Python
    data = json.loads(result)

# חילוץ הפקודה בלבד
    command = data["command"]

    return command


demo = gr.Interface(
    fn=generate_command,
    inputs=gr.Textbox(
        label="מה תרצה לבצע?",
        placeholder="לדוגמה: הצג את כל הקבצים בתיקייה הנוכחית"
    ),
    outputs=gr.Code(label="Terminal Command"),
    title="AI Terminal Command Agent",
    description="הכניסו בקשה בשפה טבעית וקבלו פקודת טרמינל מתאימה."
)


# הפעלת הממשק
def main():
    demo.launch()


if __name__ == "__main__":
    main()
    
    
