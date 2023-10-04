import tkinter as tk
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry, Floodgauge, Meter
from tkinter import messagebox



class App:
    def __init__(self):
        self.window = None
        self.table_frame = None
        self.label_1 = None
        self.label_2 = None
        self.button_1 = None
        self.button_2 = None
        self.calendar = None
        self.calendar_2 = None
        self.birth_date = None
        self.rest_date = None
        self.amount_of_rest_days = 0
        self.dates_of_due = []
        self.data_entries = []
        self.zipped_table = None
        self.sum_of_value_dues = 1
        self.average_dues = 1
        self.base = 0
        self.sickness_allowance = 0
        self.maternity_allowance =   0
        self.label_3 = None
        self.label_4 = None

    def determine_window(self):
        self.window = tk.Tk()
        self.window.title("sprawdź jak się przygotować na rok z bobasem")
        return self.window

    def determine_table_frame(self):
        self.table_frame = tk.Frame(self.window)
        self.table_frame.grid(row=5, column=0, padx=5, pady=5)
        return self.table_frame

    def first_label(self):
        self.label_1 = tk.Label(self.window, text="wpisz planowaną datę narodzin bobasa")
        self.label_1.grid(row=0, column=0, padx=5, pady=5)
        return self.label_1

    def second_label(self):
        self.label_2 = tk.Label(self.window, text="jak myślisz kiedy bobas w brzuchu nie da już pracować?")
        self.label_2.grid(row=2, column=0, padx=5, pady=5)
        return self.label_2

    def first_calendar(self):
        self.calendar = DateEntry(self.window)
        self.calendar.grid(row=1, column=0, padx=5, pady=5)
        return self.calendar

    def second_calendar(self):
        self.calendar_2 = DateEntry(self.window)
        self.calendar_2.grid(row=3, column=0, padx=5, pady=5)
        return self.calendar_2

    def determine_rest_date(self):
        rest_date_str = self.calendar_2.entry.get()
        self.rest_date = datetime.strptime(rest_date_str, '%d.%m.%Y').date()
        return self.rest_date

    def determine_birthday(self):
        birth_date_str = self.calendar.entry.get()
        self.birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y').date()
        return self.birth_date


    def first_button(self):
        self.button_1 = tk.Button(self.window, text="ile wrzucasz do systemu?", command=self.make_table)
        self.button_1.grid(row=4, column=0, padx=5, pady=5)
        return self.button_1

    def second_button(self):
        self.button_2 = tk.Button(self.window, text="oblicz ile dostaniesz", command=self.third_label)
        self.button_2.grid(row=17, column=0, padx=5, pady=5)
        return self.button_2


    def make_table(self):
        self.dates_of_due = []
        first_date = self.determine_rest_date()
        for i in range(12):
            self.dates_of_due.append(first_date)
            date_label = tk.Label(self.table_frame, text=first_date.strftime('20.%m.%Y'))
            date_label.grid(row=i, column=0, padx=5, pady=5)
            first_date += relativedelta(months=-1)
        self.data_entries = []
        for i in range(12):
            data_entry = tk.Entry(self.table_frame)
            data_entry.grid(row=i, column=1, padx=5, pady=5)
            self.data_entries.append(data_entry)
        print(self.data_entries)

        return self.dates_of_due, self.data_entries

    def validate_float(self, input_value):


        try:
            input_value = float(input_value)
            return True
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawną wartość liczbową, nie większą niż 5910.18zł")
            return False

    def calculate_amount_of_rest_days(self):
        self.amount_of_rest_days = int((self.birth_date-self.rest_date).days)
        return self.amount_of_rest_days

    def calculate_sum_of_value_dues(self):
        border_date = datetime.strptime('01.02.2023', '%d.%m.%Y').replace(hour=0, minute=0, second=0)
        border_value = 1418.48
        border_value_2022 = 1211.28
        self.sum_of_value_dues = 0
        for date_of_paying, entry in zip(self.dates_of_due, self.data_entries):
            entry_value = entry.get()
            entry_value = entry_value.replace(",", ".")
            entry_value = entry_value.replace(" ","")
            if entry_value == "":
                entry_value = 0
            if float(entry_value) >= 5910.18:
                messagebox.showerror("Błąd", "jednorazowa wpłata nie może być większa niż 5910.18zł")
            if entry_value and self.validate_float(entry_value):
                entry_value = float(entry_value)
                date_of_paying = datetime.combine(date_of_paying, time())  # Konwertuj date_of_paying na datetime
                if date_of_paying >= border_date and entry_value >= border_value:
                    self.sum_of_value_dues += entry_value
                elif date_of_paying < border_date and entry_value >= border_value_2022:
                    self.sum_of_value_dues += entry_value
        return self.sum_of_value_dues

    def calculate_average_dues(self):
        self.average_dues = self.sum_of_value_dues/12

    def calculate_base(self):
        self.base = 0.8629 * round(self.average_dues / 0.3409)
        return self.base

    def calculate_sickness_allowance(self):
        self.sickness_allowance = round((self.base/30) * self.amount_of_rest_days, 2)
        return self.sickness_allowance

    def calculate_maternity_allowance(self):
        if self.average_dues != 0:
            self.maternity_allowance = round(0.88 * self.base, 2)
        else:
            self.maternity_allowance = 1000
        return self.maternity_allowance

    def third_label(self):
        self.determine_rest_date()
        self.determine_birthday()
        self.calculate_sum_of_value_dues()
        self.calculate_average_dues()
        self.calculate_base()
        self.calculate_sickness_allowance()
        self.calculate_maternity_allowance()
        self.amount_of_rest_days = self.calculate_amount_of_rest_days()

        # Sprawdzenie, czy etykieta Label3 została już utworzona
        if self.label_3 is None:
            self.label_3 = tk.Label(self.window, text="")
            self.label_3.grid(row=18, column=0, padx=5, pady=5)

        # Aktualizacja treści Label3
        self.label_3.config(text=f"będziesz na L4 przez {self.amount_of_rest_days} dni\n"
                                 f"i otrzymasz przez cały ten czas {self.calculate_sickness_allowance()} zł\n\n"
                                 f"będziesz na urlopie macierzyńskim od dnia {self.birth_date}")

        if self.maternity_allowance == 1000:
            text = 'otrzymasz co miesiąc netto 1000 zł'
        else:
            text = f'''jeżeli wybierzesz opcję równych wypłat przez cały rok czyli 81,5% podstawy,
                        to otrzymasz co miesiąc netto {round(0.815 * self.maternity_allowance, 2)} zł,
                        jeżeli wybierzesz opcję zmiennych wypłat czyli 100% podstawy przez 20 tygodni i 70% przez 32 tygodnie,
                        to otrzymasz miesięcznie netto odpowiednio {self.maternity_allowance} zł lub {round(0.7 * self.maternity_allowance, 2)} zł'''

        # Sprawdzenie, czy etykieta Label4 została już utworzona
        if self.label_4 is None:
            self.label_4 = tk.Label(self.window, text="")
            self.label_4.grid(row=19, column=0, padx=5, pady=5)

        # Aktualizacja treści Label4
        self.label_4.config(text=text)




def main():

    app = App()
    app.determine_window()
    app.first_label()
    app.first_calendar()
    app.second_calendar()
    app.second_label()
    app.determine_rest_date()
    app.first_button()
    app.determine_table_frame()
    app.determine_birthday()
    app.determine_table_frame()
    app.second_button()
    app.calculate_sum_of_value_dues()
    app.calculate_average_dues()
    app.calculate_base()
    app.calculate_sickness_allowance()
    app.calculate_maternity_allowance()
    app.window.mainloop()

if __name__ == "__main__":
    main()










