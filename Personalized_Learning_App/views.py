import os
import json
import uuid
from dotenv import load_dotenv
import google.generativeai as genai
from xhtml2pdf import pisa
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.utils.timezone import now
from django.db.models import Count
from .models import Test, TestSubmission, ContactMessage
from .forms import RegistrationForm


# Configure GenAI API
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key) 
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
def current_course(request):
    return render(request, 'current_course.html')

@login_required
def python_course(request):
    return render(request, 'python_course.html')

@login_required
def java_course(request):
    return render(request, 'java_course.html')

@login_required
def cpp_course(request):
    return render(request, 'cpp_course.html')

@login_required
def os_course(request):
    return render(request, 'os_course.html')

@login_required
def dbms_course(request):
    return render(request, 'dbms_course.html')

@login_required
def networking_course(request):
    return render(request, 'networking_course.html')

@login_required
def devops_course(request):
    return render(request, 'devops_course.html')

def ai_analysis(request):
    return render(request, 'ai_analysis.html')

def quiz(request):
    return render(request, 'quiz.html')

def resourse_recommendations(request):
    return render(request, 'resourse_recommendations.html')

def progress(request):
    return render(request, 'progress.html')

def todo_list(request):
    return render(request, 'todo.html')

def qr_gen(request):
    return render(request, 'qr_gen.html')

@login_required
def your_achievements(request):
    return render(request, 'your_achievements.html')

@login_required
def view_subjects(request):
    return render(request, 'view_subjects.html')


@login_required
def members(request):
    return render(request, 'members.html')


@login_required
def analytics(request):
    return render(request, 'analytics.html')

@login_required
def classes(request):
    return render(request, 'classes.html')

@login_required
def admin_dash(request):
    if not request.user.is_staff:
        return redirect('login_view')

    today = now().date()
    todays_active_users = User.objects.filter(last_login__date=today).count()
    total_tests_created = Test.objects.count()
    total_tests_submitted = TestSubmission.objects.count()
    new_feedback_count = ContactMessage.objects.filter(is_read=False).count()

    context = {
        'total_users': User.objects.count(),
        'active_sessions': 150,  
        'total_courses': 200,
        'pending_requests': 20,
        'todays_active_users': todays_active_users,
        'total_tests_created': total_tests_created,
        'total_tests_submitted': total_tests_submitted,
        'new_feedback_count': new_feedback_count, 
    }

    return render(request, 'admin_dash.html', context)


#Contact us form
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Your message has been submitted successfully.")
        else:
            messages.error(request, "Please fill in all the fields.")

    return render(request, 'contact.html')


#See user feedbacks
def view_feedbacks(request):
    if not request.user.is_staff:
        return redirect('login_view')

    deleted = False

    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')
        if delete_id:
            ContactMessage.objects.filter(id=delete_id).delete()
            deleted = True 

    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    messages = ContactMessage.objects.all().order_by('-timestamp')

    return render(request, 'feedbacks.html', {
        'messages': messages,
        'deleted': deleted
    })


def register(request):
    attempted = False
    if request.method == 'POST':
        attempted = True
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                User.objects.create_user(username=username, email=email, password=password)
                return redirect('login_view')
            except Exception as e:
                messages.error(request, "Something went wrong while creating your account.")
                return redirect('register')
        else:
            errors = form.non_field_errors()
            if errors:
                messages.error(request, errors[0])
            else:
                messages.error(request, "Please check your input and try again.")
            return redirect('register')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'attempted': attempted})


def login_view(request):
    attempted = False
    if request.method == "POST":
        attempted = True
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html', {'attempted': attempted})

