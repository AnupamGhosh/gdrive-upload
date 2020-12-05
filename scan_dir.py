from pathlib import Path

class DirectoryScanner():
  def dir_found(self, path: Path):
    print(f'{path.name}:{path.stat().st_ino} is a directory inside {path.parent.name}')

  def file_found(self, path: Path):
    print(f'{path.name}:{path.stat().st_ino} is a file inside {path.parent.name}')

  def scan(self, dir_path):
    path = Path(dir_path)
    if path.is_file():
      self.file_found(path)
      return
    
    queue = [path]
    while queue:
      parent = queue.pop()
      for path in parent.iterdir():
        if path.is_dir():
          self.dir_found(path)
          queue.append(path)
        elif path.is_file():
          self.file_found(path)

if __name__ == "__main__":
  secret_path = '/Users/anupamghosh/workspace/fun/gdrive-upload/secrets/'
  scanner = DirectoryScanner()
  scanner.scan(secret_path)