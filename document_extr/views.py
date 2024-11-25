from django.shortcuts import render, redirect

from demo.server import upload_and_process_file, process_file
from .models import User
from django.http import JsonResponse, HttpResponse
from .tests import (
    input_image_setup,
    get_gemini_response,
    extract_pdf_text,
    dymanic_path,
    delete_all_files
)
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
import os
import time


# Create your views here.


def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(uname=username)
            print(user, user.password)
            if user is not None and user.password == password:
                request.session["username"] = username

                return redirect("upload")
        except Exception as e:
            print(str(e))
            print("User does not exist")

    return render(request, "login.html")


def uploadFile(request):
    username = request.session.get("username", None)
    print(delete_all_files(dymanic_path("staticfiles")))
    delete_all_files(dymanic_path("static", "images"))
    delete_all_files(dymanic_path("static"))
    processed = False
    if request.method == "POST" and request.FILES["file"]:
        uploaded_file = request.FILES["file"]
        ocr_content = extract_pdf_text(uploaded_file.read())
        print("vinay---filename---", uploaded_file.name)
        start_time = time.time()
        response = upload_and_process_file(uploaded_file)
        elapsed_time = time.time() - start_time
        # print(type(elapsed_time))
        # print(elapsed_time)
        # print(response)
        # print(type(response))
        print("upload done")
        processed = True
        try:
            with open(dymanic_path("document_extr/data/json", f"{uploaded_file.name.split('.')[0]}.json"), "w") as f:
                json.dump(response, f, indent=4)
            print(f"Dictionary saved to {f}")
        except IOError as e:
            print(f"Error saving dictionary to JSON: {e}")
        return render(
            request,
            "index.html",
            {
                "username": username,
                "processed": processed,
                "file_name": uploaded_file.name,
            },
        )
    return render(
        request,
        "index.html",
        {
            "username": username,
        },
    )


def get_fields_data():
    with open(dymanic_path("staticfiles", "genai_extracted.json"), "r") as f:
        # json_bytes = json.loads(f)
        # print("genai_extracted.json", f)
        json_bytes = (
            f.read()
            .replace("\\n", "")
            .replace("JSON", "")
            .replace("```", "")
            .replace("\\", "")
            .replace("json", "")
            .replace("Not found in the document", "")[1:-1]
        )
        print("input data ----------------", json_bytes)
    input_data = dict(json.loads(json_bytes))
    field_values_dict = {}

    def process_dict(data, prefix=""):
        for key, value in data.items():
            if isinstance(value, dict):
                process_dict(value, prefix + key)
            else:
                result_key = f"{prefix}{key}"
                if "Confidence" not in result_key:
                    result_value = [
                        value,
                        int(data.get(f"{key}Confidence", "0") * 100),
                    ]
                    field_values_dict[result_key] = result_value

    process_dict(input_data)
    return field_values_dict


def get_processed_data(file_name):
    try:
        with open(dymanic_path("document_extr/data/json", f"{file_name.split('.')[0]}.json"), 'r') as file:
            input_data = json.load(file)
            field_values_dict = {}
            print(input_data)
            for key, value in input_data.items():
                if "_confidence" not in key:
                    field_values_dict[key.replace("_", " ")] = [value, 100 * float(input_data[f"{key}_confidence"])]
        return field_values_dict
    except IOError as e:
        print(f"Error loading dictionary from JSON: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def keyingscreen_view(request):
    file_name = request.GET.get("file_name")
    field_dict = get_processed_data(file_name)
    image_urls = os.listdir(dymanic_path("static", "images"))
    file_name = request.GET.get("file_name")
    return render(
        request,
        "keyingscreen.html",
        {
            "field_values_dict": field_dict,
            "image_urls": image_urls,
            "file_name": file_name,
        },
    )


# def keyingscreen_view(request):
#     file_name = request.GET.get("file_name")
#     print(file_name)
#
#     field_dict = process_file(file_name)
#     print(field_dict)
#     # print(type(field_dict))
#     # dictionary = json.loads(field_dict)
#     # field_dict = get_fields_data()
#     # print(field_dict)
#     # image_urls = os.listdir(dymanic_path("static", "images"))
#     # print("image_urls", image_urls)
#     # file_name = request.GET.get("file_name")
#     # print("image_urls", file_name)
#     return render(
#         request,
#         "keyingscreen.html",
#         {
#             "field_values_dict": field_dict,
#             "image_urls": "image_urls",
#             "file_name": file_name,
#         },
#     )
#

@csrf_exempt
def save_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            filename = (
                    data.get("filename", "default_filename.json").split(".")[0] + ".json"
            )
            form_data = data.get("formData", {})

            # Save the data to a JSON file
            print("vinay----------", filename)
            with open(dymanic_path("static", filename), "w") as json_file:
                json.dump(form_data, json_file)

            return JsonResponse({"status": "success"})

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "success"})

    return JsonResponse({"status": "success"})


def download_view(request):
    file_name = request.GET.get("file_name").split(".")[0] + ".json"
    path = dymanic_path("static", file_name)

    if os.path.exists(path) and os.path.isfile(path):
        with open(path, "rb") as json_file:
            json_data = json_file.read()
            response = HttpResponse(json_data, content_type="application/json")
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(path)}"'
            )
            return response
    else:
        return HttpResponse("File not found", status=404)
