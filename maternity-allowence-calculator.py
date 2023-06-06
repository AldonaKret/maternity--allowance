import tkinter as tk
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry, Floodgauge, Meter
from tkinter import messagebox
import re


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
        self.sickness_allowence = 0
        self.maternity_allowence = 0

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

     # def determine_birthday(self):
    #     self.birth_date = self.calendar.entry.get()
    #     self.birth_date = datetime.strptime(self.birth_date, '%d.%m.%Y').date()
    #     return self.birth_date
    def determine_rest_date(self):
        rest_date_str = self.calendar_2.entry.get()  # Pobierz datę odpoczynku
        self.rest_date = datetime.strptime(rest_date_str, '%d.%m.%Y').date()
        return self.rest_date

    def determine_birthday(self):
        birth_date_str = self.calendar.entry.get()  # Pobierz łańcuch tekstowy daty narodzin
        self.birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y').date()  # Konwertuj na obiekt daty
        return self.birth_date


    def first_button(self):
        self.button_1 = tk.Button(self.window, text="ile wrzuciłaś do systemu przez ostatni rok?", command=self.make_table)
        self.button_1.grid(row=4, column=0, padx=5, pady=5)
        return self.button_1

    def second_button(self):
        self.button_2 = tk.Button(self.window, text="oblicz ile dostaniesz", command=self.third_label)
        self.button_2.grid(row=17, column=0, padx=5, pady=5)
        return self.button_2


    def make_table(self):
        self.dates_of_due = []
        first_date = self.determine_rest_date()  # Pobierz wartość self.rest_date z determine_rest_date()
        for i in range(12):
            self.dates_of_due.append(first_date)
            date_label = tk.Label(self.table_frame, text=first_date.strftime('%d.%m.%Y'))
            date_label.grid(row=i, column=0, padx=5, pady=5)
            first_date += relativedelta(months=-1)  # Zaktualizuj wartość first_dat

        self.data_entries = []
        for i in range(12):
            data_entry = tk.Entry(self.table_frame, validate='key')
            data_entry.grid(row=i, column=1, padx=5, pady=5)
            data_entry.configure(validatecommand=(self.table_frame.register(self.validate_float), '%P'))
            self.data_entries.append(data_entry)
        print(self.data_entries)

        # self.zipped_table = list(zip(self.dates_of_due, self.data_entries))
        return self.dates_of_due, self.data_entries

    def validate_float(self, input_value):
        try:
            float(input_value)
            return True
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawną wartość liczbową.")
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
            if entry_value and self.validate_float(entry_value):
                try:
                    entry_value = float(entry_value)
                    date_of_paying = datetime.combine(date_of_paying, time())  # Konwertuj date_of_paying na datetime
                    print("Date:", date_of_paying)
                    print("Entry value:", entry_value)
                    if date_of_paying >= border_date and entry_value >= border_value:
                        self.sum_of_value_dues += entry_value
                    elif date_of_paying < border_date and entry_value >= border_value_2022:
                        self.sum_of_value_dues += entry_value
                except ValueError:
                    messagebox.showerror("Błąd", "Wprowadź poprawną wartość liczbową.")
        return self.sum_of_value_dues

    def calculate_average_dues(self):
        self.average_dues = self.sum_of_value_dues/12

    def calculate_base(self):
        self.base = 0.8629 * round(self.average_dues / 0.3409)
        return self.base

    def calculate_sickness_allowence(self):
        self.sickness_allowence = round((self.base/30) * self.amount_of_rest_days, 2)
        return self.sickness_allowence

    def calculate_maternity_allowence(self):
        if self.average_dues != 0:
            self.maternity_allowence = round(0.88 * self.base, 2)
        else:
            self.maternity_allowence = 1000
        return self.maternity_allowence


    def third_label(self):
        if all(entry.get() for entry in self.data_entries):
            self.determine_rest_date()  # Wywołaj tę metodę
            self.determine_birthday()  # Wywołaj tę metodę
            self.calculate_sum_of_value_dues()
            self.calculate_average_dues()
            self.calculate_base()
            self.calculate_sickness_allowence()
            self.calculate_maternity_allowence()

            self.amount_of_rest_days = self.calculate_amount_of_rest_days()  # Oblicz liczbę dni odpoczynku

            self.label_3 = tk.Label(self.window, text=f"""
            będziesz na L4 przez {self.amount_of_rest_days}
            i otrzymasz przez cały ten czas {self.calculate_sickness_allowence()}

            będziesz na urlopie macierzyńskim od dnia {self.birth_date}
            """)
            self.label_3.grid(row=18, column=0, padx=5, pady=5)

            if self.maternity_allowence == 1000:
                text = 'otrzymasz co miesiąc netto 1000zł'
            if self.maternity_allowence != 1000:
                text = f'''jeżeli wybierzesz opcję równych wypłat przez cały rok czyli 81,5% podstawy,
                        to otrzymasz co miesiąc netto {round(0.815 * self.maternity_allowence, 2)},
                        jeżeli wybierzesz opcję zmiennych wypłat czyli 100% podstawy przez 20 tygodni i 70% przez 32 tygodnie,
                        to otrzymasz miesięcznie netto odpowiednio {self.maternity_allowence} lub {round(0.7 * self.maternity_allowence, 2)}'''

            self.label_4 = tk.Label(self.window, text = text)
            self.label_4.grid(row=19, column=0, padx=5, pady=5)



        else:
            messagebox.showerror("Błąd", "Wprowadź wszystkie wymagane wartości.")



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
    app.calculate_sickness_allowence()
    app.calculate_maternity_allowence()
    app.third_label()
    print("Length of dates_of_due:", len(app.dates_of_due))
    print("Length of data_entries:", len(app.data_entries))
    print("Dates of due:", app.dates_of_due)
    print("Data entries:", app.data_entries)
    app.window.mainloop()

if __name__ == "__main__":
    main()

# window_2 = tk.Tk()
# window_2.title("ile wrzuciłaś do systemu?")

# user_input_2 = get_selected_date(calendar_2)  # Pobierz wartość wpisaną przez użytkownika

# date_object = datetime.strptime(user_input_2, "%d.%m.%Y")

# table_frame = tk.Frame(window_2)
# table_frame.pack()



# # dodanie walidatora
# validate_command = master.register(validate_entry)
# data_entry.config(validate="key", validatecommand=(validate_command, '%P'))

#         # przycisk do obliczania sumy
# sum_button = tk.Button(window_2, text="Oblicz sumę", command=calculate_sum)
# sum_button.pack()

# #             # dodanie walidatora
# #             validate_command = self.master.register(self.validate_entry)
# #             data_entry.config(validate="key", validatecommand=(validate_command, '%P'))

# button_2 = tk.Button(window_2, text="oblicz zasiłek macierzyński")
# button_2.pack()

# def calculate_clicked_window:
#     messagebox.showinfo("i co dasz radę?", f"na L4 otrzymasz łącznie {}zł netto,\n zostanie odprowadzony podatek pit wsysokości {}, \n na macierzyńskim otrzymasz {}zł miesięcznie netto, \n co miesiąc zostanie odprowadzony podatek pit wsysokości {}")









