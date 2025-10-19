#!/usr/bin/env python3
"""
Script to generate translations for all missing languages
"""

# All the new translation keys that need to be added
new_keys = {
    # Control texts
    "controls_navigate": {
        "zh": "↑↓ 导航", "ar": "↑↓ التنقل", "hi": "↑↓ नेविगेट", "pt": "↑↓ Navegar", 
        "it": "↑↓ Naviga", "nl": "↑↓ Navigeren", "pl": "↑↓ Nawiguj", "tr": "↑↓ Gezin",
        "ko": "↑↓ 탐색", "th": "↑↓ นำทาง", "vi": "↑↓ Điều hướng", "id": "↑↓ Navigasi",
        "uk": "↑↓ Навігація", "cs": "↑↓ Navigace", "hu": "↑↓ Navigálás", "ro": "↑↓ Navigare",
        "bg": "↑↓ Навигация", "hr": "↑↓ Navigacija", "fi": "↑↓ Navigoi", "no": "↑↓ Naviger",
        "sv": "↑↓ Navigera", "da": "↑↓ Naviger", "el": "↑↓ Πλοήγηση", "he": "↑↓ ניווט"
    },
    "controls_select": {
        "zh": "Enter 选择", "ar": "Enter اختيار", "hi": "Enter चुनें", "pt": "Enter Selecionar",
        "it": "Enter Seleziona", "nl": "Enter Selecteren", "pl": "Enter Wybierz", "tr": "Enter Seç",
        "ko": "Enter 선택", "th": "Enter เลือก", "vi": "Enter Chọn", "id": "Enter Pilih",
        "uk": "Enter Вибрати", "cs": "Enter Vybrat", "hu": "Enter Kiválaszt", "ro": "Enter Selectează",
        "bg": "Enter Избери", "hr": "Enter Odaberi", "fi": "Enter Valitse", "no": "Enter Velg",
        "sv": "Enter Välj", "da": "Enter Vælg", "el": "Enter Επιλογή", "he": "Enter בחר"
    },
    "controls_back": {
        "zh": "ESC 返回", "ar": "ESC رجوع", "hi": "ESC वापस", "pt": "ESC Voltar",
        "it": "ESC Indietro", "nl": "ESC Terug", "pl": "ESC Wstecz", "tr": "ESC Geri",
        "ko": "ESC 뒤로", "th": "ESC กลับ", "vi": "ESC Quay lại", "id": "ESC Kembali",
        "uk": "ESC Назад", "cs": "ESC Zpět", "hu": "ESC Vissza", "ro": "ESC Înapoi",
        "bg": "ESC Назад", "hr": "ESC Natrag", "fi": "ESC Takaisin", "no": "ESC Tilbake",
        "sv": "ESC Tillbaka", "da": "ESC Tilbage", "el": "ESC Πίσω", "he": "ESC חזור"
    },
    "controls_home": {
        "zh": "H 主页", "ar": "H الرئيسية", "hi": "H होम", "pt": "H Início",
        "it": "H Casa", "nl": "H Start", "pl": "H Strona główna", "tr": "H Ana sayfa",
        "ko": "H 홈", "th": "H หน้าแรก", "vi": "H Trang chủ", "id": "H Beranda",
        "uk": "H Головна", "cs": "H Domů", "hu": "H Kezdőlap", "ro": "H Acasă",
        "bg": "H Начало", "hr": "H Početna", "fi": "H Koti", "no": "H Hjem",
        "sv": "H Hem", "da": "H Hjem", "el": "H Αρχική", "he": "H בית"
    },
    "controls_view": {
        "zh": "V 查看", "ar": "V عرض", "hi": "V देखें", "pt": "V Ver",
        "it": "V Visualizza", "nl": "V Bekijk", "pl": "V Zobacz", "tr": "V Görüntüle",
        "ko": "V 보기", "th": "V ดู", "vi": "V Xem", "id": "V Lihat",
        "uk": "V Перегляд", "cs": "V Zobrazit", "hu": "V Megtekint", "ro": "V Vizualizează",
        "bg": "V Преглед", "hr": "V Prikaži", "fi": "V Näytä", "no": "V Vis",
        "sv": "V Visa", "da": "V Vis", "el": "V Προβολή", "he": "V הצג"
    },
    "controls_delete": {
        "zh": "D 删除", "ar": "D حذف", "hi": "D हटाएं", "pt": "D Excluir",
        "it": "D Elimina", "nl": "D Verwijder", "pl": "D Usuń", "tr": "D Sil",
        "ko": "D 삭제", "th": "D ลบ", "vi": "D Xóa", "id": "D Hapus",
        "uk": "D Видалити", "cs": "D Smazat", "hu": "D Töröl", "ro": "D Șterge",
        "bg": "D Изтрий", "hr": "D Obriši", "fi": "D Poista", "no": "D Slett",
        "sv": "D Ta bort", "da": "D Slet", "el": "D Διαγραφή", "he": "D מחק"
    },
    "controls_copy": {
        "zh": "C 复制", "ar": "C نسخ", "hi": "C कॉपी", "pt": "C Copiar",
        "it": "C Copia", "nl": "C Kopieer", "pl": "C Kopiuj", "tr": "C Kopyala",
        "ko": "C 복사", "th": "C คัดลอก", "vi": "C Sao chép", "id": "C Salin",
        "uk": "C Копіювати", "cs": "C Kopírovat", "hu": "C Másol", "ro": "C Copiază",
        "bg": "C Копирай", "hr": "C Kopiraj", "fi": "C Kopioi", "no": "C Kopier",
        "sv": "C Kopiera", "da": "C Kopier", "el": "C Αντιγραφή", "he": "C העתק"
    },
    "controls_move": {
        "zh": "M 移动", "ar": "M نقل", "hi": "M स्थानांतरित", "pt": "M Mover",
        "it": "M Sposta", "nl": "M Verplaats", "pl": "M Przenieś", "tr": "M Taşı",
        "ko": "M 이동", "th": "M ย้าย", "vi": "M Di chuyển", "id": "M Pindahkan",
        "uk": "M Перемістити", "cs": "M Přesunout", "hu": "M Áthelyez", "ro": "M Mută",
        "bg": "M Премести", "hr": "M Premjesti", "fi": "M Siirrä", "no": "M Flytt",
        "sv": "M Flytta", "da": "M Flyt", "el": "M Μετακίνηση", "he": "M העבר"
    },
    "controls_rename": {
        "zh": "R 重命名", "ar": "R إعادة تسمية", "hi": "R नाम बदलें", "pt": "R Renomear",
        "it": "R Rinomina", "nl": "R Hernoem", "pl": "R Zmień nazwę", "tr": "R Yeniden adlandır",
        "ko": "R 이름 바꾸기", "th": "R เปลี่ยนชื่อ", "vi": "R Đổi tên", "id": "R Ubah nama",
        "uk": "R Перейменувати", "cs": "R Přejmenovat", "hu": "R Átnevez", "ro": "R Redenumește",
        "bg": "R Преименувай", "hr": "R Preimenuj", "fi": "R Nimeä uudelleen", "no": "R Gi nytt navn",
        "sv": "R Byt namn", "da": "R Omdøb", "el": "R Μετονομασία", "he": "R שנה שם"
    },
    "controls_new_file": {
        "zh": "N 新建文件", "ar": "N ملف جديد", "hi": "N नई फ़ाइल", "pt": "N Novo Arquivo",
        "it": "N Nuovo File", "nl": "N Nieuw Bestand", "pl": "N Nowy Plik", "tr": "N Yeni Dosya",
        "ko": "N 새 파일", "th": "N ไฟล์ใหม่", "vi": "N Tệp mới", "id": "N File Baru",
        "uk": "N Новий Файл", "cs": "N Nový Soubor", "hu": "N Új Fájl", "ro": "N Fișier Nou",
        "bg": "N Нов Файл", "hr": "N Nova Datoteka", "fi": "N Uusi Tiedosto", "no": "N Ny Fil",
        "sv": "N Ny Fil", "da": "N Ny Fil", "el": "N Νέο Αρχείο", "he": "N קובץ חדש"
    },
    "controls_new_folder": {
        "zh": "G 新建文件夹", "ar": "G مجلد جديد", "hi": "G नया फ़ोल्डर", "pt": "G Nova Pasta",
        "it": "G Nuova Cartella", "nl": "G Nieuwe Map", "pl": "G Nowy Folder", "tr": "G Yeni Klasör",
        "ko": "G 새 폴더", "th": "G โฟลเดอร์ใหม่", "vi": "G Thư mục mới", "id": "G Folder Baru",
        "uk": "G Нова Папка", "cs": "G Nová Složka", "hu": "G Új Mappa", "ro": "G Dosar Nou",
        "bg": "G Нова Папка", "hr": "G Nova Mapa", "fi": "G Uusi Kansio", "no": "G Ny Mappe",
        "sv": "G Ny Mapp", "da": "G Ny Mappe", "el": "G Νέος Φάκελος", "he": "G תיקייה חדשה"
    },
    "controls_filter": {
        "zh": "F 筛选", "ar": "F تصفية", "hi": "F फ़िल्टर", "pt": "F Filtrar",
        "it": "F Filtra", "nl": "F Filter", "pl": "F Filtruj", "tr": "F Filtrele",
        "ko": "F 필터", "th": "F กรอง", "vi": "F Lọc", "id": "F Filter",
        "uk": "F Фільтр", "cs": "F Filtr", "hu": "F Szűrő", "ro": "F Filtrează",
        "bg": "F Филтър", "hr": "F Filtriraj", "fi": "F Suodata", "no": "F Filtrer",
        "sv": "F Filtrera", "da": "F Filtrer", "el": "F Φίλτρο", "he": "F סינון"
    },
    "controls_edit": {
        "zh": "E 编辑", "ar": "E تحرير", "hi": "E संपादित", "pt": "E Editar",
        "it": "E Modifica", "nl": "E Bewerk", "pl": "E Edytuj", "tr": "E Düzenle",
        "ko": "E 편집", "th": "E แก้ไข", "vi": "E Chỉnh sửa", "id": "E Edit",
        "uk": "E Редагувати", "cs": "E Upravit", "hu": "E Szerkeszt", "ro": "E Editează",
        "bg": "E Редактирай", "hr": "E Uredi", "fi": "E Muokkaa", "no": "E Rediger",
        "sv": "E Redigera", "da": "E Rediger", "el": "E Επεξεργασία", "he": "E ערוך"
    },
    "controls_save": {
        "zh": "S 保存", "ar": "S حفظ", "hi": "S सहेजें", "pt": "S Salvar",
        "it": "S Salva", "nl": "S Opslaan", "pl": "S Zapisz", "tr": "S Kaydet",
        "ko": "S 저장", "th": "S บันทึก", "vi": "S Lưu", "id": "S Simpan",
        "uk": "S Зберегти", "cs": "S Uložit", "hu": "S Mentés", "ro": "S Salvează",
        "bg": "S Запази", "hr": "S Spremi", "fi": "S Tallenna", "no": "S Lagre",
        "sv": "S Spara", "da": "S Gem", "el": "S Αποθήκευση", "he": "S שמור"
    },
    "controls_quit": {
        "zh": "Q 退出", "ar": "Q خروج", "hi": "Q बाहर निकलें", "pt": "Q Sair",
        "it": "Q Esci", "nl": "Q Afsluiten", "pl": "Q Wyjdź", "tr": "Q Çık",
        "ko": "Q 종료", "th": "Q ออก", "vi": "Q Thoát", "id": "Q Keluar",
        "uk": "Q Вихід", "cs": "Q Ukončit", "hu": "Q Kilépés", "ro": "Q Ieșire",
        "bg": "Q Изход", "hr": "Q Izlaz", "fi": "Q Lopeta", "no": "Q Avslutt",
        "sv": "Q Avsluta", "da": "Q Afslut", "el": "Q Έξοδος", "he": "Q יציאה"
    }
}

