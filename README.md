# 📁 KASER File Manager

A beautiful console-based file manager built in Python with a menu-driven interface and emoji-rich UI.

## ✨ Features

- **📂 Navigation**: Browse directories and view current path with emoji indicators
- **🔄 File Operations**: Copy, move, delete, and rename files and folders
- **👁️ Content Viewing**: View text file contents directly in the console
- **📄 File Management**: Create new files and directories
- **🎯 User-Friendly**: Menu-driven interface with numbered options and emojis
- **🌍 Cross-Platform**: Works on Windows, Linux, and macOS
- **🛡️ Safe Operations**: Confirmation prompts for destructive operations
- **🎨 Beautiful UI**: Emoji-rich interface for better visual experience
- **📊 Smart File Icons**: Different emojis for different file types

## Requirements

- Python 3.6 or higher
- Standard library modules (os, shutil, pathlib, datetime)
- Optional: pyfiglet (for ASCII art logo)

## Installation

1. Clone or download this repository
2. Install optional dependencies (for logo):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the file manager:
```bash
python file_manager.py
```

### 🎯 Menu Options

1. **⌨️ Interactive Navigation (Arrow Keys) - RECOMMENDED** - Complete file manager with keyboard navigation
2. **📋 List directory contents** - View files and folders in current directory
3. **📂 Change directory (Enhanced Navigation)** - Advanced navigation with multiple options
4. **👁️ View file content (Enhanced)** - Advanced file viewing with search and filtering
5. **🚀 Quick navigation** - Fast navigation by selecting numbered items
6. **📋 Copy file/folder** - Copy items to another location
7. **✂️ Move/rename file/folder** - Move or rename items
8. **🗑️ Delete file/folder** - Remove items (with confirmation)
9. **✏️ Rename file/folder** - Rename existing items
10. **📄 Create new file** - Create empty text files
11. **📁 Create new directory** - Create new folders
12. **🚪 Exit** - Quit the application

### 🧭 Navigation Features

#### 📂 Enhanced Directory Navigation (Option 2)
- **Manual input**: Type directory name or use `..` for parent
- **Numbered selection**: Choose from a numbered list of directories
- **Quick shortcuts**: Go to parent, home, or root directory
- **Visual feedback**: See directory contents before navigating

#### 👁️ Enhanced File Viewing (Option 3)
- **Numbered selection**: Choose files from a detailed list
- **Search functionality**: Find files by partial name matching
- **Text file filtering**: View only text files (Python, HTML, CSS, etc.)
- **Detailed information**: File size, modification date, and type icons

#### 🚀 Quick Navigation (Option 4)
- **Instant folder access**: Navigate to folders by number
- **Quick file viewing**: View files by selecting their number
- **Rapid shortcuts**: Fast access to parent, home, and root directories
- **Streamlined interface**: Minimal steps for common operations

#### ⌨️ Interactive Navigation (Option 1) - RECOMMENDED!
- **Complete file manager**: All operations available with keyboard navigation
- **Arrow key navigation**: Use ↑↓ to navigate through files and folders
- **Visual selection**: Selected item highlighted with ▶️ indicator
- **Special navigation items**:
  - **⬆️ .. (Parent Directory)** - Navigate to parent directory
  - **🏠 ... (Root Directory)** - Navigate to root directory
- **Keyboard shortcuts**:
  - **↑↓** Navigate up/down through items
  - **Enter** Select folder (enter) or show file options
  - **ESC** Back to main menu
  - **H** Go to home directory
  - **V** View selected file content
  - **D** Delete selected item
  - **C** Copy selected item
  - **M** Move selected item
  - **R** Rename selected item
  - **N** Create new file
  - **F** Create new folder
- **File operations menu**: When selecting a file, get options for:
  - **V** View content
  - **C** Copy file
  - **M** Move file
  - **R** Rename file
  - **D** Delete file
  - **ESC** Back to navigation
- **Cross-platform**: Works on Windows, Linux, and macOS
- **No command line needed**: All operations available through keyboard shortcuts

#### 🧭 General Navigation Tips
- Use `..` to go to parent directory
- Enter full paths for absolute navigation
- Use relative paths for local navigation
- Press Enter to continue after each operation
- Use numbered lists for faster selection

### 🛡️ Safety Features

- ⚠️ Confirmation prompts for delete and move operations
- 🚫 Permission error handling with clear messages
- ✅ Input validation and error feedback
- 🔄 Graceful error handling with emoji indicators

## 📄 File Types Supported for Viewing

The file manager can display content for common text file types:
- 📝 `.txt` - Text files
- 🐍 `.py` - Python files
- 📖 `.md` - Markdown files
- 📋 `.json` - JSON files
- 📄 `.xml` - XML files
- 🌐 `.html` - HTML files
- 🎨 `.css` - CSS files
- 🟨 `.js` - JavaScript files

## 🎨 Emoji File Type Icons

The file manager displays different emojis for different file types:
- 🐍 Python files (.py)
- 🟨 JavaScript files (.js)
- 🌐 HTML files (.html)
- 🎨 CSS files (.css)
- 📋 JSON files (.json)
- 📖 Markdown files (.md)
- 🖼️ Image files (.jpg, .png, .gif, etc.)
- 🎵 Audio files (.mp3, .wav, .flac)
- 🎬 Video files (.mp4, .avi, .mov)
- 🗜️ Archive files (.zip, .rar, .7z)
- ⚙️ Executable files (.exe, .msi)
- 📊 Spreadsheet files (.xls, .xlsx)
- 📽️ Presentation files (.ppt, .pptx)
- And many more!

## 🚫 Error Handling

The application handles common errors gracefully with emoji indicators:
- 🚫 Permission denied errors
- ❌ File not found errors
- ❌ Invalid input errors
- ⚠️ Unicode decode errors for binary files

## ⌨️ Keyboard Shortcuts

### General Application
- `Ctrl+C` - 🚪 Exit the application
- `Enter` - ⏸️ Continue after operations

### Interactive Navigation Mode (Option 1) - RECOMMENDED
- `↑↓` - Navigate through files and folders
- `Enter` - Select folder or show file options
- `ESC` - Back to main menu
- `H` - Go to home directory
- `V` - View selected file content
- `D` - Delete selected item
- `C` - Copy selected item
- `M` - Move selected item
- `R` - Rename selected item
- `N` - Create new file
- `F` - Create new folder

### File Operations Menu
- `V` - View file content
- `C` - Copy file
- `M` - Move file
- `R` - Rename file
- `D` - Delete file
- `ESC` - Back to navigation

## 📄 License

This project is open source and available under the MIT License.
