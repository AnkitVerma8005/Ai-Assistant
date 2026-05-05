# AI-Powered Learning Assistant

A comprehensive educational platform designed to streamline learning by converting video content into actionable insights. 
This project was developed as a final-year initiative at the **Goel Institute of Technology & Management (GITM)**.

---

## 🌟 Features

*   **Video Summarization**: Automatically extracts key concepts and generates structured summaries from YouTube URLs.
*   **Dynamic Quiz Generation**: Creates personalized assessments with adjustable difficulty levels (Easy, Medium, Hard) based on specific topics.
*   **Interactive AI Assistant**: Provides a dedicated chat interface for real-time academic support and query resolution.
*   **Learning Dashboard**: Features progress analytics with weekly activity charts and a smart study planner to track educational goals.
*   **Notes Management**: Allows users to save AI-generated summaries as digital notes or export them directly to PDF.

---

## 🛠️ Technical Stack

*   **Backend**: Django (Python).
*   **AI Engine**: Gemini API for natural language processing and content generation
*   **Database**: SQLite (default), with a structured schema for managing users, video modules, and quiz results
*   **Frontend**: Responsive UI featuring a modern dark-mode aesthetic

---

## 📂 Project Structure

```text
Ai-Assistant-main/
├── accounts/      # User registration and authentication
├── assistant/     # Core AI chat assistant logic
├── core/          # Static assets (CSS/JS) and base templates
├── dashboard/     # User progress tracking and analytics
├── quiz/          # Quiz generation and scoring system
├── summarizer/    # Video processing and summary extraction
└── .env           # Environment configuration for API keys
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* A Gemini API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-learning-assistant.git
   cd ai-learning-assistant
   ```

2. **Set up environment variables**:
   Create a `.env` file in the `learning_assistant` directory:
   
```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Install dependencies**:
   
```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the server**:
   
```bash
   python manage.py runserver
   ```

---

## 👥 Credits

This project was developed by the following team members at **GITM**:
*   **Ankit Verma**
*   **Mohd Kaish Shekh**
*   **Rahul Verma**
*   **Sudhanshu Verma**

**Supervised by:** Dr. Nikhat Akhtar (Professor)
```
