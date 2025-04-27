import requests
from bs4 import BeautifulSoup
import time
import sys
import os
from threading import Thread
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
import random
from datetime import datetime
import re

class Colors:
    RED = "\033[38;2;234;67;53m"    
    BLUE = "\033[38;2;66;133;244m"  
    YELLOW = "\033[38;2;251;188;5m" 
    GREEN = "\033[38;2;52;168;83m"   
    RESET = "\033[0m"
    BOLD = "\033[1m"

class Banner:
    def __init__(self):
        self.console = Console()
        self.banner = """
    ▒█▀▀█ ▒█▀▄▀█ ░█▀▀█ ▀█▀ ▒█░░░ 　 ▒█▀▀▀█ ▒█▀▀▀█ ▀█▀ ▒█▄░▒█ ▀▀█▀▀ 
    ▒█░▄▄ ▒█▒█▒█ ▒█▄▄█ ▒█░ ▒█░░░ 　 ▒█░░▒█ ░▀▀▀▄▄ ▒█░ ▒█▒█▒█ ░▒█░░ 
    ▒█▄▄█ ▒█░░▒█ ▒█░▒█ ▄█▄ ▒█▄▄█ 　 ▒█▄▄▄█ ▒█▄▄▄█ ▄█▄ ▒█░░▀█ ░▒█░░
    """
        
    def get_gradient_color(self, position, length):
        google_colors = [
            (234, 67, 53),   
            (251, 188, 5),   
            (52, 168, 83),   
            (66, 133, 244)   
        ]
        
        idx = (position / length) * (len(google_colors) - 1)
        color1 = google_colors[int(idx)]
        color2 = google_colors[min(int(idx) + 1, len(google_colors) - 1)]
        
        factor = idx - int(idx)
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        
        return f"\033[38;2;{r};{g};{b}m"

    def get_custom_gradient(self, position, length):
        custom_colors = [
            (142, 68, 173),
            (41, 128, 185),
            (39, 174, 96),
            (243, 156, 18)
        ]
        
        idx = (position / length) * (len(custom_colors) - 1)
        color1 = custom_colors[int(idx)]
        color2 = custom_colors[min(int(idx) + 1, len(custom_colors) - 1)]
        
        factor = idx - int(idx)
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        
        return f"\033[38;2;{r};{g};{b}m"

    def display(self):
        os.system('clear')
        lines = self.banner.split('\n')
        colored_banner = ""
        
        for line in lines:
            for char_idx, char in enumerate(line):
                color = self.get_gradient_color(char_idx, len(line))
                colored_banner += f"{color}{char}"
            colored_banner += Colors.RESET + "\n"
        
        print(colored_banner)
        print(f"{Colors.BLUE}\t\t   Creator: github.com/fozzy-developer{Colors.RESET}\n")

class DataFormatter:
    def __init__(self):
        self.console = Console()
        self.sections = {
            "Google Account": "Google Account",
            "Google Chat": "Google Chat",
            "Google Plus": "Google Plus",
            "Play Games": "Games",
            "Maps": "Maps",
            "Calendar": "Calendar"
        }

    def translate_content(self, content):
        translations = {
            "Custom profile picture": "Custom profile picture",
            "Default cover picture": "Default cover picture",
            "Last profile edit": "Last profile edit",
            "Entity Type": "Entity Type",
            "Customer ID": "Customer ID",
            "Enterprise User": "Enterprise User",
            "No player profile found": "No player profile found",
            "Profile page": "Profile page",
            "No review": "No review",
            "No public Google Calendar": "No public Google Calendar"
        }
        
        for eng, rus in translations.items():
            content = content.replace(eng, rus)
        return content

    def format_account_data(self, raw_text):
        sections = {
            "Google Account": {},
            "Google Chat": {},
            "Google Plus": {},
            "Play Games": {},
            "Maps": {},
            "Calendar": {}
        }
        
        current_section = None
        
        for line in raw_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if "🙋 Google Account" in line:
                current_section = "Google Account"
            elif "📞 Google Chat" in line:
                current_section = "Google Chat"
            elif "🌐 Google Plus" in line:
                current_section = "Google Plus"
            elif "🎮 Play Games" in line:
                current_section = "Play Games"
            elif "🗺️ Maps" in line:
                current_section = "Maps"
            elif "🗓️ Calendar" in line:
                current_section = "Calendar"
            
            if current_section and ":" in line:
                key, value = line.split(":", 1)
                sections[current_section][key.strip()] = value.strip()
            elif current_section and line.startswith(("[-]", "[+]")):
                sections[current_section][line[3:].strip()] = ""

        return sections

    def create_section_panel(self, title, content):
        translated_content = self.translate_content(content)
        return Panel(
            Text(translated_content, style="white"),
            title=self.sections.get(title, title),
            style="blue",
            border_style="blue",
            padding=(1, 2)
        )

class GmailOSINT:
    def __init__(self):
        self.console = Console()
        self.banner = Banner()
        self.formatter = DataFormatter()

    def search_account(self, username):
        self.console.print(f"\n[blue][*] Search for information for the user: {username}[/blue]")
        
        url = f"https://gmail-osint.activetk.jp/{username}"
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            raw_data = soup.get_text()
            
            sections = self.formatter.format_account_data(raw_data)
            
            for section_name, section_data in sections.items():
                if section_data:
                    content = "\n".join([f"{k}: {v}" for k, v in section_data.items()])
                    panel = self.formatter.create_section_panel(
                        section_name,
                        content
                    )
                    self.console.print(panel)
            
        except Exception as e:
            self.console.print(f"\n[red][!] Error: {str(e)}[/red]")

    def run(self):
        try:
            self.banner.display()
            
            while True:
                self.console.print(f"\n[yellow]Enter your Gmail username (without @gmail.com):[/yellow]")
                username = input(f"{Colors.GREEN}>>> {Colors.RESET}").strip()
                
                if username:
                    self.search_account(username)
                    
                    self.console.print(f"\n[yellow]Do you want to perform a new search? (yes/no):[/yellow]")
                    if input(f"{Colors.GREEN}>>> {Colors.RESET}").lower() != 'yes':
                        break
                        
        except KeyboardInterrupt:
            self.console.print(f"\n[red][!] The program was stopped by the user[/red]")
        finally:
            self.console.print(f"\n[blue][i] The program is complete[/blue]")

if __name__ == "__main__":
    tool = GmailOSINT()
    tool.run()
