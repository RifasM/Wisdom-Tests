import csv
from io import StringIO

from django.contrib import messages
from django.shortcuts import render


def home(request):
    if request.method == "POST":
        q_count = request.POST["q_count"]
        email = request.POST["email"]
        service_type = request.POST["service"]

        csv_file = request.FILES["fileCSV"]

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "THIS IS NOT A CSV FILE")

        data_set = csv_file.read().decode("UTF-8")
        io_string = StringIO(data_set)
        next(io_string)

        cols = ['Student No ', 'Name of Candidate',
                'Registration', 'Grade ', 'Gender',
                'Name of school ', 'Date of Birth ',
                'City of Residence', 'Date and time of test',
                'Country of Residence', 'Extra time assistance',
                'Question No.', 'Time Spent on question (sec)',
                'Score if correct', 'Score if incorrect',
                'Attempt status ', 'What you marked',
                'Correct Answer',
                'Outcome (Correct/Incorrect/Not Attempted)',
                'Your score']

        student = {}

        for row in csv.reader(io_string, delimiter=",", quotechar="|"):

            if row[2] not in student:
                student[row[2]] = {
                    "student_num": row[0],
                    "name": row[1],
                    "registration": row[2],
                    "grade": row[3],
                    "gender": row[4],
                    "school": row[5],
                    "dob": row[6],
                    "city": row[7],
                    "test_dt": row[8],
                    "country": row[9],
                    "assistance": row[10],
                    "questions": [
                        {
                            "qno": row[11],
                            "time": row[12],
                            "correct_score": row[13],
                            "incorrect_score": row[14],
                            "status": row[15],
                            "answer_marked": row[16],
                            "answer_correct": row[17],
                            "outcome": row[18],
                            "score": row[19]
                        }
                    ]
                }
            else:
                student[row[2]].get("questions").append({
                    "qno": row[11],
                    "time": row[12],
                    "correct_score": row[13],
                    "incorrect_score": row[14],
                    "status": row[15],
                    "answer_marked": row[16],
                    "answer_correct": row[17],
                    "outcome": row[18],
                    "score": row[19]
                })

        print(student)

    return render(request, "index.html")


def report(request):
    return render(request, "report.html")
