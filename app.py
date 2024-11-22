import os
import threading
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Download por link")
        self.root.geometry("650x450")
        self.root.minsize(650, 450)
        
        # Estilo e tema
        style = ttk.Style(self.root)
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "light")
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Campos da interface
        self.create_widgets()

    def create_widgets(self):
        """Cria e organiza os widgets na interface."""
        ttk.Label(self.main_frame, text="Digite o link do vídeo:", anchor="center").grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = ttk.Entry(self.main_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.main_frame, text="Escolha o formato:", anchor="center").grid(row=1, column=0, padx=10, pady=10)
        self.format_var = tk.StringVar(value="mp4")
        format_frame = ttk.Frame(self.main_frame)
        format_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        ttk.Radiobutton(format_frame, text="MP4", variable=self.format_var, value="mp4").pack(side="left")
        ttk.Radiobutton(format_frame, text="MP3", variable=self.format_var, value="mp3").pack(side="left")

        # Adicionar opções de resolução ao escolher MP4
        ttk.Label(self.main_frame, text="Escolha a resolução:", anchor="center").grid(row=2, column=0, padx=10, pady=10)
        self.resolution_var = tk.StringVar(value="720")
        resolution_menu = ttk.OptionMenu(self.main_frame, self.resolution_var, "720", "360", "480", "720", "1080")
        resolution_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Botão para iniciar o download
        download_button = ttk.Button(self.main_frame, text="Baixar", command=self.start_download)
        download_button.grid(row=3, column=1, padx=10, pady=20)

        # Adicionar espaçamentos entre elementos
        for widget in self.main_frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)

    def start_download(self):
        """Inicia o processo de download."""
        url = self.url_entry.get()
        format_choice = self.format_var.get()
        output_dir = filedialog.askdirectory()
        resolution = self.resolution_var.get()

        if not url:
            messagebox.showerror("Erro", "O campo do link está vazio!")
            return
        if not output_dir:
            messagebox.showerror("Erro", "Por favor, selecione o diretório de destino!")
            return

        # Criar um modal para exibir o progresso
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progresso do download")
        
        progress_label = ttk.Label(progress_window, text="Progresso: 0%")
        progress_label.pack(pady=10)

        pbar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        pbar.pack(padx=20, pady=10)

        # Executar o download em uma thread separada
        threading.Thread(target=self.download_video, args=(url, format_choice, output_dir, resolution, pbar, progress_label, progress_window)).start()

    def download_video(self, url, format_choice, output_dir, resolution, pbar, progress_label, progress_window):
        """Baixa o vídeo utilizando yt-dlp e atualiza a barra de progresso."""
        def update_progress(d):
            """Atualiza a barra de progresso e o status do download."""
            if d['status'] == 'downloading':
                percent = d.get('percentage', 0)
                pbar['value'] = percent
                progress_label.config(text=f"Progresso: {percent:.2f}%")
                self.root.update_idletasks()
            elif d['status'] == 'finished':
                pbar['value'] = 100
                progress_label.config(text="Download concluído!")
                self.root.update_idletasks()
                progress_window.destroy()
        try:
            # Corrigir o formato para garantir que o áudio seja baixado corretamente
            ydl_opts = {
                'format': f"bestvideo[height<={resolution}]+bestaudio/best" if format_choice == 'mp4' else 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [update_progress],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if format_choice == 'mp3' else []
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloadApp(root)
    root.mainloop()
