#!/usr/bin/env python3
"""
Python Console File Manager
A menu-driven file manager for console/terminal use.
"""

import os
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
            return input("Press Enter to continue...")
        
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
            print(f"🔍 Filter active: {filter_display}")
        print("─" * 60)
        
    def list_directory(self):
        """List files and folders in current directory"""
        try:
            items = list(self.current_dir.iterdir())
            if not items:
                print("📭 Directory is empty.")
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
                    print(f"📁 {directory.name:<40} {'[DIR]':<10} {'':<15} {'🚫 Access Denied'}")
            
            # Display files
            for file in files:
                try:
                    stat = file.stat()
                    size = self.format_size(stat.st_size)
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    file_emoji = self.get_file_emoji(file.suffix)
                    print(f"{file_emoji} {file.name:<39} {'[FILE]':<10} {size:<15} {modified}")
                except PermissionError:
                    print(f"📄 {file.name:<39} {'[FILE]':<10} {'🚫 Access Denied':<15} {'🚫 Access Denied'}")
                    
        except PermissionError:
            print("🚫 Permission denied to access this directory.")
            
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
        """Load translation strings for all supported languages"""
        return {
            "en": {
                "main_menu": "MAIN MENU",
                "navigation": "Navigation",
                "settings": "Settings", 
                "exit": "Exit",
                "current_directory": "Current Directory",
                "settings_menu": "Settings Menu",
                "change_language": "Change Language",
                "display_preferences": "Display Preferences",
                "view_current_settings": "View Current Settings",
                "reset_to_defaults": "Reset to Defaults",
                "back_to_main_menu": "Back to Main Menu",
                "available_languages": "Available Languages",
                "cancel": "Cancel",
                "language_changed": "Language changed to",
                "language_change_cancelled": "Language change cancelled",
                "invalid_choice": "Invalid choice",
                "press_enter_continue": "Press Enter to continue",
                "display_preferences_title": "Display Preferences",
                "show_hidden_files": "Show Hidden Files",
                "sort_order": "Sort Order",
                "back_to_settings": "Back to Settings",
                "current_setting": "Current setting",
                "toggle": "Toggle?",
                "sort_options": "Sort Options",
                "by_name": "By Name (alphabetical)",
                "by_size": "By Size",
                "by_date": "By Date Modified",
                "by_type": "By Type",
                "sort_order_set": "Sort order set to",
                "current_settings": "Current Settings",
                "language": "Language",
                "theme": "Theme",
                "reset_confirm": "Are you sure you want to reset all settings to defaults?",
                "settings_reset": "Settings reset to defaults successfully",
                "settings_reset_cancelled": "Settings reset cancelled",
                "yes": "Yes",
                "no": "No",
                "filter_menu": "Filter Menu",
                "filter_options": "Filter Options",
                "show_files_only": "Show Files Only",
                "show_folders_only": "Show Folders Only",
                "show_text_files": "Show Text Files",
                "show_images": "Show Images",
                "show_archives": "Show Archives",
                "show_executables": "Show Executables",
                "custom_filter": "Custom Filter",
                "clear_filter": "Clear Filter",
                "back_to_navigation": "Back to Navigation",
                "enter_custom_pattern": "Enter custom filter pattern",
                "filter_applied": "Filter applied",
                "filter_cleared": "Filter cleared",
                "edit_mode": "Edit Mode",
                "view_mode": "View Mode",
                "save_changes": "Save Changes",
                "discard_changes": "Discard Changes",
                "enter_new_content": "Enter new content for line",
                "changes_saved": "Changes saved successfully",
                "changes_discarded": "Changes discarded",
                "confirm_save": "Save changes to file?",
                "confirm_discard": "Discard all changes?",
                "file_modified": "File has been modified",
                "editing_line": "Editing line",
                "press_escape_to_finish": "Press ESC to finish editing",
                "insert_mode": "INSERT",
                "overwrite_mode": "OVERWRITE",
                "new_line": "New Line",
                "line_break": "Line Break",
                "delete_line": "Delete Line"
            },
            "fr": {
                "main_menu": "MENU PRINCIPAL",
                "navigation": "Navigation",
                "settings": "Paramètres",
                "exit": "Quitter",
                "current_directory": "Répertoire Actuel",
                "settings_menu": "Menu des Paramètres",
                "change_language": "Changer de Langue",
                "display_preferences": "Préférences d'Affichage",
                "view_current_settings": "Voir les Paramètres Actuels",
                "reset_to_defaults": "Réinitialiser aux Valeurs par Défaut",
                "back_to_main_menu": "Retour au Menu Principal",
                "available_languages": "Langues Disponibles",
                "cancel": "Annuler",
                "language_changed": "Langue changée vers",
                "language_change_cancelled": "Changement de langue annulé",
                "invalid_choice": "Choix invalide",
                "press_enter_continue": "Appuyez sur Entrée pour continuer",
                "display_preferences_title": "Préférences d'Affichage",
                "show_hidden_files": "Afficher les Fichiers Cachés",
                "sort_order": "Ordre de Tri",
                "back_to_settings": "Retour aux Paramètres",
                "current_setting": "Paramètre actuel",
                "toggle": "Basculer?",
                "sort_options": "Options de Tri",
                "by_name": "Par Nom (alphabétique)",
                "by_size": "Par Taille",
                "by_date": "Par Date de Modification",
                "by_type": "Par Type",
                "sort_order_set": "Ordre de tri défini sur",
                "current_settings": "Paramètres Actuels",
                "language": "Langue",
                "theme": "Thème",
                "reset_confirm": "Êtes-vous sûr de vouloir réinitialiser tous les paramètres aux valeurs par défaut?",
                "settings_reset": "Paramètres réinitialisés aux valeurs par défaut avec succès",
                "settings_reset_cancelled": "Réinitialisation des paramètres annulée",
                "yes": "Oui",
                "no": "Non",
                "filter_menu": "Menu de Filtres",
                "filter_options": "Options de Filtres",
                "show_files_only": "Afficher Seulement les Fichiers",
                "show_folders_only": "Afficher Seulement les Dossiers",
                "show_text_files": "Afficher les Fichiers Texte",
                "show_images": "Afficher les Images",
                "show_archives": "Afficher les Archives",
                "show_executables": "Afficher les Exécutables",
                "custom_filter": "Filtre Personnalisé",
                "clear_filter": "Effacer le Filtre",
                "back_to_navigation": "Retour à la Navigation",
                "enter_custom_pattern": "Entrez un motif de filtre personnalisé",
                "filter_applied": "Filtre appliqué",
                "filter_cleared": "Filtre effacé",
                "edit_mode": "Mode Édition",
                "view_mode": "Mode Visualisation",
                "save_changes": "Sauvegarder les Modifications",
                "discard_changes": "Annuler les Modifications",
                "enter_new_content": "Entrez le nouveau contenu pour la ligne",
                "changes_saved": "Modifications sauvegardées avec succès",
                "changes_discarded": "Modifications annulées",
                "confirm_save": "Sauvegarder les modifications dans le fichier?",
                "confirm_discard": "Annuler toutes les modifications?",
                "file_modified": "Le fichier a été modifié",
                "editing_line": "Édition de la ligne",
                "press_escape_to_finish": "Appuyez sur ESC pour terminer l'édition",
                "insert_mode": "INSERTION",
                "overwrite_mode": "ÉCRASEMENT",
                "new_line": "Nouvelle Ligne",
                "line_break": "Saut de Ligne",
                "delete_line": "Supprimer la Ligne"
            },
            "es": {
                "main_menu": "MENÚ PRINCIPAL",
                "navigation": "Navegación",
                "settings": "Configuración",
                "exit": "Salir",
                "current_directory": "Directorio Actual",
                "settings_menu": "Menú de Configuración",
                "change_language": "Cambiar Idioma",
                "display_preferences": "Preferencias de Visualización",
                "view_current_settings": "Ver Configuración Actual",
                "reset_to_defaults": "Restablecer a Valores por Defecto",
                "back_to_main_menu": "Volver al Menú Principal",
                "available_languages": "Idiomas Disponibles",
                "cancel": "Cancelar",
                "language_changed": "Idioma cambiado a",
                "language_change_cancelled": "Cambio de idioma cancelado",
                "invalid_choice": "Opción inválida",
                "press_enter_continue": "Presiona Enter para continuar",
                "display_preferences_title": "Preferencias de Visualización",
                "show_hidden_files": "Mostrar Archivos Ocultos",
                "sort_order": "Orden de Clasificación",
                "back_to_settings": "Volver a Configuración",
                "current_setting": "Configuración actual",
                "toggle": "¿Alternar?",
                "sort_options": "Opciones de Clasificación",
                "by_name": "Por Nombre (alfabético)",
                "by_size": "Por Tamaño",
                "by_date": "Por Fecha de Modificación",
                "by_type": "Por Tipo",
                "sort_order_set": "Orden de clasificación establecido en",
                "current_settings": "Configuración Actual",
                "language": "Idioma",
                "theme": "Tema",
                "reset_confirm": "¿Estás seguro de que quieres restablecer toda la configuración a los valores por defecto?",
                "settings_reset": "Configuración restablecida a valores por defecto exitosamente",
                "settings_reset_cancelled": "Restablecimiento de configuración cancelado",
                "yes": "Sí",
                "no": "No",
                "filter_menu": "Menú de Filtros",
                "filter_options": "Opciones de Filtros",
                "show_files_only": "Mostrar Solo Archivos",
                "show_folders_only": "Mostrar Solo Carpetas",
                "show_text_files": "Mostrar Archivos de Texto",
                "show_images": "Mostrar Imágenes",
                "show_archives": "Mostrar Archivos",
                "show_executables": "Mostrar Ejecutables",
                "custom_filter": "Filtro Personalizado",
                "clear_filter": "Limpiar Filtro",
                "back_to_navigation": "Volver a Navegación",
                "enter_custom_pattern": "Ingrese patrón de filtro personalizado",
                "filter_applied": "Filtro aplicado",
                "filter_cleared": "Filtro limpiado"
            },
            "de": {
                "main_menu": "HAUPTMENÜ",
                "navigation": "Navigation",
                "settings": "Einstellungen",
                "exit": "Beenden",
                "current_directory": "Aktuelles Verzeichnis",
                "settings_menu": "Einstellungsmenü",
                "change_language": "Sprache Ändern",
                "display_preferences": "Anzeigeeinstellungen",
                "view_current_settings": "Aktuelle Einstellungen Anzeigen",
                "reset_to_defaults": "Auf Standardwerte Zurücksetzen",
                "back_to_main_menu": "Zurück zum Hauptmenü",
                "available_languages": "Verfügbare Sprachen",
                "cancel": "Abbrechen",
                "language_changed": "Sprache geändert zu",
                "language_change_cancelled": "Sprachänderung abgebrochen",
                "invalid_choice": "Ungültige Auswahl",
                "press_enter_continue": "Enter drücken um fortzufahren",
                "display_preferences_title": "Anzeigeeinstellungen",
                "show_hidden_files": "Versteckte Dateien Anzeigen",
                "sort_order": "Sortierreihenfolge",
                "back_to_settings": "Zurück zu Einstellungen",
                "current_setting": "Aktuelle Einstellung",
                "toggle": "Umschalten?",
                "sort_options": "Sortieroptionen",
                "by_name": "Nach Name (alphabetisch)",
                "by_size": "Nach Größe",
                "by_date": "Nach Änderungsdatum",
                "by_type": "Nach Typ",
                "sort_order_set": "Sortierreihenfolge festgelegt auf",
                "current_settings": "Aktuelle Einstellungen",
                "language": "Sprache",
                "theme": "Design",
                "reset_confirm": "Sind Sie sicher, dass Sie alle Einstellungen auf die Standardwerte zurücksetzen möchten?",
                "settings_reset": "Einstellungen erfolgreich auf Standardwerte zurückgesetzt",
                "settings_reset_cancelled": "Einstellungsrücksetzung abgebrochen",
                "yes": "Ja",
                "no": "Nein",
                "filter_menu": "Filter-Menü",
                "filter_options": "Filter-Optionen",
                "show_files_only": "Nur Dateien Anzeigen",
                "show_folders_only": "Nur Ordner Anzeigen",
                "show_text_files": "Textdateien Anzeigen",
                "show_images": "Bilder Anzeigen",
                "show_archives": "Archive Anzeigen",
                "show_executables": "Ausführbare Dateien Anzeigen",
                "custom_filter": "Benutzerdefinierter Filter",
                "clear_filter": "Filter Löschen",
                "back_to_navigation": "Zurück zur Navigation",
                "enter_custom_pattern": "Benutzerdefiniertes Filtermuster eingeben",
                "filter_applied": "Filter angewendet",
                "filter_cleared": "Filter gelöscht"
            },
            "ja": {
                "main_menu": "メインメニュー",
                "navigation": "ナビゲーション",
                "settings": "設定",
                "exit": "終了",
                "current_directory": "現在のディレクトリ",
                "settings_menu": "設定メニュー",
                "change_language": "言語を変更",
                "display_preferences": "表示設定",
                "view_current_settings": "現在の設定を表示",
                "reset_to_defaults": "デフォルトにリセット",
                "back_to_main_menu": "メインメニューに戻る",
                "available_languages": "利用可能な言語",
                "cancel": "キャンセル",
                "language_changed": "言語が変更されました",
                "language_change_cancelled": "言語変更がキャンセルされました",
                "invalid_choice": "無効な選択",
                "press_enter_continue": "続行するにはEnterを押してください",
                "display_preferences_title": "表示設定",
                "show_hidden_files": "隠しファイルを表示",
                "sort_order": "並び順",
                "back_to_settings": "設定に戻る",
                "current_setting": "現在の設定",
                "toggle": "切り替えますか？",
                "sort_options": "並び順オプション",
                "by_name": "名前順（アルファベット）",
                "by_size": "サイズ順",
                "by_date": "更新日時順",
                "by_type": "種類順",
                "sort_order_set": "並び順を設定しました",
                "current_settings": "現在の設定",
                "language": "言語",
                "theme": "テーマ",
                "reset_confirm": "すべての設定をデフォルトにリセットしてもよろしいですか？",
                "settings_reset": "設定がデフォルトにリセットされました",
                "settings_reset_cancelled": "設定リセットがキャンセルされました",
                "yes": "はい",
                "no": "いいえ",
                "filter_menu": "フィルターメニュー",
                "filter_options": "フィルターオプション",
                "show_files_only": "ファイルのみ表示",
                "show_folders_only": "フォルダーのみ表示",
                "show_text_files": "テキストファイルを表示",
                "show_images": "画像を表示",
                "show_archives": "アーカイブを表示",
                "show_executables": "実行ファイルを表示",
                "custom_filter": "カスタムフィルター",
                "clear_filter": "フィルターをクリア",
                "back_to_navigation": "ナビゲーションに戻る",
                "enter_custom_pattern": "カスタムフィルターパターンを入力",
                "filter_applied": "フィルターが適用されました",
                "filter_cleared": "フィルターがクリアされました"
            },
            "ru": {
                "main_menu": "ГЛАВНОЕ МЕНЮ",
                "navigation": "Навигация",
                "settings": "Настройки",
                "exit": "Выход",
                "current_directory": "Текущая Папка",
                "settings_menu": "Меню Настроек",
                "change_language": "Изменить Язык",
                "display_preferences": "Настройки Отображения",
                "view_current_settings": "Просмотр Текущих Настроек",
                "reset_to_defaults": "Сбросить к Значениям по Умолчанию",
                "back_to_main_menu": "Вернуться в Главное Меню",
                "available_languages": "Доступные Языки",
                "cancel": "Отмена",
                "language_changed": "Язык изменен на",
                "language_change_cancelled": "Изменение языка отменено",
                "invalid_choice": "Неверный выбор",
                "press_enter_continue": "Нажмите Enter для продолжения",
                "display_preferences_title": "Настройки Отображения",
                "show_hidden_files": "Показать Скрытые Файлы",
                "sort_order": "Порядок Сортировки",
                "back_to_settings": "Вернуться к Настройкам",
                "current_setting": "Текущая настройка",
                "toggle": "Переключить?",
                "sort_options": "Варианты Сортировки",
                "by_name": "По Имени (алфавитный)",
                "by_size": "По Размеру",
                "by_date": "По Дате Изменения",
                "by_type": "По Типу",
                "sort_order_set": "Порядок сортировки установлен на",
                "current_settings": "Текущие Настройки",
                "language": "Язык",
                "theme": "Тема",
                "reset_confirm": "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?",
                "settings_reset": "Настройки успешно сброшены к значениям по умолчанию",
                "settings_reset_cancelled": "Сброс настроек отменен",
                "yes": "Да",
                "no": "Нет",
                "filter_menu": "Меню Фильтров",
                "filter_options": "Опции Фильтров",
                "show_files_only": "Показать Только Файлы",
                "show_folders_only": "Показать Только Папки",
                "show_text_files": "Показать Текстовые Файлы",
                "show_images": "Показать Изображения",
                "show_archives": "Показать Архивы",
                "show_executables": "Показать Исполняемые Файлы",
                "custom_filter": "Пользовательский Фильтр",
                "clear_filter": "Очистить Фильтр",
                "back_to_navigation": "Вернуться к Навигации",
                "enter_custom_pattern": "Введите пользовательский шаблон фильтра",
                "filter_applied": "Фильтр применен",
                "filter_cleared": "Фильтр очищен"
            }
        }
        
    def get_text(self, key):
        """Get translated text for current language"""
        return self.translations.get(self.current_language, {}).get(key, 
               self.translations.get("en", {}).get(key, key))
        
    def load_language_settings(self):
        """Load language from settings file"""
        try:
            with open('data.json', 'r') as f:
                import json
                settings = json.load(f)
                self.current_language = settings.get("language", "en")
        except:
            self.current_language = "en"
    def settings_menu(self):
        """Display and handle settings menu"""
        # Si data.json n'existe pas, creer avec les valeurs par defaut
        if not os.path.exists('data.json'):
            default_settings = {
                "language": "en",
                "theme": "default",
                "show_hidden": False,
                "sort_by": "name"
            }
            with open('data.json', 'w') as f:
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
            
            choice = input(f"\n🎯 Choose an option (1-5): ").strip()
            
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
            with open('data.json', 'r') as f:
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
        
        choice = input(f"\n🎯 Choose language (1-31): ").strip()
        
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
                with open('data.json', 'w') as f:
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
            with open('data.json', 'r') as f:
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
            
            choice = input(f"\n🎯 Choose option (1-3): ").strip()
            
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
                
                sort_choice = input(f"\n🎯 Choose sort method (1-4): ").strip()
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
                with open('data.json', 'w') as f:
                    json.dump(settings, f, indent=4)
            except Exception as e:
                print(f"❌ Error saving settings: {e}")
                
            input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
            
    def view_current_settings(self):
        """View current application settings"""
        import json
        
        try:
            with open('data.json', 'r') as f:
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
                with open('data.json', 'w') as f:
                    import json
                    json.dump(default_settings, f, indent=4)
                self.current_language = "en"  # Reset current language
                print(f"✅ {self.get_text('settings_reset')}")
            except Exception as e:
                print(f"❌ Error resetting settings: {e}")
        else:
            print(f"❌ {self.get_text('settings_reset_cancelled')}")
            
        input(f"\n⏸️ {self.get_text('press_enter_continue')}...")
    def change_directory(self):
        """Change to a different directory with interactive navigation"""
        while True:
            print("\n📂 Current directory contents:")
            self.list_directory()
            
            print("\n📂 Navigation options:")
            print("1. Enter directory name manually")
            print("2. Select from numbered list")
            print("3. Go to parent directory (..)")
            print("4. Go to home directory (~)")
            print("5. Go to root directory (/)")
            print("6. Back to main menu")
            
            nav_choice = input("\n🎯 Choose navigation method (1-6): ").strip()
            
            if nav_choice == "1":
                self.manual_directory_input()
                break
            elif nav_choice == "2":
                self.select_directory_from_list()
                break
            elif nav_choice == "3":
                self.go_to_parent_directory()
                break
            elif nav_choice == "4":
                self.go_to_home_directory()
                break
            elif nav_choice == "5":
                self.go_to_root_directory()
                break
            elif nav_choice == "6":
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
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
            print("🚫 Permission denied to access this directory.")
            
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
                    print(f"{i}. 📁 {directory.name:<40} 🚫 Access Denied")
                    
            choice = int(input("\n🎯 Enter directory number (0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(directories):
                selected_dir = directories[choice - 1]
                try:
                    self.current_dir = selected_dir.resolve()
                    print(f"✅ Changed to: {self.current_dir}")
                except PermissionError:
                    print("🚫 Permission denied to access this directory.")
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
            
    def view_file_content(self):
        """View content of a text file with enhanced navigation"""
        while True:
            print("\n📄 Current directory files:")
            files = [item for item in self.current_dir.iterdir() if item.is_file()]
            
            if not files:
                print("📭 No files in current directory.")
                return
                
            # Display files with more details
            print(f"{'#':<3} {'📄 Name':<42} {'Size':<12} {'Modified'}")
            print("─" * 80)
            
            for i, file in enumerate(files, 1):
                try:
                    stat = file.stat()
                    size = self.format_size(stat.st_size)
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    file_emoji = self.get_file_emoji(file.suffix)
                    print(f"{i:<3} {file_emoji} {file.name:<38} {size:<12} {modified}")
                except PermissionError:
                    file_emoji = self.get_file_emoji(file.suffix)
                    print(f"{i:<3} {file_emoji} {file.name:<38} {'🚫 Access Denied':<12} {'🚫 Access Denied'}")
            
            print("\n👁️ File viewing options:")
            print("1. View file by number")
            print("2. Search files by name")
            print("3. View only text files")
            print("4. Back to main menu")
            
            view_choice = input("\n🎯 Choose option (1-4): ").strip()
            
            if view_choice == "1":
                self.view_file_by_number(files)
            elif view_choice == "2":
                self.search_and_view_file(files)
            elif view_choice == "3":
                self.view_text_files_only(files)
            elif view_choice == "4":
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
    def view_file_by_number(self, files):
        """View file by entering its number"""
        try:
            choice = int(input("\n👁️ Enter file number to view (0 to cancel): "))
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
        search_term = input("\n🔍 Enter file name to search (partial match): ").strip().lower()
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
            choice = int(input("\n👁️ Enter file number to view (0 to cancel): "))
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
            choice = int(input("\n👁️ Enter file number to view (0 to cancel): "))
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
                self.open_editor(file_path)
            else:
                print(f"⚠️ File '{file_path.name}' appears to be binary. Cannot display content.")
        except UnicodeDecodeError:
            print(f"⚠️ File '{file_path.name}' contains non-text content. Cannot display.")
        except PermissionError:
            print("🚫 Permission denied to read this file.")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            
    def open_editor(self, file_path):
        """Open file in integrated editor"""
        try:
            from editor import SimpleEditor
            
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
            input("\n⏸️ Press Enter to continue...")
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
                    controls_text = "⌨️ Editing: ←→ Move | ↑↓ Lines | Enter New Line | Insert/Delete | ESC Finish | Ctrl+S Save | Ctrl+D Discard"
                else:
                    controls_text = "⌨️ Editing: ←→ Move | Insert/Delete | ESC Finish | Ctrl+S Save | Ctrl+D Discard"
            elif edit_mode:
                controls_text = "⌨️ Controls: ↑↓ Navigate | E Edit Line | M Multi-line | S Save | D Discard | / Search | R Resize | Q Quit"
            else:
                controls_text = "⌨️ Controls: ↑↓ Navigate | E Edit Mode | / Search | N Next | P Prev | R Resize | Q Quit"
            
            if len(controls_text) > terminal_cols:
                if editing_line:
                    controls_text = "⌨️ Editing: ←→ Move | ESC Finish | Ctrl+S Save"
                elif edit_mode:
                    controls_text = "⌨️ Controls: ↑↓ Navigate | E Edit | S Save | D Discard | Q Quit"
                else:
                    controls_text = "⌨️ Controls: ↑↓ Navigate | E Edit | / Search | Q Quit"
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
        search_term = input("\n🔍 Enter search term: ").strip()
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
            input("\n⏸️ Press Enter to continue...")
            
    def edit_line(self, lines, modified_lines, line_index):
        """Edit a specific line"""
        if 0 <= line_index < len(lines):
            current_content = modified_lines.get(line_index, lines[line_index]).rstrip('\n\r')
            print(f"\n✏️ {self.get_text('enter_new_content')} {line_index + 1}:")
            print(f"Current: {current_content}")
            new_content = input("New: ").strip()
            
            if new_content != current_content:
                modified_lines[line_index] = new_content + '\n'
                print(f"✅ Line {line_index + 1} modified")
            else:
                print("ℹ️ No changes made")
                
            input("\n⏸️ Press Enter to continue...")
            
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
            input("\n⏸️ Press Enter to continue...")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            input("\n⏸️ Press Enter to continue...")
            
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
            
    def copy_item(self):
        """Copy a file or directory"""
        print("\nCurrent directory contents:")
        self.list_directory()
        
        source = input("\n📋 Enter source file/folder name: ").strip()
        if not source:
            return
            
        source_path = self.current_dir / source
        if not source_path.exists():
            print(f"❌ '{source}' does not exist.")
            return
            
        destination = input("📂 Enter destination path: ").strip()
        if not destination:
            return
            
        destination_path = Path(destination)
        
        try:
            if source_path.is_file():
                shutil.copy2(source_path, destination_path)
                print(f"✅ File copied successfully to {destination_path}")
            elif source_path.is_dir():
                shutil.copytree(source_path, destination_path)
                print(f"✅ Directory copied successfully to {destination_path}")
        except Exception as e:
            print(f"❌ Error copying: {e}")
            
    def move_item(self):
        """Move/rename a file or directory"""
        print("\nCurrent directory contents:")
        self.list_directory()
        
        source = input("\n✂️ Enter source file/folder name: ").strip()
        if not source:
            return
            
        source_path = self.current_dir / source
        if not source_path.exists():
            print(f"❌ '{source}' does not exist.")
            return
            
        destination = input("📂 Enter destination path: ").strip()
        if not destination:
            return
            
        destination_path = Path(destination)
        
        # Confirmation for move operation
        confirm = input(f"⚠️ Move '{source}' to '{destination}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return
            
        try:
            shutil.move(str(source_path), str(destination_path))
            print(f"✅ Item moved successfully to {destination_path}")
        except Exception as e:
            print(f"❌ Error moving: {e}")
            
    def delete_item(self):
        """Delete a file or directory"""
        print("\nCurrent directory contents:")
        self.list_directory()
        
        item_name = input("\n🗑️ Enter file/folder name to delete: ").strip()
        if not item_name:
            return
            
        item_path = self.current_dir / item_name
        if not item_path.exists():
            print(f"❌ '{item_name}' does not exist.")
            return
            
        # Confirmation for delete operation
        confirm = input(f"⚠️ Are you sure you want to delete '{item_name}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return
            
        try:
            if item_path.is_file():
                item_path.unlink()
                print(f"✅ File '{item_name}' deleted successfully.")
            elif item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"✅ Directory '{item_name}' deleted successfully.")
        except Exception as e:
            print(f"❌ Error deleting: {e}")
            
    def rename_item(self):
        """Rename a file or directory"""
        print("\nCurrent directory contents:")
        self.list_directory()
        
        old_name = input("\n✏️ Enter current file/folder name: ").strip()
        if not old_name:
            return
            
        old_path = self.current_dir / old_name
        if not old_path.exists():
            print(f"❌ '{old_name}' does not exist.")
            return
            
        new_name = input("✏️ Enter new name: ").strip()
        if not new_name:
            return
            
        new_path = self.current_dir / new_name
        
        try:
            old_path.rename(new_path)
            print(f"✅ '{old_name}' renamed to '{new_name}' successfully.")
        except Exception as e:
            print(f"❌ Error renaming: {e}")
            
    def create_file(self):
        """Create a new file"""
        filename = input("\n📄 Enter new file name: ").strip()
        if not filename:
            return
            
        file_path = self.current_dir / filename
        
        if file_path.exists():
            print(f"⚠️ File '{filename}' already exists.")
            return
            
        try:
            file_path.touch()
            print(f"✅ File '{filename}' created successfully.")
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            
    def create_directory(self):
        """Create a new directory"""
        dirname = input("\n📁 Enter new directory name: ").strip()
        if not dirname:
            return
            
        dir_path = self.current_dir / dirname
        
        if dir_path.exists():
            print(f"⚠️ Directory '{dirname}' already exists.")
            return
            
        try:
            dir_path.mkdir()
            print(f"✅ Directory '{dirname}' created successfully.")
        except Exception as e:
            print(f"❌ Error creating directory: {e}")
            
    def quick_navigation(self):
        """Quick navigation with file and folder selection"""
        while True:
            print("\n🚀 Quick Navigation")
            print("Current directory contents:")
            self.list_directory()
            
            print("\n🚀 Quick navigation options:")
            print("1. Navigate to folder by number")
            print("2. View file by number")
            print("3. Go to parent directory")
            print("4. Go to home directory")
            print("5. Go to root directory")
            print("6. Back to main menu")
            
            choice = input("\n🎯 Choose option (1-6): ").strip()
            
            if choice == "1":
                self.quick_navigate_to_folder()
            elif choice == "2":
                self.quick_view_file()
            elif choice == "3":
                self.go_to_parent_directory()
            elif choice == "4":
                self.go_to_home_directory()
            elif choice == "5":
                self.go_to_root_directory()
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
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
                    print(f"{i}. 📁 {directory.name:<40} 🚫 Access Denied")
                    
            choice = int(input("\n🎯 Enter directory number (0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(directories):
                selected_dir = directories[choice - 1]
                try:
                    self.current_dir = selected_dir.resolve()
                    print(f"✅ Changed to: {self.current_dir}")
                except PermissionError:
                    print("🚫 Permission denied to access this directory.")
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
                    print(f"{i}. {file_emoji} {file.name:<40} 🚫 Access Denied")
                    
            choice = int(input("\n👁️ Enter file number to view (0 to cancel): "))
            
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
                        print("📭 Directory is empty.")
                    
                    # Fill remaining space
                    for _ in range(available_lines - 1):
                        print()
                    
                    print("⌨️ Controls: ↑↓ Navigate | Enter Select | ESC Back | H Home | R Root | P Parent | F Filter")
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
                        print(f"{prefix}{item.name:<40} {'[FILE]':<10} {'🚫 Access Denied':<15} {'🚫 Access Denied'}")
                    
                    items_displayed += 1
                
                # Fill remaining space with empty lines to push controls to bottom
                remaining_lines = available_lines - items_displayed
                for _ in range(remaining_lines):
                    print()
                        
            except PermissionError:
                # Fill space to push controls to bottom
                terminal_rows, terminal_cols = self.get_terminal_size()
                available_lines = terminal_rows - 4  # Reserve space for message and controls
                
                print("🚫 Permission denied to access this directory.")
                
                # Fill remaining space
                for _ in range(available_lines - 1):
                    print()
                
                print("⌨️ Controls: ESC Back | H Home | R Root | P Parent | F Filter")
                key = self.get_key()
                if key == 'ESCAPE':
                    self.menu_mode = False
                continue
                
            # Display controls
            print("\n⌨️ Controls:")
            if self.filter_active:
                filter_display = self.get_filter_display_name()
                controls_text = f"↑↓ Navigate | Enter Select | ESC Back | H Home | V View | D Delete | C Copy | M Move | R Rename | N New File | G New Folder | 🔍 Filter: {filter_display} (F to change)"
            else:
                controls_text = "↑↓ Navigate | Enter Select | ESC Back | H Home | V View | D Delete | C Copy | M Move | R Rename | N New File | G New Folder | F Filter"
            
            # Truncate controls if too long for terminal
            if len(controls_text) > terminal_cols:
                if self.filter_active:
                    controls_text = f"↑↓ Navigate | Enter Select | ESC Back | V View | 🔍 Filter: {filter_display} (F to change)"
                else:
                    controls_text = "↑↓ Navigate | Enter Select | ESC Back | V View | F Filter"
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
                print("🚫 Permission denied to access this directory.")
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
                print("🚫 Access denied to file information")
                
            print("\n🎯 File Options:")
            print("V - View content")
            print("C - Copy file")
            print("M - Move file")
            print("R - Rename file")
            print("D - Delete file")
            print("ESC - Back to navigation")
            
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
            input("\n⏸️ Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error copying: {e}")
            input("\n⏸️ Press Enter to continue...")
            
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
            input("\n⏸️ Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error moving: {e}")
            input("\n⏸️ Press Enter to continue...")
            
    def rename_selected_item(self, item_path):
        """Rename a selected item"""
        new_name = input(f"\n✏️ Enter new name for '{item_path.name}': ").strip()
        if not new_name:
            return
            
        new_path = item_path.parent / new_name
        
        try:
            item_path.rename(new_path)
            print(f"✅ '{item_path.name}' renamed to '{new_name}' successfully.")
            input("\n⏸️ Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error renaming: {e}")
            input("\n⏸️ Press Enter to continue...")
            
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
            input("\n⏸️ Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error deleting: {e}")
            input("\n⏸️ Press Enter to continue...")
            
    def create_file_interactive(self):
        """Create a new file interactively"""
        filename = input("\n📄 Enter new file name: ").strip()
        if not filename:
            return
            
        file_path = self.current_dir / filename
        
        if file_path.exists():
            print(f"⚠️ File '{filename}' already exists.")
            input("\n⏸️ Press Enter to continue...")
            return
            
        try:
            file_path.touch()
            print(f"✅ File '{filename}' created successfully.")
            input("\n⏸️ Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            input("\n⏸️ Press Enter to continue...")
            
    def create_directory_interactive(self):
        """Create a new directory interactively"""
        dirname = input("\n📁 Enter new directory name: ").strip()
        if not dirname:
            return
            
        dir_path = self.current_dir / dirname
        
        if dir_path.exists():
            print(f"⚠️ Directory '{dirname}' already exists.")
            input("\n⏸️ Press Enter to continue...")
            return
            
        try:
            dir_path.mkdir()
            print(f"✅ Directory '{dirname}' created successfully.")
            input("\n⏸️ Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error creating directory: {e}")
            input("\n⏸️ Press Enter to continue...")
            
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
            
    def display_menu(self):
        """Display the main menu"""
        self.load_language_settings()  # Load current language
        terminal_rows, terminal_cols = self.get_terminal_size()
        
        print(f"                    🎯 {self.get_text('main_menu')} 🎯")
        print("═" * terminal_cols)
        print(f"1. 🚀 {self.get_text('navigation')}")
        print(f"2. ⚙️ {self.get_text('settings')}")
        print(f"3. 🚪 {self.get_text('exit')}")
        
        # Fill remaining space to push input to bottom
        available_lines = terminal_rows - 10  # Reserve space for logo, path, menu, and input
        for _ in range(available_lines):
            print()
        
        print("═" * terminal_cols)
        
    def run(self):
        """Main application loop"""
        while self.running:
            self.clear_screen()
            self.display_logo()
            self.display_current_path()
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1":
                    self.navigation()
                elif choice == "2":
                    self.settings_menu()
                elif choice == "3":
                    print("\n👋 Thank you for using KASER File Manager!")
                    self.running = False
                else:
                    print("❌ Invalid choice. Please enter a number between 1-3.")
                    
                if self.running:
                    input("\n⏸️ Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                self.running = False
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("⏸️ Press Enter to continue...")


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
