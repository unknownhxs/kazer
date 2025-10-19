#!/usr/bin/env python3
"""
Python Console File Manager
A menu-driven file manager for console/terminal use.
"""

import os
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

try:
    import pyfiglet
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False

try:
    import termios
    import tty
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False


class FileManager:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.running = True
        self.selected_index = 0
        self.items = []
        self.menu_mode = False
        self.current_language = "en"
        self.translations = self.load_translations()
        self.filter_active = False
        self.filter_pattern = ""
        self.all_items = []  # Store all items when filter is active
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_terminal_size(self):
        """Get terminal size (rows, columns)"""
        try:
            if os.name == 'nt':  # Windows
                import shutil
                size = shutil.get_terminal_size()
                return size.lines, size.columns
            else:  # Unix/Linux/Mac
                import shutil
                size = shutil.get_terminal_size()
                return size.lines, size.columns
        except:
            # Fallback to default size
            return 24, 80
        
    def get_key(self):
        """Get a single keypress from the user"""
        if HAS_MSVCRT:  # Windows
            key = msvcrt.getch()
            if key == b'\xe0':  # Special key
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'UP'
                elif key == b'P':  # Down arrow
                    return 'DOWN'
                elif key == b'K':  # Left arrow
                    return 'LEFT'
                elif key == b'M':  # Right arrow
                    return 'RIGHT'
                elif key == b'G':  # Home
                    return 'HOME'
                elif key == b'O':  # End
                    return 'END'
                elif key == b'I':  # Page Up
                    return 'PAGE_UP'
                elif key == b'Q':  # Page Down
                    return 'PAGE_DOWN'
            elif key == b'\r':  # Enter
                return 'ENTER'
            elif key == b'\x08':  # Backspace
                return 'BACKSPACE'
            elif key == b'\x1b':  # Escape
                return 'ESCAPE'
            elif key == b'/':  # Forward slash for search
                return '/'
            elif key == b'\x03':  # Ctrl+C
                return 'CTRL_C'
            elif key == b'\x13':  # Ctrl+S
                return 'CTRL_S'
            elif key == b'\x04':  # Ctrl+D
                return 'CTRL_D'
            elif key == b'\x7f':  # Delete
                return 'DELETE'
            elif key == b'\x08':  # Backspace
                return 'BACKSPACE'
            elif key == b'\x1a':  # Insert
                return 'INSERT'
            else:
                return key.decode('utf-8', errors='ignore').upper()
        elif HAS_TERMIOS:  # Unix/Linux/Mac
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # Escape sequence
                    ch = sys.stdin.read(2)
                    if ch == '[A':
                        return 'UP'
                    elif ch == '[B':
                        return 'DOWN'
                    elif ch == '[D':
                        return 'LEFT'
                    elif ch == '[C':
                        return 'RIGHT'
                    elif ch == '[H':
                        return 'HOME'
                    elif ch == '[F':
                        return 'END'
                    elif ch == '[5~':
                        return 'PAGE_UP'
                    elif ch == '[6~':
                        return 'PAGE_DOWN'
                elif ch == '\r' or ch == '\n':
                    return 'ENTER'
                elif ch == '\x7f':  # Backspace
                    return 'BACKSPACE'
                elif ch == '\x1b':
                    return 'ESCAPE'
                elif ch == '/':  # Forward slash for search
                    return '/'
                elif ch == '\x03':  # Ctrl+C
                    return 'CTRL_C'
                elif ch == '\x13':  # Ctrl+S
                    return 'CTRL_S'
                elif ch == '\x04':  # Ctrl+D
                    return 'CTRL_D'
                elif ch == '\x7f':  # Delete
                    return 'DELETE'
                elif ch == '\x1a':  # Insert
                    return 'INSERT'
                else:
                    return ch.upper()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            # Fallback to input() if no key detection available
            return input(f"{self.get_text('press_enter_continue')}...")
        
    def display_logo(self):
        """Display KASER logo using pyfiglet if available"""
        if HAS_PYFIGLET:
            try:
                logo = pyfiglet.figlet_format("KASER", font="slant")
                print(logo)
            except:
                print("=" * 50)
                print("           📁 KASER FILE MANAGER 📁")
                print("=" * 50)
        else:
            print("=" * 50)
            print("           📁 KASER FILE MANAGER 📁")
            print("=" * 50)
        print()
        
    def display_current_path(self):
        """Display the current directory path"""
        print(f"📂 {self.get_text('current_directory')}: {self.current_dir}")
        if self.filter_active:
            filter_display = self.get_filter_display_name()
            print(f"🔍 {self.get_text('filter_active')}: {filter_display}")
        print("─" * 60)
        
    def list_directory(self):
        """List files and folders in current directory"""
        try:
            items = list(self.current_dir.iterdir())
            if not items:
                print(f"📭 {self.get_text('directory_is_empty')}")
                return
                
            # Sort directories first, then files
            directories = []
            files = []
            
            for item in items:
                if item.is_dir():
                    directories.append(item)
                else:
                    files.append(item)
                    
            directories.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())
            
            print(f"{'📄 Name':<42} {'Type':<10} {'Size':<15} {'Modified'}")
            print("─" * 80)
            
            # Display directories
            for directory in directories:
                try:
                    stat = directory.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    print(f"📁 {directory.name:<40} {'[DIR]':<10} {'':<15} {modified}")
                except PermissionError:
                    print(f"📁 {directory.name:<40} {'[DIR]':<10} {'':<15} {'🚫 ' + self.get_text('access_denied')}")
            
            # Display files
            for file in files:
                try:
                    stat = file.stat()
                    size = self.format_size(stat.st_size)
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    file_emoji = self.get_file_emoji(file.suffix)
                    print(f"{file_emoji} {file.name:<39} {'[FILE]':<10} {size:<15} {modified}")
                except PermissionError:
                    print(f"📄 {file.name:<39} {'[FILE]':<10} {'🚫 ' + self.get_text('access_denied'):<15} {'🚫 ' + self.get_text('access_denied')}")
                    
        except PermissionError:
            print(f"🚫 {self.get_text('permission_denied')}")
            
    def get_file_emoji(self, suffix):
        """Get appropriate emoji for file type based on extension"""
        emoji_map = {
            '.py': '🐍', '.js': '🟨', '.html': '🌐', '.css': '🎨', '.json': '📋',
            '.xml': '📄', '.txt': '📝', '.md': '📖', '.pdf': '📕', '.doc': '📘',
            '.docx': '📘', '.xls': '📊', '.xlsx': '📊', '.ppt': '📽️', '.pptx': '📽️',
            '.zip': '🗜️', '.rar': '🗜️', '.7z': '🗜️', '.tar': '🗜️', '.gz': '🗜️',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.bmp': '🖼️',
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.mp4': '🎬', '.avi': '🎬',
            '.mov': '🎬', '.mkv': '🎬', '.exe': '⚙️', '.msi': '⚙️', '.deb': '📦',
            '.rpm': '📦', '.dmg': '💿', '.iso': '💿', '.sql': '🗃️', '.db': '🗃️',
            '.log': '📋', '.ini': '⚙️', '.cfg': '⚙️', '.conf': '⚙️', '.bat': '⚙️',
            '.sh': '⚙️', '.ps1': '⚙️'
        }
        return emoji_map.get(suffix.lower(), '📄')
        
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
        
    def load_translations(self):
        """Load translation strings from external JSON file"""
        import json
        try:
            with open('file manager/translations.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Translation file not found, using fallback translations")
            return self.get_fallback_translations()
        except Exception as e:
            print(f"⚠️ Error loading translations: {e}")
            return self.get_fallback_translations()
    
    def get_fallback_translations(self):
        """Fallback translations if JSON file is not available"""
        return {
            "en": {
                "main_menu": "MAIN MENU",
                "navigation": "Navigation",
                "settings": "Settings",
                "exit": "Exit",
                "current_directory": "Current Directory",
                "back_to_main_menu": "Back to main menu",
                "choose_option": "Choose an option",
                "press_enter_continue": "Press Enter to continue",
                "controls_navigate": "↑↓ Navigate",
                "controls_select": "Enter Select",
                "controls_back": "ESC Back",
                "directory_is_empty": "Directory is empty",
                "permission_denied": "Permission denied to access this directory",
                "access_denied": "Access Denied"
            },
            "fr": {
                "main_menu": "MENU PRINCIPAL",
                "navigation": "Navigation",
                "settings": "Paramètres",
                "exit": "Quitter",
                "current_directory": "Répertoire Actuel",
                "back_to_main_menu": "Retour",
                "choose_option": "Choisir une option",
                "press_enter_continue": "Appuyez sur Entrée pour continuer",
                "controls_navigate": "↑↓ Naviguer",
                "controls_select": "Entrée Sélectionner",
                "controls_back": "Échap Retour",
                "directory_is_empty": "Le répertoire est vide",
                "permission_denied": "Permission refusée pour accéder à ce répertoire",
                "access_denied": "Accès Refusé"
            }
        }
        

    def get_text(self, key):
        """Get translated text for current language"""
        return self.translations.get(self.current_language, {}).get(key, 
               self.translations.get("en", {}).get(key, key))
        
    def load_language_settings(self):
        """Load language from settings file"""
        try:
            with open('file manager/data.json', 'r') as f:
                import json
                settings = json.load(f)
                self.current_language = settings.get("language", "en")
        except:
            self.current_language = "en"
    def settings_menu(self):
        """Display and handle settings menu"""
        # Si data.json n'existe pas, creer avec les valeurs par defaut
        if not os.path.exists('file manager/data.json'):
            default_settings = {
                "language": "en",
                "theme": "default",
                "show_hidden": False,
                "sort_by": "name"
            }
            with open('file manager/data.json', 'w') as f:
                import json
                json.dump(default_settings, f, indent=4)
        
        while True:
            self.clear_screen()
            self.display_logo()
            self.load_language_settings()  # Load current language
            print(f"⚙️ {self.get_text('settings_menu')}")
            print(f"1. {self.get_text('change_language')}")
            print(f"2. {self.get_text('display_preferences')}")
            print(f"3. {self.get_text('view_current_settings')}")
            print(f"4. {self.get_text('reset_to_defaults')}")
            print(f"5. {self.get_text('back_to_main_menu')}")
            
            choice = input(f"\n🎯 {self.get_text('choose_option')} (1-5): ").strip()
            
            if choice == "1":
                self.change_language()
            elif choice == "2":
                self.display_preferences()
            elif choice == "3":
                self.view_current_settings()
            elif choice == "4":
                self.reset_to_defaults()
            elif choice == "5":
                break
            else:
                print(f"❌ {self.get_text('invalid_choice')}. Please enter 1-5.")
                input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
                
    def change_language(self):
        """Change the application language"""
        import json
        
        # Load current settings
        try:
            with open('file manager/data.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {"language": "en"}
        
        print(f"\n🌍 {self.get_text('available_languages')}:")
        print("1. English (en)")
        print("2. Français (fr)")
        print("3. Español (es)")
        print("4. Deutsch (de)")
        print("5. 日本語 (ja)")
        print("6. Русский (ru)")
        print("7. 中文 (zh)")
        print("8. العربية (ar)")
        print("9. हिन्दी (hi)")
        print("10. Português (pt)")
        print("11. Italiano (it)")
        print("12. Nederlands (nl)")
        print("13. Polski (pl)")
        print("14. Türkçe (tr)")
        print("15. 한국어 (ko)")
        print("16. ไทย (th)")
        print("17. Tiếng Việt (vi)")
        print("18. Bahasa Indonesia (id)")
        print("19. Українська (uk)")
        print("20. Čeština (cs)")
        print("21. Magyar (hu)")
        print("22. Română (ro)")
        print("23. Български (bg)")
        print("24. Hrvatski (hr)")
        print("25. Suomi (fi)")
        print("26. Norsk (no)")
        print("27. Svenska (sv)")
        print("28. Dansk (da)")
        print("29. Ελληνικά (el)")
        print("30. עברית (he)")
        print(f"31. {self.get_text('cancel')}")
        
        choice = input(f"\n🎯 {self.get_text('choose_language')} (1-31): ").strip()
        
        language_map = {
            "1": "en", "2": "fr", "3": "es", "4": "de", "5": "ja", "6": "ru",
            "7": "zh", "8": "ar", "9": "hi", "10": "pt", "11": "it", "12": "nl",
            "13": "pl", "14": "tr", "15": "ko", "16": "th", "17": "vi", "18": "id",
            "19": "uk", "20": "cs", "21": "hu", "22": "ro", "23": "bg", "24": "hr",
            "25": "fi", "26": "no", "27": "sv", "28": "da", "29": "el", "30": "he"
        }
        
        if choice in language_map:
            new_language = language_map[choice]
            settings["language"] = new_language
            
            try:
                with open('file manager/data.json', 'w') as f:
                    json.dump(settings, f, indent=4)
                self.current_language = new_language  # Update current language
                print(f"✅ {self.get_text('language_changed')} {new_language}")
            except Exception as e:
                print(f"❌ Error saving settings: {e}")
        elif choice == "31":
            print(f"❌ {self.get_text('language_change_cancelled')}")
        else:
            print(f"❌ {self.get_text('invalid_choice')}")
            
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        
    def display_preferences(self):
        """Configure display preferences"""
        import json
        
        try:
            with open('file manager/data.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {"show_hidden": False, "sort_by": "name"}
        
        while True:
            self.clear_screen()
            self.display_logo()
            self.load_language_settings()  # Load current language
            print(f"🎨 {self.get_text('display_preferences_title')}")
            print(f"1. {self.get_text('show_hidden_files')}")
            print(f"2. {self.get_text('sort_order')}")
            print(f"3. {self.get_text('back_to_settings')}")
            
            choice = input(f"\n🎯 {self.get_text('choose_option')} (1-3): ").strip()
            
            if choice == "1":
                current = self.get_text("yes") if settings.get("show_hidden", False) else self.get_text("no")
                print(f"\n{self.get_text('current_setting')}: {self.get_text('show_hidden_files')} = {current}")
                toggle = input(f"{self.get_text('toggle')} (y/N): ").strip().lower()
                if toggle == 'y':
                    settings["show_hidden"] = not settings.get("show_hidden", False)
                    new_value = self.get_text("yes") if settings['show_hidden'] else self.get_text("no")
                    print(f"✅ {self.get_text('show_hidden_files')}: {new_value}")
            elif choice == "2":
                print(f"\n📊 {self.get_text('sort_options')}:")
                print(f"1. {self.get_text('by_name')}")
                print(f"2. {self.get_text('by_size')}")
                print(f"3. {self.get_text('by_date')}")
                print(f"4. {self.get_text('by_type')}")
                
                sort_choice = input(f"\n🎯 {self.get_text('choose_sort_method')} (1-4): ").strip()
                sort_map = {
                    "1": "name",
                    "2": "size", 
                    "3": "date",
                    "4": "type"
                }
                
                if sort_choice in sort_map:
                    settings["sort_by"] = sort_map[sort_choice]
                    print(f"✅ {self.get_text('sort_order_set')}: {sort_map[sort_choice]}")
                else:
                    print(f"❌ {self.get_text('invalid_choice')}")
            elif choice == "3":
                break
            else:
                print(f"❌ {self.get_text('invalid_choice')}")
                
            # Save settings after each change
            try:
                with open('file manager/data.json', 'w') as f:
                    json.dump(settings, f, indent=4)
            except Exception as e:
                print(f"❌ Error saving settings: {e}")
                
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def view_current_settings(self):
        """View current application settings"""
        import json
        
        try:
            with open('file manager/data.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {}
            
        self.load_language_settings()  # Load current language
        print(f"\n📋 {self.get_text('current_settings')}:")
        print("─" * 40)
        
        language = settings.get("language", "en")
        language_names = {
            "en": "English", "fr": "Français", "es": "Español", "de": "Deutsch",
            "ja": "日本語", "ru": "Русский", "zh": "中文", "ar": "العربية",
            "hi": "हिन्दी", "pt": "Português", "it": "Italiano", "nl": "Nederlands",
            "pl": "Polski", "tr": "Türkçe", "ko": "한국어", "th": "ไทย",
            "vi": "Tiếng Việt", "id": "Bahasa Indonesia", "uk": "Українська",
            "cs": "Čeština", "hu": "Magyar", "ro": "Română", "bg": "Български",
            "hr": "Hrvatski", "fi": "Suomi", "no": "Norsk", "sv": "Svenska",
            "da": "Dansk", "el": "Ελληνικά", "he": "עברית"
        }
        print(f"🌍 {self.get_text('language')}: {language_names.get(language, language)}")
        
        show_hidden = settings.get("show_hidden", False)
        hidden_value = self.get_text("yes") if show_hidden else self.get_text("no")
        print(f"👁️ {self.get_text('show_hidden_files')}: {hidden_value}")
        
        sort_by = settings.get("sort_by", "name")
        sort_names = {
            "name": self.get_text("by_name"),
            "size": self.get_text("by_size"),
            "date": self.get_text("by_date"), 
            "type": self.get_text("by_type")
        }
        print(f"📊 {self.get_text('sort_order')}: {sort_names.get(sort_by, sort_by)}")
        
        theme = settings.get("theme", "default")
        print(f"🎨 {self.get_text('theme')}: {theme}")
        
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.load_language_settings()  # Load current language
        confirm = input(f"\n⚠️ {self.get_text('reset_confirm')} (y/N): ").strip().lower()
        
        if confirm == 'y':
            default_settings = {
                "language": "en",
                "theme": "default", 
                "show_hidden": False,
                "sort_by": "name"
            }
            
            try:
                with open('file manager/data.json', 'w') as f:
                    import json
                    json.dump(default_settings, f, indent=4)
                self.current_language = "en"  # Reset current language
                print(f"✅ {self.get_text('settings_reset')}")
            except Exception as e:
                print(f"❌ Error resetting settings: {e}")
        else:
            print(f"❌ {self.get_text('settings_reset_cancelled')}")
            
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
    def manual_directory_input(self):
        """Manual directory input"""
        print("\n📂 Enter directory name (or '..' for parent directory):")
        choice = input("> ").strip()
        
        if not choice:
            return
            
        if choice == "..":
            new_path = self.current_dir.parent
        else:
            new_path = self.current_dir / choice
            
        try:
            if new_path.exists() and new_path.is_dir():
                self.current_dir = new_path.resolve()
                print(f"✅ Changed to: {self.current_dir}")
            else:
                print(f"❌ Directory '{choice}' does not exist.")
        except PermissionError:
            print(f"🚫 {self.get_text('permission_denied')}")
            
    def select_directory_from_list(self):
        """Select directory from numbered list"""
        try:
            directories = [item for item in self.current_dir.iterdir() if item.is_dir()]
            
            if not directories:
                print("📭 No directories in current location.")
                return
                
            print("\n📁 Available directories:")
            for i, directory in enumerate(directories, 1):
                try:
                    stat = directory.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    print(f"{i}. 📁 {directory.name:<40} {modified}")
                except PermissionError:
                    print(f"{i}. 📁 {directory.name:<40} 🚫 {self.get_text('access_denied')}")
                    
            choice = int(input(f"\n🎯 {self.get_text('enter_directory_number')} ({self.get_text('cancel')}): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(directories):
                selected_dir = directories[choice - 1]
                try:
                    self.current_dir = selected_dir.resolve()
                    print(f"✅ Changed to: {self.current_dir}")
                except PermissionError:
                    print(f"🚫 {self.get_text('permission_denied')}")
            else:
                print("❌ Invalid directory number.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def go_to_parent_directory(self):
        """Go to parent directory"""
        try:
            parent = self.current_dir.parent
            if parent != self.current_dir:  # Not at root
                self.current_dir = parent
                print(f"✅ Changed to parent directory: {self.current_dir}")
            else:
                print("ℹ️ Already at root directory.")
        except Exception as e:
            print(f"❌ Error accessing parent directory: {e}")
            
    def go_to_home_directory(self):
        """Go to home directory"""
        try:
            home_dir = Path.home()
            self.current_dir = home_dir
            print(f"✅ Changed to home directory: {self.current_dir}")
        except Exception as e:
            print(f"❌ Error accessing home directory: {e}")
            
    def go_to_root_directory(self):
        """Go to root directory"""
        try:
            root_dir = Path(self.current_dir.anchor)
            self.current_dir = root_dir
            print(f"✅ Changed to root directory: {self.current_dir}")
        except Exception as e:
            print(f"❌ Error accessing root directory: {e}")
            
    def view_file_by_number(self, files):
        """View file by entering its number"""
        try:
            choice = int(input(f"\n👁️ {self.get_text('enter_file_number')} ({self.get_text('cancel')}): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(files):
                file_path = files[choice - 1]
                self.display_file_content(file_path)
            else:
                print("❌ Invalid file number.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def search_and_view_file(self, files):
        """Search for files by name and view them"""
        search_term = input(f"\n🔍 {self.get_text('enter_file_name_search')}: ").strip().lower()
        if not search_term:
            return
            
        matching_files = [f for f in files if search_term in f.name.lower()]
        
        if not matching_files:
            print(f"❌ No files found matching '{search_term}'.")
            return
            
        print(f"\n🔍 Found {len(matching_files)} matching file(s):")
        for i, file in enumerate(matching_files, 1):
            file_emoji = self.get_file_emoji(file.suffix)
            print(f"{i}. {file_emoji} {file.name}")
            
        try:
            choice = int(input(f"\n👁️ {self.get_text('enter_file_number')} ({self.get_text('cancel')}): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(matching_files):
                file_path = matching_files[choice - 1]
                self.display_file_content(file_path)
            else:
                print("❌ Invalid file number.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def view_text_files_only(self, files):
        """View only text files"""
        text_extensions = ['.txt', '.py', '.md', '.json', '.xml', '.html', '.css', '.js', '.ini', '.cfg', '.conf', '.log']
        text_files = [f for f in files if f.suffix.lower() in text_extensions]
        
        if not text_files:
            print("📭 No text files found in current directory.")
            return
            
        print(f"\n📝 Text files ({len(text_files)} found):")
        for i, file in enumerate(text_files, 1):
            file_emoji = self.get_file_emoji(file.suffix)
            print(f"{i}. {file_emoji} {file.name}")
            
        try:
            choice = int(input(f"\n👁️ {self.get_text('enter_file_number')} ({self.get_text('cancel')}): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(text_files):
                file_path = text_files[choice - 1]
                self.display_file_content(file_path)
            else:
                print("❌ Invalid file number.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def display_file_content(self, file_path):
        """Display content of a file with integrated editor"""
        try:
            # Check if file is likely a text file
            text_extensions = ['.txt', '.py', '.md', '.json', '.xml', '.html', '.css', '.js', '.ini', '.cfg', '.conf', '.log', '.csv', '.rtf', '.yml', '.yaml', '.toml', '.sql', '.sh', '.bat', '.ps1']

            if file_path.suffix.lower() in text_extensions:
                # Special handling for Markdown files
                if file_path.suffix.lower() == '.md':
                    self.display_markdown_file(file_path)
                else:
                    self.open_editor(file_path)
            else:
                print(f"⚠️ File '{file_path.name}' appears to be binary. Cannot display content.")
        except UnicodeDecodeError:
            print(f"⚠️ File '{file_path.name}' contains non-text content. Cannot display.")
        except PermissionError:
            print("🚫 Permission denied to read this file.")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    def display_markdown_file(self, file_path):
        """Display Markdown file using Rich library for better terminal rendering"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            if not markdown_content.strip():
                print("📭 Markdown file is empty.")
                input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
                return
            
            # Use Rich library if available
            if HAS_RICH:
                self.display_markdown_with_rich(markdown_content, file_path.name)
            else:
                # Fallback to custom HTML conversion
                html_content = self.convert_markdown_to_html(markdown_content)
                self.display_html_content(html_content, file_path.name)
            
        except Exception as e:
            print(f"❌ Error reading Markdown file: {e}")
            # Fallback to regular editor
            self.open_editor(file_path)
    
    def display_markdown_with_rich(self, markdown_content, filename):
        """Display Markdown using Rich library for beautiful terminal rendering"""
        console = Console()
        
        # Clear screen
        self.clear_screen()
        
        # Display header
        console.print("=" * 80, style="bold blue")
        console.print(f"📄 {filename} - Markdown Viewer (Rich)", style="bold green")
        console.print("=" * 80, style="bold blue")
        console.print()
        
        # Create Markdown object
        markdown = Markdown(markdown_content)
        
        # Display the markdown with Rich
        console.print(markdown)
        
        console.print()
        console.print("-" * 80, style="dim")
        console.print("⌨️ Controls: Q Quit | E Edit Mode | Any key to continue", style="bold yellow")
        
        # Wait for user input
        key = self.get_key()
        
        if key == 'E':
            # Switch to edit mode
            console.print("\n🔄 Switching to edit mode...", style="bold yellow")
            input(f"⏸️ {self.get_text('press_enter_continue')}...")
            return
        elif key == 'Q' or key == 'ESCAPE':
            return
        else:
            # Continue with any other key
            input(f"⏸️ {self.get_text('press_enter_continue')}...")
    
    def convert_markdown_to_html(self, markdown_text):
        """Convert Markdown text to HTML with enhanced formatting for console display"""
        html = markdown_text
        
        # Headers with enhanced styling
        html = re.sub(r'^### (.*?)$', r'<h3 style="color: #4CAF50; margin: 10px 0; font-weight: bold;">\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2 style="color: #2196F3; margin: 15px 0; font-weight: bold;">\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1 style="color: #FF9800; margin: 20px 0; font-weight: bold; text-transform: uppercase;">\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and Italic with enhanced styling
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #E91E63; font-weight: bold;">\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em style="color: #9C27B0; font-style: italic;">\1</em>', html)
        
        # Code blocks with enhanced styling
        html = re.sub(r'```(.*?)```', r'<pre style="background: #f5f5f5; padding: 10px; border-left: 4px solid #4CAF50; margin: 10px 0; overflow-x: auto; font-family: monospace;"><code style="font-family: monospace;">\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.*?)`', r'<code style="background: #f0f0f0; padding: 2px 4px; border-radius: 3px; color: #D32F2F; font-family: monospace;">\1</code>', html)
        
        # Links with enhanced styling
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #1976D2; text-decoration: underline;">\1</a>', html)
        
        # Lists with enhanced styling
        html = re.sub(r'^\- (.*?)$', r'<li style="margin: 5px 0; color: #424242; list-style-type: disc;">\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^(\d+)\. (.*?)$', r'<li style="margin: 5px 0; color: #424242; list-style-type: decimal;">\2</li>', html, flags=re.MULTILINE)
        
        # Blockquotes with enhanced styling
        html = re.sub(r'^> (.*?)$', r'<blockquote style="border-left: 4px solid #FFC107; padding-left: 15px; margin: 10px 0; color: #666; font-style: italic; background: #f9f9f9;">\1</blockquote>', html, flags=re.MULTILINE)
        
        # Horizontal rules with enhanced styling
        html = re.sub(r'^---$', r'<hr style="border: none; border-top: 2px solid #E0E0E0; margin: 20px 0;">', html, flags=re.MULTILINE)
        
        # Tables (basic support)
        html = re.sub(r'^\|(.+)\|$', r'<table style="border-collapse: collapse; width: 100%;"><tr style="border-bottom: 1px solid #ddd;">\1</tr></table>', html, flags=re.MULTILINE)
        
        # Convert line breaks to <br>
        html = html.replace('\n', '<br>\n')
        
        # Wrap in HTML structure
        html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 100%;">
            {html}
        </div>
        """
        
        return html
    
    def display_html_content(self, html_content, filename):
        """Display HTML content in a formatted way"""
        self.clear_screen()
        
        print("=" * 80)
        print(f"📄 {filename} - Markdown Preview")
        print("=" * 80)
        print()
        
        # Process HTML content to extract formatted lines
        formatted_lines = self.process_html_to_lines(html_content)
        current_line = 0
        total_lines = len(formatted_lines)
        
        while current_line < total_lines:
            # Display current page
            for i in range(current_line, min(current_line + 20, total_lines)):
                line = formatted_lines[i]
                if line.strip():
                    print(line)
                else:
                    print()
            
            print()
            print("-" * 80)
            print(f"📄 Line {current_line + 1}-{min(current_line + 20, total_lines)} of {total_lines}")
            print("⌨️ Controls: ↑↓ Navigate | Q Quit | E Edit Mode")
            
            # Get user input
            key = self.get_key()
            
            if key == 'UP':
                current_line = max(0, current_line - 1)
            elif key == 'DOWN':
                current_line = min(total_lines - 20, current_line + 1)
            elif key == 'PAGE_UP':
                current_line = max(0, current_line - 20)
            elif key == 'PAGE_DOWN':
                current_line = min(total_lines - 20, current_line + 20)
            elif key == 'Q' or key == 'ESCAPE':
                break
            elif key == 'E':
                # Switch to edit mode
                print("\n🔄 Switching to edit mode...")
                input(f"⏸️ {self.get_text('press_enter_continue')}...")
                return
            
            self.clear_screen()
    
    def process_html_to_lines(self, html_content):
        """Process HTML content and convert to formatted lines"""
        import re
        
        lines = []
        
        # Split by <br> tags first
        html_lines = html_content.split('<br>')
        
        for html_line in html_lines:
            html_line = html_line.strip()
            if not html_line:
                lines.append("")
                continue
            
            # Process different HTML elements
            if '<h1' in html_line:
                # H1 title
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"╔══════════════════════════════════════════════════════════════════════════════╗")
                lines.append(f"║ {text.upper():^78} ║")
                lines.append(f"╚══════════════════════════════════════════════════════════════════════════════╝")
                
            elif '<h2' in html_line:
                # H2 title
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"┌──────────────────────────────────────────────────────────────────────────────┐")
                lines.append(f"│ {text:^78} │")
                lines.append(f"└──────────────────────────────────────────────────────────────────────────────┘")
                
            elif '<h3' in html_line:
                # H3 title
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"┌─ {text} {'─' * (75 - len(text))}┐")
                
            elif '<strong' in html_line:
                # Bold text
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"█ {text} █")
                
            elif '<em' in html_line:
                # Italic text
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"▸ {text} ◂")
                
            elif '<code' in html_line and '<pre' not in html_line:
                # Inline code
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"┌─ CODE ─┐")
                lines.append(f"│ {text} │")
                lines.append(f"└────────┘")
                
            elif '<pre' in html_line:
                # Code block
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"┌─ CODE BLOCK ─┐")
                lines.append(f"│ {text} │")
                lines.append(f"└──────────────┘")
                
            elif '<blockquote' in html_line:
                # Blockquote
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"┌─ QUOTE ─{'─' * (70 - len(text))}┐")
                lines.append(f"│ {text} │")
                lines.append(f"└{'─' * 78}┘")
                
            elif '<li' in html_line:
                # List item
                text = re.sub(r'<[^>]+>', '', html_line)
                lines.append(f"├─ {text}")
                
            elif '<hr' in html_line:
                # Horizontal rule
                lines.append("─" * 80)
                
            else:
                # Regular text
                text = re.sub(r'<[^>]+>', '', html_line)
                if text.strip():
                    lines.append(text)
                else:
                    lines.append("")
        
        return lines
    
    def strip_html_tags(self, html_text):
        """Strip HTML tags while preserving formatting with special characters and colors"""
        import re
        
        # Store original HTML for pattern detection
        original_html = html_text
        
        # Remove HTML tags but keep content
        text = re.sub(r'<[^>]+>', '', html_text)
        
        # Add special characters and formatting based on HTML structure
        if 'style=' in original_html:
            if 'h1' in original_html:
                # H1: Large title with special characters
                text = f"╔══════════════════════════════════════════════════════════════════════════════╗\n║ {text.upper():^78} ║\n╚══════════════════════════════════════════════════════════════════════════════╝"
            elif 'h2' in original_html:
                # H2: Medium title with special characters
                text = f"┌──────────────────────────────────────────────────────────────────────────────┐\n│ {text:^78} │\n└──────────────────────────────────────────────────────────────────────────────┘"
            elif 'h3' in original_html:
                # H3: Small title with special characters
                text = f"┌─ {text} {'─' * (75 - len(text))}┐"
            elif 'strong' in original_html or 'font-weight: bold' in original_html:
                # Bold text with special characters
                text = f"█ {text} █"
            elif 'em' in original_html or 'font-style: italic' in original_html:
                # Italic text with special characters
                text = f"▸ {text} ◂"
            elif 'code' in original_html:
                # Code with special characters
                text = f"┌─ CODE ─┐\n│ {text} │\n└────────┘"
            elif 'blockquote' in original_html:
                # Blockquote with special characters
                text = f"┌─ QUOTE ─{'─' * (70 - len(text))}┐\n│ {text} │\n└{'─' * 78}┘"
            elif 'li' in original_html:
                # List item with special characters
                text = f"├─ {text}"
            elif 'hr' in original_html:
                # Horizontal rule with special characters
                text = "─" * 80
        
        return text
            
    def open_editor(self, file_path):
        """Open file in integrated editor"""
        try:
            from file_manager.editor import SimpleEditor
            
            # Create editor with translations
            editor = SimpleEditor(file_path, self.translations.get(self.current_language, {}))
            
            # Run editor
            editor.run()
            
        except ImportError:
            print("❌ Editor module not found. Falling back to simple viewer.")
            self.nano_like_viewer(file_path)
        except Exception as e:
            print(f"❌ Error opening editor: {e}")
            self.nano_like_viewer(file_path)
            
    def nano_like_viewer(self, file_path):
        """Nano-like file viewer with navigation and search"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
            
        if not lines:
            print("📭 File is empty.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            return
            
        # Viewer state
        current_line = 0
        terminal_rows, terminal_cols = self.get_terminal_size()
        lines_per_page = max(5, terminal_rows - 8)  # Reserve space for header and footer
        search_term = ""
        search_results = []
        search_index = 0
        edit_mode = False
        modified_lines = {}  # Store modified lines
        file_modified = False
        editing_line = False
        current_edit_line = 0
        cursor_position = 0
        insert_mode = True
        editing_mode = "single"  # "single" or "multi"
        
        while True:
            self.clear_screen()
            
            # Get current terminal size (in case it changed)
            terminal_rows, terminal_cols = self.get_terminal_size()
            lines_per_page = max(5, terminal_rows - 8)
            
            # Header
            print("═" * terminal_cols)
            if editing_line:
                mode_text = f"✏️ {self.get_text('editing_line')} {current_edit_line + 1}"
                insert_text = f" | {self.get_text('insert_mode')}" if insert_mode else f" | {self.get_text('overwrite_mode')}"
                multi_text = f" | {self.get_text('new_line')}" if editing_mode == "multi" else ""
                print(f"{mode_text}{insert_text}{multi_text} 📖 {file_path.name} - {len(lines)} lines")
                print(f"💡 {self.get_text('press_escape_to_finish')}")
            else:
                mode_text = f"✏️ {self.get_text('edit_mode')}" if edit_mode else f"👁️ {self.get_text('view_mode')}"
                modified_text = f" | 🔴 {self.get_text('file_modified')}" if file_modified else ""
                print(f"{mode_text} 📖 {file_path.name} - {len(lines)} lines{modified_text}")
                if search_term and search_results:
                    print(f"🔍 Search: '{search_term}' ({search_index + 1}/{len(search_results)} results)")
                elif search_term:
                    print(f"🔍 Search: '{search_term}' (0 results)")
            print("═" * terminal_cols)
            
            # Calculate how many lines we can display
            # Include modified lines in the count
            total_lines = len(lines) + len([i for i in modified_lines.keys() if i >= len(lines)])
            available_lines = terminal_rows - 6  # Reserve space for header (3) and footer (3)
            lines_to_show = min(available_lines, total_lines)
            
            # Display current page
            start_line = max(0, current_line - lines_to_show // 2)
            end_line = min(total_lines, start_line + lines_to_show)
            
            # Fill the available space with lines
            lines_displayed = 0
            for i in range(start_line, end_line):
                if lines_displayed >= available_lines:
                    break
                    
                line_num = i + 1
                
                # Use modified content if available
                if i in modified_lines:
                    line_content = modified_lines[i].rstrip('\n\r')
                elif i < len(lines):
                    line_content = lines[i].rstrip('\n\r')
                else:
                    line_content = ""  # New line
                
                # Truncate line if too long for terminal
                max_line_width = terminal_cols - 12  # Reserve space for line number, prefix, and modification indicator
                if len(line_content) > max_line_width:
                    line_content = line_content[:max_line_width-3] + "..."
                
                # Add modification indicator
                mod_indicator = " *" if i in modified_lines else "  "
                
                # Handle editing line display
                if editing_line and i == current_edit_line:
                    # Show cursor in editing line
                    cursor_char = "█" if insert_mode else "▌"
                    if cursor_position < len(line_content):
                        display_content = (line_content[:cursor_position] + 
                                         cursor_char + 
                                         line_content[cursor_position:])
                    else:
                        display_content = line_content + cursor_char
                    
                    # Truncate if too long
                    max_line_width = terminal_cols - 12
                    if len(display_content) > max_line_width:
                        display_content = display_content[:max_line_width-3] + "..."
                    
                    print(f"▶️ {line_num:4d}:{mod_indicator} {display_content}")
                else:
                    # Highlight current line
                    if i == current_line:
                        print(f"▶️ {line_num:4d}:{mod_indicator} {line_content}")
                    else:
                        print(f"   {line_num:4d}:{mod_indicator} {line_content}")
                lines_displayed += 1
            
            # Fill remaining space with empty lines to push controls to bottom
            remaining_lines = available_lines - lines_displayed
            for _ in range(remaining_lines):
                print()
                    
            # Footer with controls (always at bottom)
            print("═" * terminal_cols)
            if editing_line:
                if editing_mode == "multi":
                    controls_text = f"⌨️ {self.get_text('controls_editing')}: {self.get_text('controls_move_cursor')} | {self.get_text('controls_lines')} | {self.get_text('controls_enter_new_line')} | {self.get_text('controls_insert_delete')} | {self.get_text('controls_finish')} | {self.get_text('controls_ctrl_s_save')} | {self.get_text('controls_ctrl_d_discard')}"
                else:
                    controls_text = f"⌨️ {self.get_text('controls_editing')}: {self.get_text('controls_move_cursor')} | {self.get_text('controls_insert_delete')} | {self.get_text('controls_finish')} | {self.get_text('controls_ctrl_s_save')} | {self.get_text('controls_ctrl_d_discard')}"
            elif edit_mode:
                controls_text = f"⌨️ Controls: {self.get_text('controls_navigate')} | {self.get_text('controls_edit_line')} | {self.get_text('controls_multi_line')} | {self.get_text('controls_save')} | {self.get_text('controls_discard')} | {self.get_text('controls_search')} | {self.get_text('controls_resize')} | {self.get_text('controls_quit')}"
            else:
                controls_text = f"⌨️ Controls: {self.get_text('controls_navigate')} | {self.get_text('controls_edit_mode')} | {self.get_text('controls_search')} | {self.get_text('controls_next')} | {self.get_text('controls_prev')} | {self.get_text('controls_resize')} | {self.get_text('controls_quit')}"
            
            if len(controls_text) > terminal_cols:
                if editing_line:
                    controls_text = f"⌨️ {self.get_text('controls_editing')}: {self.get_text('controls_move_cursor')} | {self.get_text('controls_finish')} | {self.get_text('controls_ctrl_s_save')}"
                elif edit_mode:
                    controls_text = f"⌨️ Controls: {self.get_text('controls_navigate')} | {self.get_text('controls_edit')} | {self.get_text('controls_save')} | {self.get_text('controls_discard')} | {self.get_text('controls_quit')}"
                else:
                    controls_text = f"⌨️ Controls: {self.get_text('controls_navigate')} | {self.get_text('controls_edit')} | {self.get_text('controls_search')} | {self.get_text('controls_quit')}"
            print(controls_text)
            
            # Handle key input
            key = self.get_key()
            
            # Handle editing mode
            if editing_line:
                self.handle_editing_input(key, lines, modified_lines, current_edit_line, cursor_position, insert_mode)
                # Update cursor position and insert mode
                cursor_position = self.cursor_position
                insert_mode = self.insert_mode
                if not self.editing_line:
                    editing_line = False
                    file_modified = True
                continue
            
            if key == 'UP':
                current_line = max(0, current_line - 1)
            elif key == 'DOWN':
                current_line = min(len(lines) - 1, current_line + 1)
            elif key == 'PAGE_UP' or key == 'LEFT':  # Use LEFT as Page Up
                current_line = max(0, current_line - lines_per_page)
            elif key == 'PAGE_DOWN' or key == 'RIGHT':  # Use RIGHT as Page Down
                current_line = min(len(lines) - 1, current_line + lines_per_page)
            elif key == 'HOME':
                current_line = 0
            elif key == 'END':
                current_line = len(lines) - 1
            elif key == '/':
                search_results, search_index, search_term = self.search_in_file(lines, current_line)
                # After search, update current line to the found result
                if search_results:
                    current_line = search_results[search_index]
            elif key == 'N':
                if search_results and search_index < len(search_results) - 1:
                    search_index += 1
                    current_line = search_results[search_index]
                elif search_results:
                    # Wrap to first result if at end
                    search_index = 0
                    current_line = search_results[search_index]
            elif key == 'P':
                if search_results and search_index > 0:
                    search_index -= 1
                    current_line = search_results[search_index]
                elif search_results:
                    # Wrap to last result if at beginning
                    search_index = len(search_results) - 1
                    current_line = search_results[search_index]
            elif key == 'Q' or key == 'ESCAPE':
                # Check if there are unsaved changes
                if file_modified:
                    confirm = input(f"\n⚠️ {self.get_text('confirm_discard')} (y/N): ").strip().lower()
                    if confirm == 'y':
                        break
                else:
                    break
            elif key == 'ENTER':
                if edit_mode:
                    # Edit current line
                    self.edit_line(lines, modified_lines, current_line)
                    file_modified = True
                else:
                    # Show line details
                    self.show_line_details(lines, current_line)
            elif key == 'E':
                if edit_mode:
                    # Start inline editing
                    editing_line = True
                    current_edit_line = current_line
                    cursor_position = 0
                    insert_mode = True
                else:
                    # Switch to edit mode
                    edit_mode = True
            elif key == 'M':
                if edit_mode:
                    # Toggle between single and multi-line editing
                    editing_mode = "multi" if editing_mode == "single" else "single"
            elif key == 'S':
                if edit_mode and file_modified:
                    # Save changes
                    self.save_file_changes(file_path, lines, modified_lines)
                    file_modified = False
                    modified_lines.clear()
            elif key == 'D':
                if edit_mode and file_modified:
                    # Discard changes
                    confirm = input(f"\n⚠️ {self.get_text('confirm_discard')} (y/N): ").strip().lower()
                    if confirm == 'y':
                        modified_lines.clear()
                        file_modified = False
                        edit_mode = False
            elif key == 'R':
                # Refresh/Resize - recalculate terminal size
                terminal_rows, terminal_cols = self.get_terminal_size()
                lines_per_page = max(5, terminal_rows - 8)
                # Ensure current line is still valid
                if current_line >= len(lines):
                    current_line = len(lines) - 1
                
    def search_in_file(self, lines, current_line):
        """Search for text in file and return search results"""
        search_term = input(f"\n🔍 {self.get_text('enter_search_term')}: ").strip()
        if not search_term:
            return [], 0, ""
            
        search_results = []
        
        for i, line in enumerate(lines):
            if search_term.lower() in line.lower():
                search_results.append(i)
                
        if search_results:
            print(f"✅ Found {len(search_results)} matches for '{search_term}'")
            # Find the best starting position
            search_index = 0
            # If current line is in results, start from there
            if current_line in search_results:
                search_index = search_results.index(current_line)
            # Otherwise, find the first result after current line
            else:
                for i, result_line in enumerate(search_results):
                    if result_line > current_line:
                        search_index = i
                        break
        else:
            print(f"❌ No matches found for '{search_term}'")
            search_index = 0
            
        input("\n⏸️ Press Enter to continue...")
        return search_results, search_index, search_term
        
    def show_line_details(self, lines, line_index):
        """Show detailed information about a line"""
        if 0 <= line_index < len(lines):
            line = lines[line_index]
            print(f"\n📋 Line {line_index + 1} Details:")
            print(f"Length: {len(line)} characters")
            print(f"Content: {repr(line)}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def edit_line(self, lines, modified_lines, line_index):
        """Edit a specific line"""
        if 0 <= line_index < len(lines):
            current_content = modified_lines.get(line_index, lines[line_index]).rstrip('\n\r')
            print(f"\n✏️ {self.get_text('enter_new_content')} {line_index + 1}:")
            print(f"Current: {current_content}")
            new_content = input(f"{self.get_text('enter_new_content')}: ").strip()
            
            if new_content != current_content:
                modified_lines[line_index] = new_content + '\n'
                print(f"✅ Line {line_index + 1} modified")
            else:
                print(f"ℹ️ {self.get_text('no_changes_made')}")
                
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def save_file_changes(self, file_path, original_lines, modified_lines):
        """Save changes to file"""
        try:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                for line in original_lines:
                    f.write(line)
            
            # Write modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                for i, line in enumerate(original_lines):
                    if i in modified_lines:
                        f.write(modified_lines[i])
                    else:
                        f.write(line)
            
            print(f"✅ {self.get_text('changes_saved')}")
            print(f"📁 Backup created: {backup_path.name}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def handle_editing_input(self, key, lines, modified_lines, line_index, cursor_pos, insert_mode):
        """Handle input during inline editing"""
        # Get current line content
        if line_index in modified_lines:
            current_content = modified_lines[line_index].rstrip('\n\r')
        else:
            current_content = lines[line_index].rstrip('\n\r')
        
        # Initialize instance variables
        self.cursor_position = cursor_pos
        self.insert_mode = insert_mode
        self.editing_line = True
        self.editing_mode = "multi"  # Enable multi-line editing
        
        if key == 'ESCAPE':
            # Finish editing
            self.editing_line = False
        elif key == 'LEFT':
            # Move cursor left
            self.cursor_position = max(0, self.cursor_position - 1)
        elif key == 'RIGHT':
            # Move cursor right
            self.cursor_position = min(len(current_content), self.cursor_position + 1)
        elif key == 'HOME':
            # Move to beginning of line
            self.cursor_position = 0
        elif key == 'END':
            # Move to end of line
            self.cursor_position = len(current_content)
        elif key == 'UP':
            # Move to previous line (if exists)
            if line_index > 0:
                self.current_edit_line = line_index - 1
                # Get the previous line content
                if line_index - 1 in modified_lines:
                    prev_content = modified_lines[line_index - 1].rstrip('\n\r')
                else:
                    prev_content = lines[line_index - 1].rstrip('\n\r')
                # Set cursor position to end of previous line or current position
                self.cursor_position = min(self.cursor_position, len(prev_content))
        elif key == 'DOWN':
            # Move to next line (if exists)
            if line_index < len(lines) - 1:
                self.current_edit_line = line_index + 1
                # Get the next line content
                if line_index + 1 in modified_lines:
                    next_content = modified_lines[line_index + 1].rstrip('\n\r')
                else:
                    next_content = lines[line_index + 1].rstrip('\n\r')
                # Set cursor position to end of next line or current position
                self.cursor_position = min(self.cursor_position, len(next_content))
        elif key == 'INSERT':
            # Toggle insert/overwrite mode
            self.insert_mode = not self.insert_mode
        elif key == 'BACKSPACE':
            # Delete character before cursor
            if self.cursor_position > 0:
                new_content = (current_content[:self.cursor_position-1] + 
                             current_content[self.cursor_position:])
                modified_lines[line_index] = new_content + '\n'
                self.cursor_position -= 1
        elif key == 'DELETE':
            # Delete character at cursor
            if self.cursor_position < len(current_content):
                new_content = (current_content[:self.cursor_position] + 
                             current_content[self.cursor_position+1:])
                modified_lines[line_index] = new_content + '\n'
        elif key == 'CTRL_S':
            # Save changes
            self.editing_line = False
        elif key == 'CTRL_D':
            # Discard changes
            if line_index in modified_lines:
                del modified_lines[line_index]
            self.editing_line = False
        elif key == 'ENTER':
            # Create new line
            if self.cursor_position < len(current_content):
                # Split line at cursor position
                first_part = current_content[:self.cursor_position]
                second_part = current_content[self.cursor_position:]
                
                # Update current line with first part
                modified_lines[line_index] = first_part + '\n'
                
                # Create new line with second part
                # We need to add this as a new line after the current one
                new_line_content = second_part + '\n'
                
                # Store the new line content temporarily
                self.new_line_content = new_line_content
                self.new_line_index = line_index + 1
                
                # Move to new line
                self.current_edit_line = line_index + 1
                self.cursor_position = 0
            else:
                # Insert empty line after current line
                self.new_line_content = '\n'
                self.new_line_index = line_index + 1
                
                # Move to new line
                self.current_edit_line = line_index + 1
                self.cursor_position = 0
        elif len(key) == 1 and key.isprintable():
            # Insert character
            if self.insert_mode:
                # Insert mode
                new_content = (current_content[:self.cursor_position] + 
                             key + 
                             current_content[self.cursor_position:])
            else:
                # Overwrite mode
                if self.cursor_position < len(current_content):
                    new_content = (current_content[:self.cursor_position] + 
                                 key + 
                                 current_content[self.cursor_position+1:])
                else:
                    new_content = current_content + key
            
            modified_lines[line_index] = new_content + '\n'
            self.cursor_position += 1
            
    def quick_navigate_to_folder(self):
        """Quickly navigate to a folder by selecting its number"""
        try:
            directories = [item for item in self.current_dir.iterdir() if item.is_dir()]
            
            if not directories:
                print("📭 No directories in current location.")
                return
                
            print("\n📁 Available directories:")
            for i, directory in enumerate(directories, 1):
                try:
                    stat = directory.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    print(f"{i}. 📁 {directory.name:<40} {modified}")
                except PermissionError:
                    print(f"{i}. 📁 {directory.name:<40} 🚫 {self.get_text('access_denied')}")
                    
            choice = int(input(f"\n🎯 {self.get_text('enter_directory_number')} ({self.get_text('cancel')}): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(directories):
                selected_dir = directories[choice - 1]
                try:
                    self.current_dir = selected_dir.resolve()
                    print(f"✅ Changed to: {self.current_dir}")
                except PermissionError:
                    print(f"🚫 {self.get_text('permission_denied')}")
            else:
                print("❌ Invalid directory number.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def quick_view_file(self):
        """Quickly view a file by selecting its number"""
        try:
            files = [item for item in self.current_dir.iterdir() if item.is_file()]
            
            if not files:
                print("📭 No files in current directory.")
                return
                
            print("\n📄 Available files:")
            for i, file in enumerate(files, 1):
                try:
                    stat = file.stat()
                    size = self.format_size(stat.st_size)
                    file_emoji = self.get_file_emoji(file.suffix)
                    print(f"{i}. {file_emoji} {file.name:<40} {size}")
                except PermissionError:
                    file_emoji = self.get_file_emoji(file.suffix)
                    print(f"{i}. {file_emoji} {file.name:<40} 🚫 {self.get_text('access_denied')}")
                    
            choice = int(input(f"\n👁️ {self.get_text('enter_file_number')} ({self.get_text('cancel')}): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(files):
                file_path = files[choice - 1]
                self.display_file_content(file_path)
            else:
                print("❌ Invalid file number.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def navigation(self):
        """Interactive navigation with arrow keys - Main navigation mode"""
        self.menu_mode = True
        self.selected_index = 0
        
        while self.menu_mode:
            self.clear_screen()
            self.display_logo()
            self.display_current_path()
            
            # Get directory contents
            try:
                items = list(self.current_dir.iterdir())
                
                # Sort items (directories first, then files)
                directories = [item for item in items if item.is_dir()]
                files = [item for item in items if item.is_file()]
                directories.sort(key=lambda x: x.name.lower())
                files.sort(key=lambda x: x.name.lower())
                
                # Add special navigation items at the beginning
                self.items = []
                
                # Add parent directory if not at root
                if self.current_dir.parent != self.current_dir:
                    self.items.append(Path(".."))
                
                # Add root directory if not already at root
                if self.current_dir != Path(self.current_dir.anchor):
                    self.items.append(Path("..."))
                
                # Add regular directories and files
                self.items.extend(directories)
                self.items.extend(files)
                
                # Apply filter if active
                if self.filter_active:
                    self.all_items = self.items.copy()
                    self.items = self.filter_items(self.items, self.filter_pattern)
                
                if not self.items:
                    # Fill space to push controls to bottom
                    terminal_rows, terminal_cols = self.get_terminal_size()
                    available_lines = terminal_rows - 6  # Reserve space for message and controls
                    
                    if self.filter_active:
                        filter_display = self.get_filter_display_name()
                        print(f"📭 No items match filter: {filter_display}")
                    else:
                        print(f"📭 {self.get_text('directory_is_empty')}")
                    
                    # Fill remaining space
                    for _ in range(available_lines - 1):
                        print()
                    
                    print(f"⌨️ Controls: {self.get_text('controls_navigate')} | {self.get_text('controls_select')} | {self.get_text('controls_back')} | {self.get_text('controls_home')} | {self.get_text('controls_root')} | {self.get_text('controls_parent')} | {self.get_text('controls_filter')}")
                    key = self.get_key()
                    if key == 'ESCAPE':
                        self.menu_mode = False
                    continue
                
                # Ensure selected index is valid
                if self.selected_index >= len(self.items):
                    self.selected_index = 0
                elif self.selected_index < 0:
                    self.selected_index = len(self.items) - 1
                    
                # Get terminal size for display
                terminal_rows, terminal_cols = self.get_terminal_size()
                
                # Calculate available space for items
                available_lines = terminal_rows - 8  # Reserve space for header, title, and controls
                items_to_show = min(available_lines, len(self.items))
                
                # Display header
                print(f"{'📄 Name':<42} {'Type':<10} {'Size':<15} {'Modified'}")
                print("─" * terminal_cols)
                
                # Display items with selection
                items_displayed = 0
                for i, item in enumerate(self.items):
                    if items_displayed >= available_lines:
                        break
                        
                    try:
                        # Handle special navigation items
                        if item.name == "..":
                            prefix = "▶️ " if i == self.selected_index else "⬆️ "
                            print(f"{prefix}{'.. (Parent Directory)':<40} {'[NAV]':<10} {'':<15} {'Navigation'}")
                        elif item.name == "...":
                            prefix = "▶️ " if i == self.selected_index else "🏠 "
                            print(f"{prefix}{'... (Root Directory)':<40} {'[NAV]':<10} {'':<15} {'Navigation'}")
                        elif item.is_dir():
                            stat = item.stat()
                            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                            prefix = "▶️ " if i == self.selected_index else "📁 "
                            print(f"{prefix}{item.name:<40} {'[DIR]':<10} {'':<15} {modified}")
                        else:
                            stat = item.stat()
                            size = self.format_size(stat.st_size)
                            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                            file_emoji = self.get_file_emoji(item.suffix)
                            prefix = "▶️ " if i == self.selected_index else f"{file_emoji} "
                            print(f"{prefix}{item.name:<40} {'[FILE]':<10} {size:<15} {modified}")
                    except PermissionError:
                        prefix = "▶️ " if i == self.selected_index else "📄 "
                        print(f"{prefix}{item.name:<40} {'[FILE]':<10} {'🚫 ' + self.get_text('access_denied'):<15} {'🚫 ' + self.get_text('access_denied')}")
                    
                    items_displayed += 1
                
                # Fill remaining space with empty lines to push controls to bottom
                remaining_lines = available_lines - items_displayed
                for _ in range(remaining_lines):
                    print()
                        
            except PermissionError:
                # Fill space to push controls to bottom
                terminal_rows, terminal_cols = self.get_terminal_size()
                available_lines = terminal_rows - 4  # Reserve space for message and controls
                
                print(f"🚫 {self.get_text('permission_denied')}")
                
                # Fill remaining space
                for _ in range(available_lines - 1):
                    print()
                
                print(f"⌨️ Controls: {self.get_text('controls_back')} | {self.get_text('controls_home')} | {self.get_text('controls_root')} | {self.get_text('controls_parent')} | {self.get_text('controls_filter')}")
                key = self.get_key()
                if key == 'ESCAPE':
                    self.menu_mode = False
                continue
                
            # Display controls
            print("\n⌨️ Controls:")
            if self.filter_active:
                filter_display = self.get_filter_display_name()
                controls_text = f"{self.get_text('controls_navigate')} | {self.get_text('controls_select')} | {self.get_text('controls_back')} | {self.get_text('controls_home')} | {self.get_text('controls_view')} | {self.get_text('controls_delete')} | {self.get_text('controls_copy')} | {self.get_text('controls_move')} | {self.get_text('controls_rename')} | {self.get_text('controls_new_file')} | {self.get_text('controls_new_folder')} | 🔍 {self.get_text('controls_filter_active').format(filter_name=filter_display)}"
            else:
                controls_text = f"{self.get_text('controls_navigate')} | {self.get_text('controls_select')} | {self.get_text('controls_back')} | {self.get_text('controls_home')} | {self.get_text('controls_view')} | {self.get_text('controls_delete')} | {self.get_text('controls_copy')} | {self.get_text('controls_move')} | {self.get_text('controls_rename')} | {self.get_text('controls_new_file')} | {self.get_text('controls_new_folder')} | {self.get_text('controls_filter')}"
            
            # Truncate controls if too long for terminal
            if len(controls_text) > terminal_cols:
                if self.filter_active:
                    controls_text = f"{self.get_text('controls_navigate')} | {self.get_text('controls_select')} | {self.get_text('controls_back')} | {self.get_text('controls_view')} | 🔍 {self.get_text('controls_filter_active').format(filter_name=filter_display)}"
                else:
                    controls_text = f"{self.get_text('controls_navigate')} | {self.get_text('controls_select')} | {self.get_text('controls_back')} | {self.get_text('controls_view')} | {self.get_text('controls_filter')}"
            print(controls_text)
            
            # Handle key input
            key = self.get_key()
            
            if key == 'UP':
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == 'DOWN':
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == 'ENTER':
                self.handle_item_selection()
            elif key == 'ESCAPE':
                self.menu_mode = False
            elif key == 'H':
                self.go_to_home_directory()
            elif key == 'V':
                if self.selected_index < len(self.items):
                    selected_item = self.items[self.selected_index]
                    if selected_item.is_file():
                        self.display_file_content(selected_item)
            elif key == 'D':
                if self.selected_index < len(self.items):
                    selected_item = self.items[self.selected_index]
                    if selected_item.name not in ['..', '...']:
                        self.delete_selected_item(selected_item)
            elif key == 'C':
                if self.selected_index < len(self.items):
                    selected_item = self.items[self.selected_index]
                    if selected_item.name not in ['..', '...']:
                        self.copy_selected_item(selected_item)
            elif key == 'M':
                if self.selected_index < len(self.items):
                    selected_item = self.items[self.selected_index]
                    if selected_item.name not in ['..', '...']:
                        self.move_selected_item(selected_item)
            elif key == 'R':
                if self.selected_index < len(self.items):
                    selected_item = self.items[self.selected_index]
                    if selected_item.name not in ['..', '...']:
                        self.rename_selected_item(selected_item)
            elif key == 'N':
                self.create_file_interactive()
            elif key == 'F':
                self.show_filter_menu()
            elif key == 'G':
                self.create_directory_interactive()
            elif key == 'S':
                # Open settings from navigation (quick access)
                self.settings_menu()
                    
    def handle_item_selection(self):
        """Handle selection of an item"""
        if self.selected_index >= len(self.items):
            return
            
        selected_item = self.items[self.selected_index]
        
        # Handle special navigation items
        if selected_item.name == "..":
            self.go_to_parent_directory()
        elif selected_item.name == "...":
            self.go_to_root_directory()
        elif selected_item.is_dir():
            try:
                self.current_dir = selected_item.resolve()
                self.selected_index = 0
                print(f"✅ Changed to: {self.current_dir}")
            except PermissionError:
                print(f"🚫 {self.get_text('permission_denied')}")
        else:
            # For files, show options
            self.show_file_options(selected_item)
            
    def show_file_options(self, file_path):
        """Show options for a selected file"""
        while True:
            self.clear_screen()
            print(f"📄 File: {file_path.name}")
            print(f"📂 Path: {file_path}")
            print("─" * 60)
            
            try:
                stat = file_path.stat()
                size = self.format_size(stat.st_size)
                modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                print(f"📊 Size: {size}")
                print(f"📅 Modified: {modified}")
            except PermissionError:
                print(f"🚫 {self.get_text('access_denied_to_file')}")
                
            print("\n🎯 File Options:")
            print(f"V - {self.get_text('view_content')}")
            print(f"C - {self.get_text('copy_file')}")
            print(f"M - {self.get_text('move_file')}")
            print(f"R - {self.get_text('rename_file')}")
            print(f"D - {self.get_text('delete_file')}")
            print(f"ESC - {self.get_text('back_to_navigation')}")
            
            key = self.get_key()
            
            if key == 'V':
                self.display_file_content(file_path)
            elif key == 'C':
                self.copy_selected_item(file_path)
            elif key == 'M':
                self.move_selected_item(file_path)
            elif key == 'R':
                self.rename_selected_item(file_path)
            elif key == 'D':
                self.delete_selected_item(file_path)
                break
            elif key == 'ESCAPE':
                break
                
    def copy_selected_item(self, item_path):
        """Copy a selected item"""
        destination = input(f"\n📂 Enter destination path for '{item_path.name}': ").strip()
        if not destination:
            return
            
        destination_path = Path(destination)
        
        try:
            if item_path.is_file():
                shutil.copy2(item_path, destination_path)
                print(f"✅ File copied successfully to {destination_path}")
            elif item_path.is_dir():
                shutil.copytree(item_path, destination_path)
                print(f"✅ Directory copied successfully to {destination_path}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        except Exception as e:
            print(f"❌ Error copying: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def move_selected_item(self, item_path):
        """Move a selected item"""
        destination = input(f"\n📂 Enter destination path for '{item_path.name}': ").strip()
        if not destination:
            return
            
        destination_path = Path(destination)
        
        confirm = input(f"⚠️ Move '{item_path.name}' to '{destination}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return
            
        try:
            shutil.move(str(item_path), str(destination_path))
            print(f"✅ Item moved successfully to {destination_path}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        except Exception as e:
            print(f"❌ Error moving: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def rename_selected_item(self, item_path):
        """Rename a selected item"""
        new_name = input(f"\n✏️ Enter new name for '{item_path.name}': ").strip()
        if not new_name:
            return
            
        new_path = item_path.parent / new_name
        
        try:
            item_path.rename(new_path)
            print(f"✅ '{item_path.name}' renamed to '{new_name}' successfully.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        except Exception as e:
            print(f"❌ Error renaming: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def delete_selected_item(self, item_path):
        """Delete a selected item"""
        confirm = input(f"⚠️ Are you sure you want to delete '{item_path.name}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return
            
        try:
            if item_path.is_file():
                item_path.unlink()
                print(f"✅ File '{item_path.name}' deleted successfully.")
            elif item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"✅ Directory '{item_path.name}' deleted successfully.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        except Exception as e:
            print(f"❌ Error deleting: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def create_file_interactive(self):
        """Create a new file interactively"""
        filename = input("\n📄 Enter new file name: ").strip()
        if not filename:
            return
            
        file_path = self.current_dir / filename
        
        if file_path.exists():
            print(f"⚠️ File '{filename}' already exists.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            return
            
        try:
            file_path.touch()
            print(f"✅ File '{filename}' created successfully.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def create_directory_interactive(self):
        """Create a new directory interactively"""
        dirname = input("\n📁 Enter new directory name: ").strip()
        if not dirname:
            return
            
        dir_path = self.current_dir / dirname
        
        if dir_path.exists():
            print(f"⚠️ Directory '{dirname}' already exists.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            return
            
        try:
            dir_path.mkdir()
            print(f"✅ Directory '{dirname}' created successfully.")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        except Exception as e:
            print(f"❌ Error creating directory: {e}")
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def filter_items(self, items, pattern):
        """Filter items based on pattern"""
        if not pattern:
            return items
            
        filtered = []
        
        for item in items:
            # Handle special navigation items
            if item.name in ['..', '...']:
                filtered.append(item)
            elif pattern == "FILE_ONLY":
                # Show only files
                if item.is_file():
                    filtered.append(item)
            elif pattern == "FOLDER_ONLY":
                # Show only folders
                if item.is_dir():
                    filtered.append(item)
            elif pattern == "TEXT_FILES":
                # Show only text files
                if item.is_file() and item.suffix.lower() in ['.txt', '.py', '.md', '.json', '.xml', '.html', '.css', '.js', '.ini', '.cfg', '.conf', '.log', '.csv', '.rtf']:
                    filtered.append(item)
            elif pattern == "IMAGE_FILES":
                # Show only image files
                if item.is_file() and item.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico', '.webp']:
                    filtered.append(item)
            elif pattern == "ARCHIVE_FILES":
                # Show only archive files
                if item.is_file() and item.suffix.lower() in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tar.gz', '.tar.bz2']:
                    filtered.append(item)
            elif pattern == "EXECUTABLE_FILES":
                # Show only executable files
                if item.is_file() and item.suffix.lower() in ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app', '.bat', '.sh', '.ps1', '.cmd']:
                    filtered.append(item)
            else:
                # Custom pattern matching
                pattern_lower = pattern.lower()
                if pattern_lower in item.name.lower():
                    filtered.append(item)
                
        return filtered
        
    def show_filter_menu(self):
        """Show filter selection menu"""
        while True:
            self.clear_screen()
            self.display_logo()
            self.load_language_settings()  # Load current language
            
            terminal_rows, terminal_cols = self.get_terminal_size()
            
            print(f"🔍 {self.get_text('filter_menu')}")
            print("═" * terminal_cols)
            
            if self.filter_active:
                print(f"📋 {self.get_text('current_setting')}: 🔍 '{self.filter_pattern}'")
                print("─" * terminal_cols)
            
            print(f"1. 📄 {self.get_text('show_files_only')}")
            print(f"2. 📁 {self.get_text('show_folders_only')}")
            print(f"3. 📝 {self.get_text('show_text_files')}")
            print(f"4. 🖼️ {self.get_text('show_images')}")
            print(f"5. 🗜️ {self.get_text('show_archives')}")
            print(f"6. ⚙️ {self.get_text('show_executables')}")
            print(f"7. ✏️ {self.get_text('custom_filter')}")
            print(f"8. 🗑️ {self.get_text('clear_filter')}")
            print(f"9. ⬅️ {self.get_text('back_to_navigation')}")
            
            # Fill remaining space to push input to bottom
            available_lines = terminal_rows - 15  # Reserve space for logo, menu, and input
            for _ in range(available_lines):
                print()
            
            choice = input(f"🎯 {self.get_text('filter_options')} (1-9): ").strip()
            
            if choice == "1":
                self.apply_predefined_filter("files")
            elif choice == "2":
                self.apply_predefined_filter("folders")
            elif choice == "3":
                self.apply_predefined_filter("text")
            elif choice == "4":
                self.apply_predefined_filter("images")
            elif choice == "5":
                self.apply_predefined_filter("archives")
            elif choice == "6":
                self.apply_predefined_filter("executables")
            elif choice == "7":
                self.apply_custom_filter()
            elif choice == "8":
                self.clear_filter()
            elif choice == "9":
                break
            else:
                print(f"❌ {self.get_text('invalid_choice')}")
                input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
                
    def apply_predefined_filter(self, filter_type):
        """Apply predefined filter based on type"""
        if filter_type == "files":
            self.filter_pattern = "FILE_ONLY"
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: {self.get_text('show_files_only')}")
        elif filter_type == "folders":
            self.filter_pattern = "FOLDER_ONLY"
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: {self.get_text('show_folders_only')}")
        elif filter_type == "text":
            self.filter_pattern = "TEXT_FILES"
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: {self.get_text('show_text_files')}")
        elif filter_type == "images":
            self.filter_pattern = "IMAGE_FILES"
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: {self.get_text('show_images')}")
        elif filter_type == "archives":
            self.filter_pattern = "ARCHIVE_FILES"
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: {self.get_text('show_archives')}")
        elif filter_type == "executables":
            self.filter_pattern = "EXECUTABLE_FILES"
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: {self.get_text('show_executables')}")
            
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        
    def apply_custom_filter(self):
        """Apply custom filter pattern"""
        pattern = input(f"\n🔍 {self.get_text('enter_custom_pattern')}: ").strip()
        if pattern:
            self.filter_pattern = pattern
            self.filter_active = True
            print(f"✅ {self.get_text('filter_applied')}: '{pattern}'")
        else:
            print("❌ Filter cancelled.")
            
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        
    def clear_filter(self):
        """Clear current filter"""
        if self.filter_active:
            self.filter_active = False
            self.filter_pattern = ""
            print(f"✅ {self.get_text('filter_cleared')}")
        else:
            print("ℹ️ No active filter to clear.")
            
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
        
    def get_filter_display_name(self):
        """Get display name for current filter"""
        if not self.filter_active:
            return ""
            
        filter_names = {
            "FILE_ONLY": self.get_text('show_files_only'),
            "FOLDER_ONLY": self.get_text('show_folders_only'),
            "TEXT_FILES": self.get_text('show_text_files'),
            "IMAGE_FILES": self.get_text('show_images'),
            "ARCHIVE_FILES": self.get_text('show_archives'),
            "EXECUTABLE_FILES": self.get_text('show_executables')
        }
        
        return filter_names.get(self.filter_pattern, f"'{self.filter_pattern}'")
            
    def run(self):
        """Main application loop"""
        # Start the application directly in navigation mode so the tool
        # can be used programmatically or as a CLI helper without a main menu.
        try:
            # Load language settings before starting
            self.load_language_settings()
            # Enter navigation mode. navigation() manages its own loop and
            # will return when the user exits navigation (ESC in menu).
            self.navigation()
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def main():
    """Entry point of the application"""
    try:
        file_manager = FileManager()
        file_manager.run()
    except Exception as e:
        print(f"❌ Failed to start file manager: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# Programmatic entry point for importing as a module
def start_tool(start_path: str = None):
    """Start the FileManager programmatically.

    Args:
        start_path: Optional path to start in (defaults to current working directory).
    """
    fm = FileManager()
    if start_path:
        try:
            p = Path(start_path)
            if p.exists() and p.is_dir():
                fm.current_dir = p.resolve()
        except Exception:
            pass
    fm.run()
