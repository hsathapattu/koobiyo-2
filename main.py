from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define the user profile schema
class UserProfile(BaseModel):
    name: str
    age: int
    school_interest: bool = None
    career_dream: str = None
    friendships: bool = None
    struggles: str = None
    career_path: str = None
    relationship_status: bool = None
    future_goals: str = None
    life_achievement: str = None
    work_life_balance: bool = None
    financial_state: bool = None
    legacy_thoughts: str = None
    retirement_plans: bool = None
    health_and_wellness: bool = None
    spirituality: bool = None
    peace_of_mind: bool = None
    life_reflection: str = None

# Route to serve the frontend HTML page
@app.get("/", response_class=HTMLResponse)
async def read_index():
    return open("index.html", "r").read()

# Route to handle the prediction generation
@app.post("/generate_prediction/")
async def generate_prediction(user_profile: UserProfile):
    # Prepare the user data for prediction
    user_data_summary = (
        f"Name: {user_profile.name}, Age: {user_profile.age}\n"
        f"School Interest: {'Yes' if user_profile.school_interest else 'No'}, "
        f"Career Path: {user_profile.career_path or 'N/A'}, "
        f"Relationship Status: {'Yes' if user_profile.relationship_status else 'No'}, "
        f"Struggles Faced: {user_profile.struggles or 'N/A'}, "
        f"Life Achievement: {user_profile.life_achievement or 'N/A'}, "
        f"Legacy Thoughts: {user_profile.legacy_thoughts or 'N/A'}, "
        f"Health and Wellness: {'Yes' if user_profile.health_and_wellness else 'No'}, "
        f"Spirituality: {'Yes' if user_profile.spirituality else 'No'}\n"
        "Based on this information, provide a deeply personalized prediction, including emotional, career, and health insights, "
        "along with powerful guidance for the next life stages. The prediction should feel incredibly real and impactful."
    )

    # Call the Groq API for prediction
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",  # You can adjust this model if needed
            messages=[{
                "role": "system", "content": "You are a wise AI that offers transformative, life-changing future predictions based on deep personal data."
            }, {
                "role": "user", "content": user_data_summary
            }]
        )
        prediction = chat_completion.choices[0].message.content
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}

