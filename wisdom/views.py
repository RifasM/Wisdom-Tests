import csv
import os
from io import StringIO

from django.contrib import messages
from django.shortcuts import render
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from Wisdom_Tests.settings import MEDIA_ROOT


def home(request):
    if request.method == "POST":
        email = request.POST["email"]
        service_type = request.POST["service"]

        csv_file = request.FILES["fileCSV"]

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "THIS IS NOT A CSV FILE")

        data_set = csv_file.read().decode("UTF-8")
        io_string = StringIO(data_set)
        next(io_string)

        student = {}

        for row in csv.reader(io_string, delimiter=",", quotechar="|"):

            if row[2] not in student:
                student[row[2]] = {
                    "student_num": row[0],
                    "student_picture": os.path.join(MEDIA_ROOT, "Pics/{}.jpg".format(row[0])),
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
                    ],
                    "attempts": 1 if str(row[15]).lower() == "attempted" else 0,
                    "skips": 1 if str(row[15]).lower() == "unattempted" else 0,
                    "performance_correct": 1 if str(row[18]).lower() == "correct" else 0,
                    "performance_incorrect": 1 if str(row[18]).lower() == "incorrect" else 0,
                    "performance_unattempted": 1 if str(row[18]).lower() == "unattempted" else 0,
                    "total_time": int(row[12]),
                    "total_score": int(row[19]),
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
                student[row[2]]["attempts"] += 1 if str(row[15]).lower() == "attempted" else 0
                student[row[2]]["skips"] += 1 if str(row[15]).lower() == "unattempted" else 0
                student[row[2]]["performance_correct"] += 1 if str(row[18]).lower() == "correct" else 0
                student[row[2]]["performance_incorrect"] += 1 if str(row[18]).lower() == "incorrect" else 0
                student[row[2]]["performance_unattempted"] += 1 if str(row[18]).lower() == "unattempted" else 0
                student[row[2]]["total_time"] += int(row[12])
                student[row[2]]["total_score"] += int(row[19])

        pdf_dir = os.path.join(MEDIA_ROOT, "temp")

        for person in student:
            print(person)
            # html_template = get_template("report.html"
            html = render_to_string("report.html", student[person])
            # pdf_file = HTML(str(html_template)).write_pdf()

            html_path = os.path.join(pdf_dir, student[person]["student_num"] + "_demo.html")
            pdf_path = os.path.join(pdf_dir, student[person]["student_num"] + "_demo.pdf")

            with open(html_path, "wb") as f:

                f.write(str(html).encode("utf-8"))
                print('http://' + request.get_host() +
                      "/media/temp/" +
                      student[person]["student_num"] +
                      "_demo.html")

                with open(pdf_path, "wb") as p:
                    pisa_status = pisa.CreatePDF(
                        str(html).encode("utf-8"),
                        dest=p)

                if not os.path.isdir(pdf_dir):
                    os.mkdir(pdf_dir)

                """pdfkit.from_file(
                    html_path, pdf_path)"""

                # os.system("wkhtmltopdf --javascript-delay 1000 {} {}".format(html_path, pdf_path))
                # os.remove(html_path)

        """for person in student:
            # template = get_template("report.html")
            html = render_to_string("report.html", student[person])

            if not os.path.isdir(pdf_dir):
                os.mkdir(pdf_dir)

            pdfkit.from_string(
                html, os.path.join(os.path.join(pdf_dir, student[person]["student_num"] + "_demo.pdf")))

        zip_path = os.path.join(MEDIA_ROOT, "report.zip")

        zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

        for path in os.listdir(pdf_dir):
            fdir, fname = os.path.split(path)
            zip_path = os.path.join(pdf_dir, fname)

            zf.write(zip_path)

        zf.close()

        with open(zip_path, "rb") as f:
            resp = HttpResponse(f, "application/x-zip-compressed")

            resp['Content-Disposition'] = 'attachment; filename=report.zip'

        return resp"""

        return render(request, "report.html", student.get("32030938"))
    return render(request, "index.html")


def report(request):
    return render(request, "report.html")
