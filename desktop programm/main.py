import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk
import serial
import serial.tools.list_ports
import time
import threading
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")

class textIde(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("DroneIDE")
        self.geometry("1000x800")
        
        # Create main layout
        self.grid_columnconfigure(1, weight=1)  # Column with editor and terminal should expand
        self.grid_rowconfigure(0, weight=1)     # Make the main content expand
        
        # Toolbar on the left
        self.toolbar = ctk.CTkFrame(self, width=50)
        self.toolbar.grid(row=0, column=0, sticky="nsew")
        
        # Main content area
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=3)  # Editor gets 3 parts
        self.main_content.grid_rowconfigure(1, weight=1)  # Terminal gets 1 part

        # Editor frame
        self.editor_frame = ctk.CTkFrame(self.main_content)
        self.editor_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Terminal frame
        self.terminal_frame = ctk.CTkFrame(self.main_content)
        self.terminal_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add separator between editor and terminal
        self.separator = ttk.Separator(self.main_content, orient='horizontal')
        self.separator.grid(row=0, column=0, sticky="sew")

        # Toolbar content
        self.label = ctk.CTkLabel(self.toolbar, text="FGSDr", font=("Arial", 15))
        self.label.pack(pady=10)

        self.paint_button = ctk.CTkButton(self.toolbar, text="Open", command=self.save)
        self.paint_button.pack(fill="x", pady=10)

        self.ide_button = ctk.CTkButton(self.toolbar, text="Save", command=self.open)
        self.ide_button.pack(fill="x", pady=10)

        self.run_button = ctk.CTkButton(self.toolbar, text="Quit", command=self.quit)
        self.run_button.pack(fill="x", pady=10)

        # Arduino IDE components
        self.port_label = ctk.CTkLabel(self.toolbar, text="com port:")
        self.port_label.pack(pady=5)

        self.port_combo = ctk.CTkComboBox(self.toolbar, values=[])
        self.port_combo.pack(pady=5)

        # Set the first port as the default selection if there are any ports available
        ports = self.get_serial_ports()
        if ports:
            self.port_combo.set(ports[0])  # Выбор первого порта по умолчанию

        self.send_button = ctk.CTkButton(self.toolbar, text="Upload", command=self.send_code)
        self.send_button.pack(pady=5)

        self.send_line_button = ctk.CTkButton(self.toolbar, text="Send Line", command=self.send_line)
        self.send_line_button.pack(pady=5)

        # Editor setup
        self.line_number_area = tk.Text(self.editor_frame, width=5, font=("Consolas", 12))
        self.line_number_area.pack(side=ctk.LEFT, fill="y")
        
        self.text_area = tk.Text(self.editor_frame, font=("Consolas", 12))
        self.text_area.pack(side=ctk.LEFT, fill="both", expand=True)
        self.text_area.tag_config('keyword', foreground='#f250e7')  # purple
        self.text_area.tag_config('builtin', foreground='#9950f2')  # blue-violet
        self.text_area.tag_config('string', foreground='#6a8759')  # green
        self.text_area.tag_config('comment', foreground='#8d9ba6')  # dark green
        self.text_area.tag_config('unknown', foreground='#84adf0')  # blue-violet
        self.text_area.tag_config('class', foreground='#48b083')  # green-blue
        self.text_area.tag_config('clas', foreground='#50adfa')  # green-blue
        self.text_area.tag_config('def_func', foreground='#dee86d')  # light green

        self.keywords = ['if', 'else', 'for', 'while', 'import', 'class', 'function', 'func', 'return', '++', '+', '>', '<', '=', '@obj', 'case', 'forward()', 'back()', 'start()', 'landing()']
        self.builtins = ['self', 'print', 'len', 'range', 'list', 'dict', 'set', 'int', 'float', 'str', 'bool', 'var', 'let']
        self.strings = ['"', "'", '"""', "'''"]
        self.comments = ['// ']
        self.clas = ['class', 'function', '++', '+', '>', '<', '=', '@obj', 'case']

        self.text_area.bind("<KeyRelease>", self.highlight_syntax_realtime)  

        self.serial_port = None
        self.current_line = 1
        self.text_area.tag_config('current_line', background='yellow')

        self.port_combo.bind("<FocusIn>", self.update_ports)

        # Terminal setup
        self.terminal_header = ctk.CTkFrame(self.terminal_frame)
        self.terminal_header.pack(fill="x", padx=5, pady=2)
        
        self.terminal_label = ctk.CTkLabel(self.terminal_header, text="Serial Port Monitor")
        self.terminal_label.pack(side="left", padx=5)
        
        self.autoscroll_var = tk.BooleanVar(value=True)
        self.autoscroll_check = ctk.CTkCheckBox(self.terminal_header, text="Autoscroll", variable=self.autoscroll_var)
        self.autoscroll_check.pack(side="right", padx=5)
        
        self.clear_terminal_btn = ctk.CTkButton(self.terminal_header, text="Clear", width=60, command=self.clear_terminal)
        self.clear_terminal_btn.pack(side="right", padx=5)
        
        # Create scrolled text widget for serial output
        self.serial_output = tk.Text(self.terminal_frame, font=("Consolas", 12), height=8, bg='black', fg='#00FF00')
        self.serial_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure tags for different message types
        self.serial_output.tag_configure('received', foreground='#00FF00')  # Зеленый для входящих
        self.serial_output.tag_configure('sent', foreground='#00FFFF')      # Голубой для исходящих
        
        # Add scrollbar to serial output
        self.serial_scrollbar = ttk.Scrollbar(self.terminal_frame, orient="vertical", command=self.serial_output.yview)
        self.serial_output.configure(yscrollcommand=self.serial_scrollbar.set)
        self.serial_scrollbar.pack(side="right", fill="y")
        
        # Initialize serial reading flag
        self.is_reading_serial = False

    def get_serial_ports(self):
        """Получить список доступных последовательных портов"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

    def update_ports(self, event=None):
        """Update the list of available serial ports in the combobox."""
        start_time = time.time()
        timeout = 1  # seconds
        while time.time() - start_time < timeout:
            ports = self.get_serial_ports()
            if ports and self.port_combo.get() not in ports:
                self.port_combo.configure(values=ports)
                self.port_combo.set(ports[0])
                return
            elif ports and not self.port_combo.cget("values"):
                 self.port_combo.configure(values=ports)
                 self.port_combo.set(ports[0])
                 return
            time.sleep(0.2)  # Check every 200ms
        # If no new ports are found after the timeout, update with whatever is available
        ports = self.get_serial_ports()
        self.port_combo.configure(values=ports)
        if ports and self.port_combo.get() not in ports:
            self.port_combo.set(ports[0])

    def start_serial_monitor(self):
        """Start monitoring the serial port in a separate thread"""
        if not self.serial_port or not self.serial_port.is_open:
            try:
                selected_port = self.port_combo.get()
                self.serial_port = serial.Serial(
                    port=selected_port,
                    baudrate=115200,
                    timeout=0.1,  # Уменьшаем timeout для более быстрого чтения
                    write_timeout=1
                )
                time.sleep(0.5)  # Уменьшаем время ожидания после открытия порта
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open port: {e}")
                return
                
        self.is_reading_serial = True
        self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.serial_thread.start()
        
    def stop_serial_monitor(self):
        """Stop monitoring the serial port"""
        self.is_reading_serial = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            
    def log_to_serial_monitor(self, message, message_type='received'):
        """Add a message to the serial monitor with timestamp"""
        if not message or message.isspace():
            return
        timestamp = time.strftime('%H:%M:%S', time.localtime())
        direction = '>>' if message_type == 'sent' else '<<'
        formatted_message = f"[{timestamp}] {direction} {message}\n"
        self.after(0, self._update_serial_output, formatted_message, message_type)
        
    def _update_serial_output(self, message, message_type):
        """Update the serial monitor with new message"""
        self.serial_output.insert(tk.END, message, message_type)
        if self.autoscroll_var.get():
            self.serial_output.see(tk.END)
            
    def read_serial(self):
        """Read data from serial port and display it in the serial monitor"""
        while self.is_reading_serial:
            if self.serial_port and self.serial_port.is_open:
                try:
                    if self.serial_port.in_waiting:
                        data = self.serial_port.read(self.serial_port.in_waiting).decode('utf-8', errors='ignore')
                        if data:
                            self.log_to_serial_monitor(data.strip(), 'received')
                except Exception as e:
                    error_msg = f"Error reading serial port: {str(e)}"
                    self.log_to_serial_monitor(error_msg, 'received')
                    print(error_msg)
                    break
            time.sleep(0.01)  # Уменьшаем задержку для более быстрого чтения
            
    def send_code(self):
        """Send code to the selected serial port"""
        if self.serial_port is None or not self.serial_port.is_open:
            try:
                selected_port = self.port_combo.get()
                self.serial_port = serial.Serial(
                    port=selected_port,
                    baudrate=115200,
                    timeout=0.1,
                    write_timeout=1
                )
                time.sleep(0.5)
                # Start serial monitor when connection is established
                self.start_serial_monitor()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open port: {e}")
                return

        code = self.text_area.get("1.0", tk.END)
        try:
            self.serial_port.write(code.encode('utf-8'))
            self.log_to_serial_monitor(code.strip(), 'sent')
        except Exception as e:
            self.log_to_serial_monitor(f"Error sending data: {str(e)}", 'sent')
            
    def auto_brace(self, event):
        if event.char in "{}[]()<>":
            self.text_area.insert("insert", event.char)
            self.text_area.insert("insert", self.get_closing_brace(event.char))
            self.text_area.mark_set("insert", "insert -1c")

    def get_closing_brace(self, char):
        braces = {"{": "}", "[": "]", "(": ")", "<":">"}
        return braces[char]

    def update_line_numbers(self):
        self.line_number_area.delete("1.0", "end")
        for i, line in enumerate(self.text_area.get("1.0", "end").split("\n"), start=1):
            self.line_number_area.insert("end", f"{i}\n")
        self.after(100, self.update_line_numbers)

    def highlight_syntax_realtime(self, event):
        self.text_area.tag_remove('keyword', '1.0', 'end')
        self.text_area.tag_remove('builtin', '1.0', 'end')
        self.text_area.tag_remove('string', '1.0', 'end')
        self.text_area.tag_remove('comment', '1.0', 'end')
        self.text_area.tag_remove('unknown', '1.0', 'end')
        self.text_area.tag_remove('class', '1.0', 'end')
        self.text_area.tag_remove('clas', '1.0', 'end')
        self.text_area.tag_remove('def_func', '1.0', 'end')

        text = self.text_area.get('1.0', 'end-1c')
        lines = text.split('\n')

        for i, line in enumerate(lines, 1):
            words = line.split()
            for j, word in enumerate(words):
                if word in self.keywords:
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('keyword', start, end)

                elif word in self.builtins:
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('builtin', start, end)

                elif word == 'class':
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('clas', start, end)

                    if j + 1 < len(words):
                        next_word = words[j + 1]
                        start = f'{i}.{line.index(next_word)}'
                        end = f'{i}.{line.index(next_word) + len(next_word)}'
                        self.text_area.tag_add('class', start, end)

                elif word == 'def':
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('clas', start, end)

                    if j + 1 < len(words):
                        next_word = words[j + 1]
                        start = f'{i}.{line.index(next_word)}'
                        end = f'{i}.{line.index(next_word) + len(next_word)}'
                        self.text_area.tag_add('def_func', start, end)

                elif word.endswith('__') or word.endswith('.__'):  # Check for class names
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('class', start, end)

                elif word not in self.keywords and word not in self.builtins and not word.isdigit():
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('unknown', start, end)

            for string in self.strings:
                if string in line:
                    start = f'{i}.{line.index(string)}'
                    end = f'{i}.{line.index(string) + len(string)}'
                    self.text_area.tag_add('string', start, end)

            for comment in self.comments:
                if comment in line:
                    start = f'{i}.{line.index(comment)}'
                    end = f'{i}.end'
                    self.text_area.tag_add('comment', start, end)

    def run(self):
        self.mainloop()

    def open(self):
        self.text_area.delete("1.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".fde", filetypes=[('FDE', '*.fde')])
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get("1.0", tk.END)
                file.write(code)

    def save(self):
        file_path = filedialog.askopenfilename(filetypes=[('FDE', '*.fde')])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, code)

    def quit(self):
        """Clean up and close the application"""
        self.stop_serial_monitor()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.destroy()

    def highlight_line(self, line_number):
        """Highlights the given line number in the text area."""
        self.text_area.tag_remove('current_line', '1.0', tk.END)  # Remove previous highlights
        start = f'{line_number}.0'
        end = f'{line_number}.end'
        self.text_area.tag_add('current_line', start, end)
        self.text_area.see(start)  # Scroll to the current line

    def send_line(self):
        """Отправить код построчно на выбранный последовательный порт"""
        if self.serial_port is None or not self.serial_port.is_open:
            try:
                selected_port = self.port_combo.get()
                self.serial_port = serial.Serial(
                    port=selected_port,
                    baudrate=115200,
                    timeout=0.1,
                    write_timeout=1
                )
                time.sleep(0.5)
                self.start_serial_monitor()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open port: {e}")
                return

        code = self.text_area.get("1.0", tk.END)
        lines = code.split('\n')
        if self.current_line <= len(lines):
            line = lines[self.current_line - 1] + '\n'
            try:
                self.serial_port.write(line.encode('utf-8'))
                self.log_to_serial_monitor(line.strip(), 'sent')
            except Exception as e:
                self.log_to_serial_monitor(f"Error sending line: {str(e)}", 'sent')
            self.highlight_line(self.current_line)
            self.current_line += 1
        else:
            messagebox.showinfo("Информация", "Весь код отправлен!")
            self.text_area.tag_remove('current_line', '1.0', tk.END)
            self.current_line = 1

    def clear_terminal(self):
        """Clear the serial monitor output"""
        self.serial_output.delete(1.0, tk.END)

if __name__ == "__main__":
    app = textIde()
    app.run()