import requests
import tkinter as tk
from tkinter import ttk, messagebox
import locale
from googletrans import Translator


system_lang = locale.getdefaultlocale()[0].split('_')[0]


translator = Translator()


def translate_text(text):
    try:
        return translator.translate(text, dest=system_lang).text
    except:
        return text  


def get_currency_list():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return list(data["rates"].keys())
    except:
        messagebox.showerror(translate_text("Error"), translate_text("Failed to fetch currency list!"))
        return []


def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from.get()
        to_currency = combo_to.get()

        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = response.json()
        rate = data["rates"].get(to_currency, None)

        if rate is None:
            messagebox.showerror(translate_text("Error"), translate_text("Invalid currency selection!"))
            return
        
        converted_amount = amount * rate
        label_result.config(text=f"{translate_text('Converted Amount')}: {converted_amount:.2f} {to_currency}")
    except ValueError:
        messagebox.showerror(translate_text("Error"), translate_text("Please enter a valid number!"))
    except:
        messagebox.showerror(translate_text("Error"), translate_text("Failed to fetch exchange rates!"))


root = tk.Tk()
root.title("Global Currency Converter")
root.geometry("400x300")


currencies = get_currency_list()

label_amount = tk.Label(root, text=translate_text("Enter amount:"), font=("Arial", 12))
label_amount.pack(pady=5)
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

label_from = tk.Label(root, text=translate_text("From Currency:"), font=("Arial", 12))
label_from.pack(pady=5)
combo_from = ttk.Combobox(root, values=currencies, font=("Arial", 12))
combo_from.set("USD")  
combo_from.pack(pady=5)

label_to = tk.Label(root, text=translate_text("To Currency:"), font=("Arial", 12))
label_to.pack(pady=5)
combo_to = ttk.Combobox(root, values=currencies, font=("Arial", 12))
combo_to.set("EGP")  
combo_to.pack(pady=5)

button_convert = tk.Button(root, text=translate_text("Convert"), font=("Arial", 12), command=convert_currency)
button_convert.pack(pady=10)

label_result = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_result.pack(pady=5)

root.mainloop()