def admin_login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dash')
        else:
            messages.error(request, "Invalid admin credentials.")

    return render(request, 'admin_login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

def admin_logout(request):
    logout(request)
    return redirect('index')

def generate_mcq(topic, num_questions=10):
    prompt = f"""
    Generate {num_questions} multiple-choice questions (MCQs) for {topic} exam preparation.
    Each question should belong to a specific subtopic (e.g., Data Types, Exception Handling).
    Format each question as follows:

    Question: <MCQ Question> <marks>
    Correct Answer: <Correct Option Letter (e.g. a)>
    (a) <Option 1>
    (b) <Option 2>
    (c) <Option 3>
    (d) <Option 4>
    Subtopic: <Subtopic Name (e.g., Data Types)>

    Ensure each question is followed immediately by its correct answer, marks, four options, and the subtopic in a clear and structured manner.
    """
    response = model.generate_content(prompt)
    # Split response into individual questions (using double newline as separator)
    mcq_texts = response.text.strip().split("\n\n")
    formatted_mcqs = []

    for mcq in mcq_texts:
        lines = [line.strip() for line in mcq.strip().split("\n") if line.strip()]
        if len(lines) >= 7:  # Expecting at least 7 lines: 4 options, correct answer, question, and subtopic
            question_line = lines[0].replace("Question: ", "").strip()
            parts = question_line.rsplit(" ", 1)
            if len(parts) == 2:
                question_text, marks_str = parts
                try:
                    marks = float(marks_str)
                except ValueError:
                    marks = 1
            else:
                question_text = question_line
                marks = 1

            correct_answer = lines[1].replace("Correct Answer: ", "").strip()
            options = lines[2:6]
            subtopic = lines[6].replace("Subtopic: ", "").strip()  # Extract the subtopic
            
            formatted_mcqs.append({
                'question': question_text,
                'marks': marks,
                'correct_answer': correct_answer,
                'options': options,
                'topic': topic,  # Store the main topic
                'subtopic': subtopic  # Store the subtopic for each question
            })
    return formatted_mcqs


def mcq_test(request):
    if request.method == "POST":
        topic = request.POST.get("topic")
        mcqs = generate_mcq(topic, 10)

        # Save the test entry to the database
        if request.user.is_authenticated:
            Test.objects.create(user=request.user, topic=topic)

        request.session['mcqs'], request.session['topic'] = mcqs, topic
        return render(request, "mcq_test.html", {"mcqs": mcqs, "topic": topic})

    return render(request, "mcq_test.html")


def fetch_study_material(topic):
    prompt = f"""
    The user has incorrect answers in {topic}. Provide:
    1. Brief explanation
    2. Common mistakes
    3. Example code
    4. Learning resources
    5. YouTube tutorial link
    6. Google search URL
    """
    return model.generate_content(prompt).text.strip()


def submit_test(request):
    if request.method == "POST":
        mcqs = request.session.get("mcqs", [])
        test_submission = []

        website_links = {
            'python': {
                'w3schools': 'https://www.w3schools.com/python/',
                'geeksforgeeks': 'https://www.geeksforgeeks.org/python-programming-language-tutorial/'
            },
            'java': {
                'w3schools': 'https://www.w3schools.com/java/java_intro.asp',
                'geeksforgeeks': 'https://www.geeksforgeeks.org/java/?ref=ghm'
            }
        }

        # Get the topic from the first MCQ (assuming all MCQs belong to the same topic)
        topic = mcqs[0].get('topic', 'unknown').lower() if mcqs else 'unknown'
        links = website_links.get(topic, {})

        for idx, mcq in enumerate(mcqs, start=1):
            user_answer = request.POST.get(f"q{idx}", "")
            test = Test.objects.filter(user=request.user, topic=topic).order_by('-created_at').first()

            test_submission.append({
                "question": mcq["question"],
                "options": mcq["options"],
                "correct_answer": mcq["correct_answer"],
                "user_answer": user_answer,
                "marks": mcq["marks"],
                "topic": topic
            })

        analysis_response = model.generate_content(f"Analyze: {json.dumps(test_submission, indent=2)}")
        formatted_analysis = analysis_response.text.strip().replace("\n", "<br>")

        # Prepare dummy placeholders for now if needed
        study_material = {topic: fetch_study_material(topic)}
        youtube_links = [{'topic': topic, 'url': f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}"}]
        google_links = [{'topic': topic, 'url': f"https://www.google.com/search?q={topic.replace(' ', '+')}"}]

        request.session["test_report"] = {
            "analysis": formatted_analysis,
            "study_material": study_material,
            "youtube_links": youtube_links,
            "google_links": google_links,
        }

        if test:
            TestSubmission.objects.create(test=test, user=request.user)

        return render(request, "test_result.html", {
            "analysis": formatted_analysis,
            "study_material": study_material,
            "youtube_links": youtube_links,
            "google_links": google_links,
            "website_links": links,
            "topic": topic,
        })

    return render(request, "test_result.html", {
        "analysis": "No analysis available yet.",
        "study_material": {},
        "youtube_links": [],
        "google_links": [],
        "website_links": {},
        "topic": "unknown"
    })


#PDF generation
def generate_pdf(request):
    # Retrieve the test report from session
    test_report = request.session.get("test_report", {})

    # Ensure the test report contains necessary keys and data
    if not test_report:
        return HttpResponse("No report data available.", status=400)

    # Fetch the template for PDF generation
    template_path = "test_report_pdf.html"
    template = get_template(template_path)
    html = template.render(test_report)  # Render HTML with data

    # Generate PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Test_Report.pdf"'

    # Convert HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response