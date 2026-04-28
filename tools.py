import os

def readFile (filename: str) -> dict:
    """
    Lee el contenido completo de un archivo.
    :param filename: ruta al archivo (absoluta o relativa al cwd).
    :return: dict con 'filePath' y 'content'.
    """

    try:
        with open(filename, "r") as f:
            content = f.read()
        return {
            "filePath": filename,
            "content": content
    }
    except Exception as e:
        return {
            "error": str(e)
        }
    

def listFiles(path: str) -> dict:
    """
    List files and directories in a given path.

    Use this to explore the file system.
    DO NOT use this to read file contents.

    :param path: Directory path.
    :return: dict with path and list of files.
    """
    
    try:
        absPath = os.path.abspath(path)

        files =[]
        for item in os.listdir(path):
            fullPath = os.path.join(path, item)

            files.append({
                "filename": item,
                "type": "directory" if os.path.isdir(fullPath) else "file"
            
            })

        return {
            "path": absPath,
            "files": files
        }
    except Exception as e:
        return {"error": str(e)}
    
def editFile(path: str, oldStr: str, newStr: str) -> dict:
    """
    Edit or create a file.

    - If oldStr is empty: create or overwrite the file with newStr.
    - If oldStr is provided: replace the FIRST occurrence with newStr.

    Use this to modify files or create new ones.

    :param path: File path.
    :param oldStr: Text to replace (empty to create).
    :param newStr: New content or replacement.
    :return: dict describing the action taken.
    """
    try:
        if oldStr == "":
            with open(path, "w", encoding="utf-8") as f:
                f.write(newStr)

            return{
            "action": "createdFile",
            "path": path
            }
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if oldStr not in content:
            return{
                "action": "oldStringNotFound",
                "path": path,
            }
        
        updated = content.replace(oldStr, newStr, 1)

        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        
        return{
            "action" : "edited",
            "path": path
        }
    except Exception as e:
        return {"error": str(e)}

         