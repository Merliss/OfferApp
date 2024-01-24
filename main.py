import tkinter as tk
from tkinter import ttk
import requests
import json
from bs4 import BeautifulSoup
from tkcalendar import DateEntry
import pdfkit
from datetime import datetime
import os
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import pathname2url

logo_path = "logo.png"
logo_url = urljoin('file:', pathname2url(str(logo_path)))


config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Assistant")
        self.create_widgets()
        self.api_response = ""

    def create_widgets(self):
        self.length_label = ttk.Label(self, text="Długość opisu:")
        self.length_combo = ttk.Combobox(self, values=[50, 100, 200, 400])
        self.submit_button = ttk.Button(self, text="Wygeneruj opis na podstawie\nwprowadzonych danych", command=self.submit_prompt)
        self.response_text = tk.Text(self)

        self.job_title_label = ttk.Label(self, text="Nazwa stanowiska:")
        self.job_title_entry = ttk.Entry(self)
        self.company_name_label = ttk.Label(self, text="Nazwa firmy:")
        self.company_name_entry = ttk.Entry(self)
        self.location_label = ttk.Label(self, text="Lokalizajca:")
        self.location_entry = ttk.Entry(self)
        self.salary_label = ttk.Label(self, text="Wynagrodzenie:")
        self.salary_entry = ttk.Entry(self)
        self.deadline_label = ttk.Label(self, text="Złóż aplikacje do:")
        self.deadline_entry = DateEntry(self, date_pattern='dd/mm/yyyy')
        self.submit_html_button = ttk.Button(self, text="Zapisz zmiany", command=self.submit_changes)
        self.experience_level_label = ttk.Label(self, text="Poziom doświadczenia:")
        self.experience_level_combo = ttk.Combobox(self, values=["Junior", "Mid", "Senior"])
        self.location_label = ttk.Label(self, text="Lokalizacja:")
        self.location_entry = ttk.Entry(self)
        self.work_type_label = ttk.Label(self, text="Typ pracy:")
        self.work_type_combo = ttk.Combobox(self, values=["Stacjonarna", "Hybrydowa", "Zdalna"])
        self.department_label = ttk.Label(self, text="Departament:")
        self.department_combo = ttk.Combobox(self, values=["Marketing", "IT", "Finanse", "Produkcja", "Inżynieria", "Logistyka", "HR", "Kadry menedżerskie"])
        self.cv_style_label = ttk.Label(self, text="Styl oferty:")
        self.cv_style_entry = ttk.Combobox(self, values=["Luźny", "Formalny", "Standardowy", "Barwny", "oferta w formie historii", "Wierszyk"])
        self.requirements_label = ttk.Label(self, text="Wymagania:")
        self.requirements_entry = ttk.Entry(self)

        self.length_label.grid(row=1, column=0)
        self.length_combo.grid(row=1, column=1)
        self.submit_button.grid(row=2, column=0, columnspan=2)
        self.response_text.grid(row=3, column=0, columnspan=2)

        self.job_title_label.grid(row=4, column=0)
        self.job_title_entry.grid(row=4, column=1)
        self.company_name_label.grid(row=5, column=0)
        self.company_name_entry.grid(row=5, column=1)
        self.location_label.grid(row=6, column=0)
        self.location_entry.grid(row=6, column=1)
        self.salary_label.grid(row=7, column=0)
        self.salary_entry.grid(row=7, column=1)
        self.deadline_label.grid(row=8, column=0)
        self.deadline_entry.grid(row=8, column=1)
        self.department_label.grid(row=9, column=0)
        self.department_combo.grid(row=9, column=1)
        self.experience_level_label.grid(row=10, column=0)
        self.experience_level_combo.grid(row=10, column=1)
        self.location_label.grid(row=11, column=0)
        self.location_entry.grid(row=11, column=1)
        self.work_type_label.grid(row=12, column=0)
        self.work_type_combo.grid(row=12, column=1)
        self.requirements_label.grid(row=13, column=0)
        self.requirements_entry.grid(row=13, column=1)
        self.cv_style_label.grid(row=14, column=0)
        self.cv_style_entry.grid(row=14, column=1)
        self.submit_html_button.grid(row=15, column=0, columnspan=2)

    def submit_prompt(self):
        length = self.length_combo.get()
        job_title = self.job_title_entry.get()
        company_name = self.company_name_entry.get()
        location = self.location_entry.get()
        salary = self.salary_entry.get()
        deadline = self.deadline_entry.get_date().isoformat()

        experience_level = self.experience_level_combo.get()
        location = self.location_entry.get()
        work_type = self.work_type_combo.get()
        department = self.department_combo.get()
        requirements = self.requirements_entry.get().split(';')
        if not length or not job_title or not company_name or not location or not salary or not deadline or not experience_level or not location or not work_type or not department or not requirements:
            self.response_text.delete('1.0', tk.END)
            self.response_text.insert(tk.END, "Uzupełnij wszystkie pola.")
            return
        length = int(length)
        prompt = f"Dodaj opis oferty pracy dla stanowiska z perpsektywy pracodawcy: {self.job_title_entry.get()}, które ma w wymaganich {self.requirements_entry.get()}. Zastosuj styl oferty:{self.cv_style_entry.get()} Wygeneruj maksymalnie {length} znaków."
        response = self.get_response_from_api(prompt, length)
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert(tk.END, response)

    # Save the response for later use
        self.api_response = response

    def get_response_from_api(self, prompt, length):
        url = "https://api.openai.com/v1/engines/gpt-3.5-turbo-instruct/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer API-KEY"
        }
        data = {
            "prompt": prompt,
            "max_tokens": length
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_json = response.json()
            return response_json["choices"][0]["text"]
        else:
            return f"Error: {response.status_code}, {response.text}"
        
    def submit_changes(self):
        job_title = self.job_title_entry.get()
        company_name = self.company_name_entry.get()
        location = self.location_entry.get()
        salary = self.salary_entry.get()
        deadline = self.deadline_entry.get_date().isoformat()

        experience_level = self.experience_level_combo.get()
        location = self.location_entry.get()
        work_type = self.work_type_combo.get()
        department = self.department_combo.get()
        requirements = self.requirements_entry.get().split(';')

        self.modify_html(job_title, company_name, location, salary, deadline, experience_level, work_type, department, requirements, self.api_response)

    def modify_html(self, job_title, company_name, location, salary, deadline, experience_level, work_type, department, requirements, description):
        with open("job_offer2.html", "r") as file:
            soup = BeautifulSoup(file, "html.parser")

        soup.find("h1", class_="job-title").string = job_title
        soup.find("h1", class_="company-name").string = company_name

        # Update the job description with the API response
        soup.find("p", class_="job-description").string = description
        soup.find("img", class_="company-logo")["src"] = logo_path

        job_details = soup.find("div", class_="job-details").find_all("p")
        job_details[0].string = f"Departament: {department}"
        job_details[1].string = f"Widełki płacowe: {salary} rocznie"
        job_details[2].string = f"Poziom doświadczenia: {experience_level}"
        job_details[3].string = f"Lokalizacja: {location}"
        job_details[4].string = f"Typ pracy: {work_type}"
        job_details[5].string = f"Złóż aplikacje do: {deadline}"

        requirements_ul = soup.find("ul", class_="job-requirements")
        requirements_ul.clear()
        for requirement in requirements:
            li = soup.new_tag("li")
            li.string = requirement
            requirements_ul.append(li)

        with open("job_offer2.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
        
        pdfkit.from_file('job_offer2.html', f'{job_title}_{experience_level}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf',configuration=config, options={'encoding': "UTF-8",'enable-local-file-access': None})

if __name__ == "__main__":
    app = Application()
    app.mainloop()