# Generate the translation strings for all languages
def generate_translations():
    languages = ["zh", "ar", "hi", "pt", "it", "nl", "pl", "tr", "ko", "th", "vi", "id", "uk", "cs", "hu", "ro", "bg", "hr", "fi", "no", "sv", "da", "el", "he"]
    
    for lang in languages:
        print(f'            "{lang}": {{')
        print(f'                "main_menu": "MAIN MENU",')
        print(f'                "navigation": "Navigation",')
        print(f'                "settings": "Settings",')
        print(f'                "exit": "Exit",')
        print(f'                "current_directory": "Current Directory",')
        print(f'                "settings_menu": "Settings Menu",')
        print(f'                "change_language": "Change Language",')
        print(f'                "display_preferences": "Display Preferences",')
        print(f'                "view_current_settings": "View Current Settings",')
        print(f'                "reset_to_defaults": "Reset to Defaults",')
        print(f'                "back_to_main_menu": "Back to Main Menu",')
        print(f'                "available_languages": "Available Languages",')
        print(f'                "cancel": "Cancel",')
        print(f'                "language_changed": "Language changed to",')
        print(f'                "language_change_cancelled": "Language change cancelled",')
        print(f'                "invalid_choice": "Invalid choice",')
        print(f'                "press_enter_continue": "Press Enter to continue",')
        print(f'                "display_preferences_title": "Display Preferences",')
        print(f'                "show_hidden_files": "Show Hidden Files",')
        print(f'                "sort_order": "Sort Order",')
        print(f'                "back_to_settings": "Back to Settings",')
        print(f'                "current_setting": "Current setting",')
        print(f'                "toggle": "Toggle?",')
        print(f'                "sort_options": "Sort Options",')
        print(f'                "by_name": "By Name (alphabetical)",')
        print(f'                "by_size": "By Size",')
        print(f'                "by_date": "By Date Modified",')
        print(f'                "by_type": "By Type",')
        print(f'                "sort_order_set": "Sort order set to",')
        print(f'                "current_settings": "Current Settings",')
        print(f'                "language": "Language",')
        print(f'                "theme": "Theme",')
        print(f'                "reset_confirm": "Are you sure you want to reset all settings to defaults?",')
        print(f'                "settings_reset": "Settings reset to defaults successfully",')
        print(f'                "settings_reset_cancelled": "Settings reset cancelled",')
        print(f'                "yes": "Yes",')
        print(f'                "no": "No",')
        print(f'                "filter_menu": "Filter Menu",')
        print(f'                "filter_options": "Filter Options",')
        print(f'                "show_files_only": "Show Files Only",')
        print(f'                "show_folders_only": "Show Folders Only",')
        print(f'                "show_text_files": "Show Text Files",')
        print(f'                "show_images": "Show Images",')
        print(f'                "show_archives": "Show Archives",')
        print(f'                "show_executables": "Show Executables",')
        print(f'                "custom_filter": "Custom Filter",')
        print(f'                "clear_filter": "Clear Filter",')
        print(f'                "back_to_navigation": "Back to Navigation",')
        print(f'                "enter_custom_pattern": "Enter custom filter pattern",')
        print(f'                "filter_applied": "Filter applied",')
        print(f'                "filter_cleared": "Filter cleared",')
        print(f'                "edit_mode": "Edit Mode",')
        print(f'                "view_mode": "View Mode",')
        print(f'                "save_changes": "Save Changes",')
        print(f'                "discard_changes": "Discard Changes",')
        print(f'                "enter_new_content": "Enter new content for line",')
        print(f'                "changes_saved": "Changes saved successfully",')
        print(f'                "changes_discarded": "Changes discarded",')
        print(f'                "confirm_save": "Save changes to file?",')
        print(f'                "confirm_discard": "Discard all changes?",')
        print(f'                "file_modified": "File has been modified",')
        print(f'                "editing_line": "Editing line",')
        print(f'                "press_escape_to_finish": "Press ESC to finish editing",')
        print(f'                "insert_mode": "INSERT",')
        print(f'                "overwrite_mode": "OVERWRITE",')
        print(f'                "new_line": "New Line",')
        print(f'                "line_break": "Line Break",')
        print(f'                "delete_line": "Delete Line",')
        
        # Add control texts
        for key, translations in new_keys.items():
            if lang in translations:
                print(f'                "{key}": "{translations[lang]}",')
        
        print(f'            }},')
        print()

if __name__ == "__main__":
    generate_translations()
