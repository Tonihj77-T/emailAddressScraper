class FileHandler:
    def read_lines(self, file_path):
        """Read lines from a file"""
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
    
    def write_lines(self, file_path, lines):
        """Write lines to a file"""
        try:
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(f"{line}\n")
            return True
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")
            return False