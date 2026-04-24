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

