import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from cryptography.fernet import Fernet
import base64
import pyperclip  

BG_COLOR = "#0D0D0D"     
TEXT_COLOR = "#00FF00"    
FONT = ("Courier", 12)    

class RansomwareSimulator:
    def __init__(self, master):
        self.master = master
        master.title("EDUCATIONAL RANSOMWARE SIMULATOR")
        master.configure(bg=BG_COLOR)
        
        # Generate a key for Fernet encryption
        self.key = Fernet.generate_key()
        self.key_string = self.key.decode('utf-8')
        self.cipher = Fernet(self.key)
        
        self.simulation_folder = "simulation_folder"
        if not os.path.exists(self.simulation_folder):
            os.makedirs(self.simulation_folder)
            self.create_dummy_files()

        self.create_widgets()
        
    def create_dummy_files(self):
        dummy_files = {
            "document.txt": "This is a sample document with important information.",
            "notes.txt": "These are my personal notes that I wouldn't want to lose.",
            "contacts.csv": "Name,Email,Phone\nJohn Doe,john@example.com,555-1234\nJane Smith,jane@example.com,555-5678",
            "project_plan.txt": "Project timeline:\n1. Planning - 2 weeks\n2. Development - 8 weeks\n3. Testing - 4 weeks\n4. Deployment - 2 weeks"
        }
        
        for filename, content in dummy_files.items():
            file_path = os.path.join(self.simulation_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def create_widgets(self):
        title_label = tk.Label(
            self.master, 
            text="RANSOMWARE SIMULATION - FOR EDUCATIONAL PURPOSES ONLY",
            bg=BG_COLOR, 
            fg="red", 
            font=("Courier", 14, "bold")
        )
        title_label.pack(pady=10)
        
        warning_label = tk.Label(
            self.master,
            text="⚠️ This is a simulation tool. Do not use for malicious purposes. ⚠️",
            bg=BG_COLOR,
            fg="yellow",
            font=FONT
        )
        warning_label.pack(pady=5)

        self.console = tk.Text(self.master, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=70, height=15)
        self.console.pack(padx=10, pady=10)
        self.console.insert(tk.END, "[ SYSTEM ] Initializing ransomware simulation...\n")
        self.console.insert(tk.END, f"[ SYSTEM ] Simulation folder: {os.path.abspath(self.simulation_folder)}\n")
        self.console.config(state=tk.DISABLED)

        button_frame = tk.Frame(self.master, bg=BG_COLOR)
        button_frame.pack(pady=10)

        self.encrypt_button = tk.Button(
            button_frame, text="Simulate Encryption",
            command=self.start_encryption,
            bg="black", fg="red", font=FONT, relief=tk.RAISED,
            padx=10, pady=5
        )
        self.encrypt_button.pack(side=tk.LEFT, padx=10)

        self.decrypt_button = tk.Button(
            button_frame, text="✅ Simulate Decryption",
            command=self.start_decryption,
            bg="black", fg="green", font=FONT, relief=tk.RAISED,
            padx=10, pady=5, state=tk.DISABLED
        )
        self.decrypt_button.pack(side=tk.LEFT, padx=10)

        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        
        self.status_label = tk.Label(self.master, text="Ready", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.status_label.pack(pady=5)

    def log_message(self, message):
        self.console.config(state=tk.NORMAL)
        for char in message:
            self.console.insert(tk.END, char)
            self.console.update()
            time.sleep(0.01)
        self.console.insert(tk.END, "\n")
        self.console.config(state=tk.DISABLED)
        self.console.see(tk.END)

    def update_status(self, message):
        self.status_label.config(text=message)

    def start_encryption(self):
        self.encrypt_button.config(state=tk.DISABLED)
        self.update_status("Encryption in progress...")
        threading.Thread(target=self.run_encryption, daemon=True).start()

    def encrypt_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = self.cipher.encrypt(data)
            encrypted_path = file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            os.remove(file_path)
            return True
        except Exception as e:
            self.log_message(f"[ ERROR ] Failed to encrypt {file_path}: {str(e)}")
            return False

    def run_encryption(self):
        self.log_message("[ WARNING ] Scanning files for encryption...")
        
        files = [os.path.join(self.simulation_folder, f) 
                for f in os.listdir(self.simulation_folder) 
                if not f.endswith('.encrypted') and f != "READ_ME.txt"]

        if not files:
            self.log_message("[ ERROR ] No files found for encryption!")
            self.update_status("Encryption failed - no files found")
            self.encrypt_button.config(state=tk.NORMAL)
            return

        self.progress["maximum"] = len(files)
        self.progress["value"] = 0
        
        encrypted_count = 0
        for i, file_path in enumerate(files):
            if self.encrypt_file(file_path):
                self.log_message(f"[ ENCRYPTED ] {file_path}")
                encrypted_count += 1
            self.progress["value"] = i + 1
            time.sleep(0.3)

        self.log_message(f"[ COMPLETE ] Encrypted {encrypted_count} of {len(files)} files")
        self.create_ransom_note()
        self.show_payment_interface()
        self.update_status(f"Encryption complete. {encrypted_count} files encrypted.")

    def create_ransom_note(self):
        note_path = os.path.join(self.simulation_folder, "READ_ME.txt")
        note_message = (
            "🔥🔥 ALL YOUR FILES HAVE BEEN ENCRYPTED 🔥🔥\n\n"
            "Your files are now encrypted with military-grade encryption.\n"
            "To recover them, you must pay the ransom!\n"
            "Proceed to the payment portal to simulate payment and receive the decryption key.\n"
            "💀 The clock is ticking... 💀\n"
            "DO NOT try to decrypt the files yourself or they may be permanently lost."
        )
        with open(note_path, 'w', encoding='utf-8') as note:
            note.write(note_message)

    def show_payment_interface(self):
        payment_window = tk.Toplevel(self.master)
        payment_window.title("💳 Payment Portal & Ransom Note")
        payment_window.configure(bg=BG_COLOR)
        payment_window.minsize(500, 600)

        def on_payment_window_close():
            flash_bg(payment_window)
            messagebox.showwarning("Warning", "Payment is required to recover your files!")
        
        payment_window.protocol("WM_DELETE_WINDOW", on_payment_window_close)

        total_seconds = 24 * 60 * 60
        
        countdown_frame = tk.Frame(payment_window, bg="red")
        countdown_frame.pack(fill=tk.X, padx=10, pady=5)
        
        countdown_label = tk.Label(
            countdown_frame,
            text="TIME REMAINING: 24:00:00",
            bg="red",
            fg="white",
            font=("Courier", 14, "bold")
        )
        countdown_label.pack(pady=5)
        
        def update_countdown(remaining):
            if remaining <= 0:
                countdown_label.config(text="TIME EXPIRED!")
                return
            hours, remainder = divmod(remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_label.config(text=f"TIME REMAINING: {hours:02d}:{minutes:02d}:{seconds:02d}")
            payment_window.after(1000, update_countdown, remaining - 1)
        
        update_countdown(total_seconds)

        note_frame = tk.Frame(payment_window, bg=BG_COLOR)
        note_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        note_title = tk.Label(
            note_frame,
            text="!! RANSOM NOTE !!",
            bg=BG_COLOR,
            fg="red",
            font=("Courier", 16, "bold")
        )
        note_title.pack(pady=5)

        note_text = tk.Text(
            note_frame, width=60, height=10,
            bg=BG_COLOR, fg=TEXT_COLOR, font=FONT
        )
        note_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        note_path = os.path.join(self.simulation_folder, "READ_ME.txt")
        with open(note_path, 'r', encoding='utf-8') as note_file:
            note_text.insert(tk.END, note_file.read())
        note_text.config(state=tk.DISABLED)

        payment_frame = tk.Frame(payment_window, bg=BG_COLOR)
        payment_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        payment_title = tk.Label(
            payment_frame,
            text="PAYMENT PORTAL",
            bg=BG_COLOR, fg=TEXT_COLOR,
            font=("Courier", 14, "bold")
        )
        payment_title.pack(pady=5)

        amount_label = tk.Label(
            payment_frame,
            text="RANSOM AMOUNT: $500 IN BITCOIN",
            bg=BG_COLOR, fg="red",
            font=("Courier", 12, "bold")
        )
        amount_label.pack(pady=10)

        payment_details_frame = tk.Frame(payment_frame, bg=BG_COLOR)
        payment_details_frame.pack(pady=10)

        btc_label = tk.Label(
            payment_details_frame, 
            text="Bitcoin Address:", 
            bg=BG_COLOR, 
            fg=TEXT_COLOR, 
            font=FONT
        )
        btc_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        btc_value = tk.Label(
            payment_details_frame, 
            text="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", 
            bg="black", 
            fg=TEXT_COLOR, 
            font=FONT
        )
        btc_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        form_frame = tk.Frame(payment_frame, bg=BG_COLOR)
        form_frame.pack(pady=10)

        cc_label = tk.Label(form_frame, text="Credit Card Number:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        cc_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        cc_entry = tk.Entry(form_frame, font=FONT, width=25)
        cc_entry.grid(row=0, column=1, padx=5, pady=5)

        exp_label = tk.Label(form_frame, text="Expiration Date (MM/YY):", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        exp_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        exp_entry = tk.Entry(form_frame, font=FONT, width=10)
        exp_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        cvv_label = tk.Label(form_frame, text="CVV:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        cvv_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        cvv_entry = tk.Entry(form_frame, font=FONT, width=5, show="*")
        cvv_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        def process_payment():
            if not cc_entry.get().strip() or not exp_entry.get().strip() or not cvv_entry.get().strip():
                messagebox.showerror("Error", "Please fill in all payment fields.")
                return

            pay_button.config(state=tk.DISABLED)
            payment_processing_label = tk.Label(
                payment_frame,
                text="Processing payment...",
                bg=BG_COLOR,
                fg="yellow",
                font=FONT
            )
            payment_processing_label.pack(pady=5)
            payment_window.update()
            time.sleep(2)
            payment_processing_label.destroy()
            
            key_display_frame = tk.Frame(payment_frame, bg="green", padx=10, pady=10)
            key_display_frame.pack(pady=10, fill=tk.X)
            
            key_label = tk.Label(
                key_display_frame,
                text="DECRYPTION KEY:",
                bg="green",
                fg="white",
                font=("Courier", 12, "bold")
            )
            key_label.pack(pady=(5, 0))
            
            key_entry = tk.Entry(
                key_display_frame,
                width=45,
                font=("Courier", 10),
                readonlybackground="black",
                fg="white",
                justify="center"
            )
            key_entry.insert(0, self.key_string)
            key_entry.configure(state="readonly")
            key_entry.pack(pady=(5, 0))
            
            def copy_key():
                pyperclip.copy(self.key_string)
                copy_status.config(text="✓ Key copied to clipboard!")
                payment_window.after(2000, lambda: copy_status.config(text=""))
            
            copy_button = tk.Button(
                key_display_frame,
                text="Copy Key",
                command=copy_key,
                bg="black",
                fg="white",
                font=FONT
            )
            copy_button.pack(pady=5)
            
            copy_status = tk.Label(
                key_display_frame,
                text="",
                bg="green",
                fg="white",
                font=FONT
            )
            copy_status.pack(pady=(0, 5))
            
            self.log_message(f"[ PAYMENT ] Payment accepted. Decryption key provided.")
            
            messagebox.showinfo("Payment Successful", 
                              "Payment processed. Your decryption key has been provided. "
                              "Use this key to decrypt your files.")
            
            self.decrypt_button.config(state=tk.NORMAL)
            
            payment_window.protocol("WM_DELETE_WINDOW", payment_window.destroy)
            
            self.update_status("Payment received. Decryption available.")

        pay_button = tk.Button(
            payment_frame, 
            text="Pay Now", 
            command=process_payment,
            bg="black", 
            fg="green", 
            font=FONT, 
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        pay_button.pack(pady=10)

    def start_decryption(self):
        key_input = simpledialog.askstring("Decryption", "Enter the decryption key:")
        
        if key_input is None:
            return
        
        try:
            if key_input != self.key_string:
                messagebox.showerror("Error", "Incorrect decryption key!")
                return
            
            self.cipher = Fernet(key_input.encode())
            self.decrypt_button.config(state=tk.DISABLED)
            self.update_status("Decryption in progress...")
            threading.Thread(target=self.run_decryption, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Invalid decryption key format: {e}")

    def decrypt_file(self, encrypted_file_path):
        try:
            original_file_path = encrypted_file_path.rsplit('.encrypted', 1)[0]
            with open(encrypted_file_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            with open(original_file_path, 'wb') as f:
                f.write(decrypted_data)
            os.remove(encrypted_file_path)
            return True
        except Exception as e:
            self.log_message(f"[ ERROR ] Failed to decrypt {encrypted_file_path}: {str(e)}")
            return False

    def run_decryption(self):
        self.log_message("[ SYSTEM ] Decryption in progress...")
        
        encrypted_files = [os.path.join(self.simulation_folder, f) 
                         for f in os.listdir(self.simulation_folder) 
                         if f.endswith('.encrypted')]

        if not encrypted_files:
            self.log_message("[ ERROR ] No encrypted files found!")
            self.update_status("Decryption failed - no encrypted files found")
            self.decrypt_button.config(state=tk.NORMAL)
            return

        self.progress["maximum"] = len(encrypted_files)
        self.progress["value"] = 0
        
        decrypted_count = 0
        for i, file_path in enumerate(encrypted_files):
            if self.decrypt_file(file_path):
                self.log_message(f"[ DECRYPTED ] {file_path}")
                decrypted_count += 1
            self.progress["value"] = i + 1
            time.sleep(0.3)

        note_path = os.path.join(self.simulation_folder, "READ_ME.txt")
        if os.path.exists(note_path):
            os.remove(note_path)
            
        self.log_message(f"[ COMPLETE ] Decrypted {decrypted_count} of {len(encrypted_files)} files")
        messagebox.showinfo("Success", f"All files have been decrypted! ({decrypted_count} files recovered)")
        self.encrypt_button.config(state=tk.NORMAL)
        self.update_status("Decryption complete. All files recovered.")

def flash_bg(widget, times=3, delay=200):
    orig_color = widget.cget("bg")
    def flash(count):
        if count % 2 == 0:
            widget.configure(bg="red")
        else:
            widget.configure(bg=orig_color)
        if count < times * 2:
            widget.after(delay, lambda: flash(count+1))
        else:
            widget.configure(bg=orig_color)
    flash(0)

def main():
    root = tk.Tk()
    root.geometry("700x500")
    app = RansomwareSimulator(root)
    
    disclaimer = tk.Label(
        root,
        text="DISCLAIMER: This software is for educational purposes only. Unauthorized use of ransomware is illegal.",
        bg=BG_COLOR,
        fg="yellow",
        font=("Courier", 8)
    )
    disclaimer.pack(side=tk.BOTTOM, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()