from pathlib import Path

class DirectoryScanner():
  def dir_found(self, path: Path):
    print(f'{path.name}:{path.stat().st_ino} is a directory inside {path.parent.name}')

  def file_found(self, path: Path):
    print(f'{path.name}:{path.stat().st_ino} is a file inside {path.parent.name}')

  def scan(self, dir_path):
    queue = [Path(dir_path)]
    while queue:
      parent = queue.pop()
      if parent.is_file():
        self.file_found(parent)
      elif parent.is_dir():
        self.dir_found(parent)
        for path in parent.iterdir():
          queue.append(path)

if __name__ == "__main__":
  secret_path = '/Users/anupamghosh/workspace/fun/gdrive-upload/secrets/'
  scanner = DirectoryScanner()
  scanner.scan(secret_path)