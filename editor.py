#!/usr/bin/env python3
"""
Simple text editor module for KASER file manager
Provides a nano-like editing experience with proper line handling
"""

import os
import sys
from pathlib import Path

class SimpleEditor:
    def __init__(self, file_path, translations=None):
        self.file_path = Path(file_path)
        self.translations = translations or {}
        self.lines = []
        self.current_line = 0
        self.cursor_pos = 0
        self.insert_mode = True
        self.modified = False
        self.terminal_rows = 24
        self.terminal_cols = 80
        
    def get_text(self, key):
        """Get translated text"""
        return self.translations.get(key, key)
    
    def get_terminal_size(self):
        """Get terminal size"""
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
            return 24, 80
    
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def load_file(self):
        """Load file content"""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.lines = f.readlines()
            else:
                self.lines = ['']
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def save_file(self):
        """Save file content"""
        try:
            # Create backup
            backup_path = self.file_path.with_suffix(self.file_path.suffix + '.bak')
            if self.file_path.exists():
                with open(backup_path, 'w', encoding='utf-8') as f:
                    with open(self.file_path, 'r', encoding='utf-8') as original:
                        f.write(original.read())
            
            # Save current content
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for line in self.lines:
                    f.write(line)
            
            self.modified = False
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def get_key(self):
        """Get key input with better character support"""
        try:
            if os.name == 'nt':  # Windows
                import msvcrt
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
                elif key == b'\r':  # Enter
                    return 'ENTER'
                elif key == b'\x08':  # Backspace
                    return 'BACKSPACE'
                elif key == b'\x1b':  # Escape
                    return 'ESCAPE'
                elif key == b'\x13':  # Ctrl+S
                    return 'CTRL_S'
                elif key == b'\x04':  # Ctrl+D
                    return 'CTRL_D'
                elif key == b'\x1a':  # Insert
                    return 'INSERT'
                else:
                    # For regular characters, use input() to handle accents properly
                    try:
                        char = key.decode('cp1252', errors='ignore')  # Windows encoding
                        if char and char.isprintable() and len(char) == 1:
                            return char
                        else:
                            return None
                    except:
                        return None
            else:  # Unix/Linux/Mac
                import termios
                import tty
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
                    elif ch == '\r' or ch == '\n':
                        return 'ENTER'
                    elif ch == '\x7f':  # Backspace
                        return 'BACKSPACE'
                    elif ch == '\x1b':
                        return 'ESCAPE'
                    elif ch == '\x13':  # Ctrl+S
                        return 'CTRL_S'
                    elif ch == '\x04':  # Ctrl+D
                        return 'CTRL_D'
                    elif ch == '\x1a':  # Insert
                        return 'INSERT'
                    else:
                        # Handle special characters and accents
                        if ch and ch.isprintable():
                            return ch
                        else:
                            return None
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            return input("Press Enter to continue...")
    
    def display_header(self):
        """Display editor header"""
        self.terminal_rows, self.terminal_cols = self.get_terminal_size()
        print("═" * self.terminal_cols)
        
        mode_text = f"✏️ {self.get_text('edit_mode')}"
        insert_text = f" | {self.get_text('insert_mode')}" if self.insert_mode else f" | {self.get_text('overwrite_mode')}"
        modified_text = f" | 🔴 {self.get_text('file_modified')}" if self.modified else ""
        
        print(f"{mode_text}{insert_text}{modified_text} 📖 {self.file_path.name} - {len(self.lines)} lines")
        print(f"💡 {self.get_text('press_escape_to_finish')}")
        print("═" * self.terminal_cols)
    
    def display_content(self):
        """Display file content with cursor"""
        available_lines = self.terminal_rows - 6  # Reserve space for header and footer
        
        # Calculate display range
        start_line = max(0, self.current_line - available_lines // 2)
        end_line = min(len(self.lines), start_line + available_lines)
        
        lines_displayed = 0
        for i in range(start_line, end_line):
            if lines_displayed >= available_lines:
                break
                
            line_num = i + 1
            line_content = self.lines[i].rstrip('\n\r')
            
            # Truncate line if too long
            max_width = self.terminal_cols - 10
            if len(line_content) > max_width:
                line_content = line_content[:max_width-3] + "..."
            
            # Show cursor on current line
            if i == self.current_line:
                cursor_char = "█" if self.insert_mode else "▌"
                if self.cursor_pos < len(line_content):
                    display_content = (line_content[:self.cursor_pos] + 
                                     cursor_char + 
                                     line_content[self.cursor_pos:])
                else:
                    display_content = line_content + cursor_char
                
                # Truncate display content
                if len(display_content) > max_width:
                    display_content = display_content[:max_width-3] + "..."
                
                print(f"▶️ {line_num:4d}: {display_content}")
            else:
                print(f"   {line_num:4d}: {line_content}")
            
            lines_displayed += 1
        
        # Fill remaining space
        remaining_lines = available_lines - lines_displayed
        for _ in range(remaining_lines):
            print()
    
    def display_footer(self):
        """Display editor footer with controls"""
        print("═" * self.terminal_cols)
        controls = "⌨️ Controls: ↑↓ Navigate | ←→ Move | Enter New Line | Insert Toggle | F French Chars | Ctrl+S Save | ESC Quit"
        if len(controls) > self.terminal_cols:
            controls = "⌨️ Controls: ↑↓ Navigate | ←→ Move | Enter New Line | F French | Ctrl+S Save | ESC Quit"
        print(controls)
    
    def handle_input(self, key):
        """Handle key input"""
        if key == 'UP':
            if self.current_line > 0:
                self.current_line -= 1
                # Adjust cursor position to fit in new line
                line_length = len(self.lines[self.current_line].rstrip('\n\r'))
                self.cursor_pos = min(self.cursor_pos, line_length)
        
        elif key == 'DOWN':
            if self.current_line < len(self.lines) - 1:
                self.current_line += 1
                # Adjust cursor position to fit in new line
                line_length = len(self.lines[self.current_line].rstrip('\n\r'))
                self.cursor_pos = min(self.cursor_pos, line_length)
        
        elif key == 'LEFT':
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        
        elif key == 'RIGHT':
            line_length = len(self.lines[self.current_line].rstrip('\n\r'))
            if self.cursor_pos < line_length:
                self.cursor_pos += 1
        
        elif key == 'HOME':
            self.cursor_pos = 0
        
        elif key == 'END':
            line_length = len(self.lines[self.current_line].rstrip('\n\r'))
            self.cursor_pos = line_length
        
        elif key == 'INSERT':
            self.insert_mode = not self.insert_mode
        
        elif key == 'F':
            # Handle French characters
            self.handle_special_character_input()
        
        elif key == 'ENTER':
            # Create new line
            current_line_content = self.lines[self.current_line].rstrip('\n\r')
            
            if self.cursor_pos < len(current_line_content):
                # Split line at cursor
                first_part = current_line_content[:self.cursor_pos]
                second_part = current_line_content[self.cursor_pos:]
                
                # Update current line
                self.lines[self.current_line] = first_part + '\n'
                
                # Insert new line
                self.lines.insert(self.current_line + 1, second_part + '\n')
            else:
                # Insert empty line
                self.lines.insert(self.current_line + 1, '\n')
            
            # Move to new line
            self.current_line += 1
            self.cursor_pos = 0
            self.modified = True
        
        elif key == 'BACKSPACE':
            if self.cursor_pos > 0:
                # Delete character before cursor
                current_line_content = self.lines[self.current_line].rstrip('\n\r')
                new_content = (current_line_content[:self.cursor_pos-1] + 
                             current_line_content[self.cursor_pos:])
                self.lines[self.current_line] = new_content + '\n'
                self.cursor_pos -= 1
                self.modified = True
            elif self.current_line > 0:
                # Join with previous line
                prev_line_content = self.lines[self.current_line - 1].rstrip('\n\r')
                current_line_content = self.lines[self.current_line].rstrip('\n\r')
                new_content = prev_line_content + current_line_content
                self.lines[self.current_line - 1] = new_content + '\n'
                self.lines.pop(self.current_line)
                self.current_line -= 1
                self.cursor_pos = len(prev_line_content)
                self.modified = True
        
        elif key == 'CTRL_S':
            if self.save_file():
                print(f"✅ {self.get_text('changes_saved')}")
                input("\n⏸️ Press Enter to continue...")
            return 'SAVE'
        
        elif key == 'ESCAPE':
            if self.modified:
                confirm = input(f"\n⚠️ {self.get_text('confirm_discard')} (y/N): ").strip().lower()
                if confirm == 'y':
                    return 'QUIT'
            else:
                return 'QUIT'
        
        elif len(key) == 1 and key.isprintable():
            # Insert character
            current_line_content = self.lines[self.current_line].rstrip('\n\r')
            
            if self.insert_mode:
                # Insert mode
                new_content = (current_line_content[:self.cursor_pos] + 
                             key + 
                             current_line_content[self.cursor_pos:])
            else:
                # Overwrite mode
                if self.cursor_pos < len(current_line_content):
                    new_content = (current_line_content[:self.cursor_pos] + 
                                 key + 
                                 current_line_content[self.cursor_pos+1:])
                else:
                    new_content = current_line_content + key
            
            self.lines[self.current_line] = new_content + '\n'
            self.cursor_pos += 1
            self.modified = True
        
        elif key == 'SPECIAL_CHAR':
            # Handle special characters with input prompt
            self.handle_special_character_input()
        
        return 'CONTINUE'
    
    def handle_special_character_input(self):
        """Handle special character input with a prompt"""
        print(f"\n🔤 {self.get_text('enter_special_char', 'Enter special character')}:")
        print("Common French characters: é è ê ë à â ä ç ù û ü ô ö î ï")
        char = input("Character: ").strip()
        
        if len(char) == 1 and char.isprintable():
            current_line_content = self.lines[self.current_line].rstrip('\n\r')
            
            if self.insert_mode:
                new_content = (current_line_content[:self.cursor_pos] + 
                             char + 
                             current_line_content[self.cursor_pos:])
            else:
                if self.cursor_pos < len(current_line_content):
                    new_content = (current_line_content[:self.cursor_pos] + 
                                 char + 
                                 current_line_content[self.cursor_pos+1:])
                else:
                    new_content = current_line_content + char
            
            self.lines[self.current_line] = new_content + '\n'
            self.cursor_pos += 1
            self.modified = True
    
    def run(self):
        """Main editor loop"""
        if not self.load_file():
            return False
        
        while True:
            self.clear_screen()
            self.display_header()
            self.display_content()
            self.display_footer()
            
            key = self.get_key()
            result = self.handle_input(key)
            
            if result == 'QUIT':
                break
            elif result == 'SAVE':
                continue
        
        return True

if __name__ == "__main__":
    # Test the editor
    import tempfile
    
    # Create a test file
    test_file = Path(tempfile.gettempdir()) / "test_edit.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Line 1: Test content\n")
        f.write("Line 2: Another line\n")
        f.write("Line 3: Third line\n")
    
    # Test translations
    translations = {
        'edit_mode': 'Edit Mode',
        'insert_mode': 'INSERT',
        'overwrite_mode': 'OVERWRITE',
        'file_modified': 'File has been modified',
        'press_escape_to_finish': 'Press ESC to finish editing',
        'changes_saved': 'Changes saved successfully',
        'confirm_discard': 'Discard all changes?'
    }
    
    # Run editor
    editor = SimpleEditor(test_file, translations)
    editor.run()
    
    # Clean up
    test_file.unlink()
    print("Editor test completed.")
