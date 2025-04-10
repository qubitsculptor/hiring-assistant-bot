questions = [
    "What's your full name?",
    "What's your email address?",
    "Could you share your phone number?",
    "How many years of experience do you have?",
    "What position(s) are you interested in?",
    "What's your current location?",
    "Tell me about your tech stack — programming languages, frameworks, tools, etc.",
]

field_keys = ["full_name", "email", "phone", "years_of_experience", "desired_position", "location", "tech_stack"]

exit_keywords = ["exit", "quit", "bye", "goodbye", "stop", "thank you", "thanks"]

def build_prompt(tech_stack):
    return f"""
    Based strictly on the tech stack below, generate 5 concise technical interview questions.
    DO NOT include any explanations, intros, comments, difficulty levels, or anything else.
    Only output the questions numbered from 1 to 5.

    Tech stack: {tech_stack}
    """
