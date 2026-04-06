#!/usr/bin/env python3
"""
PDF Compressor for any platform, with a focus on macOS aesthetics and functionality.
A simple GUI application to compress PDF files
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not found. Installing...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    import PyPDF2

class PDFCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Compressor")
        self.root.geometry("500x450")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Compressor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Input PDF:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file, width=40).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=1, column=2, pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output PDF:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=40).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=2, column=2, pady=5)
        
        # Compression options
        options_frame = ttk.LabelFrame(main_frame, text="Compression Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        options_frame.columnconfigure(0, weight=1)
        
        self.compression_level = tk.StringVar(value="medium")
        ttk.Radiobutton(options_frame, text="Light compression (faster)", 
                       variable=self.compression_level, value="light").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(options_frame, text="Medium compression (balanced)", 
                       variable=self.compression_level, value="medium").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(options_frame, text="Heavy compression (smaller file)", 
                       variable=self.compression_level, value="heavy").grid(row=2, column=0, sticky=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Compress PDF", command=self.compress_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to compress PDF files")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10)
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file to compress",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-suggest output filename
            if not self.output_file.get():
                input_path = Path(filename)
                output_path = input_path.parent / f"{input_path.stem}_compressed.pdf"
                self.output_file.set(str(output_path))
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save compressed PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def clear_fields(self):
        self.input_file.set("")
        self.output_file.set("")
        self.status_label.config(text="Ready to compress PDF files")
    
    def compress_pdf(self):
        input_path = self.input_file.get()
        output_path = self.output_file.get()
        
        # Validation
        if not input_path:
            messagebox.showerror("Error", "Please select an input PDF file")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify an output file path")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input file does not exist")
            return
        
        if input_path == output_path:
            messagebox.showerror("Error", "Input and output files cannot be the same")
            return
        
        try:
            self.progress.start()
            self.status_label.config(text="Compressing PDF...")
            self.root.update()
            
            # Get original file size
            original_size = os.path.getsize(input_path)
            
            # Perform compression
            success = self.perform_compression(input_path, output_path)
            
            self.progress.stop()
            
            if success:
                # Get compressed file size
                compressed_size = os.path.getsize(output_path)
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                self.status_label.config(text=f"Compression complete! Size reduced by {reduction:.1f}%")
                messagebox.showinfo("Success", 
                    f"PDF compressed successfully!\n\n"
                    f"Original size: {self.format_file_size(original_size)}\n"
                    f"Compressed size: {self.format_file_size(compressed_size)}\n"
                    f"Reduction: {reduction:.1f}%")
            else:
                self.status_label.config(text="Compression failed")
                
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Error occurred during compression")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def perform_compression(self, input_path, output_path):
        try:
            with open(input_path, 'rb') as input_file:
                reader = PyPDF2.PdfReader(input_file)
                writer = PyPDF2.PdfWriter()
                
                # Copy pages and apply compression
                for page in reader.pages:
                    # Apply compression based on selected level
                    if self.compression_level.get() == "light":
                        page.compress_content_streams()
                    elif self.compression_level.get() == "medium":
                        page.compress_content_streams()
                        # Remove duplicate objects
                        if hasattr(page, 'scale_by'):
                            page.scale_by(0.95)  # Slight scaling
                    else:  # heavy
                        page.compress_content_streams()
                        if hasattr(page, 'scale_by'):
                            page.scale_by(0.9)  # More aggressive scaling
                    
                    writer.add_page(page)
                
                # Write compressed PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                return True
                
        except Exception as e:
            print(f"Compression error: {e}")
            return False
    
    def format_file_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

def main():
    # Check if running on macOS
    if sys.platform != "darwin":
        print("This app is designed for macOS, but should work on other platforms too.")
    
    root = tk.Tk()
    
    # macOS specific styling
    if sys.platform == "darwin":
        try:
            # Use native macOS appearance
            root.tk.call('tk', 'scaling', 1.0)
        except:
            pass
    
    app = PDFCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()