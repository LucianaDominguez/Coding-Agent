TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "readFile",
            "description": "Read the full content of a file. Use this when you need to see what is inside a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the file to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "listFiles",
            "description": "List files and directories in a given path. Use this to explore the filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list."
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "editFile",
            "description": "Create or edit a file. If old_str is empty, creates or overwrites the file. Otherwise replaces the first occurrence of old_str with new_str.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to edit or create."
                    },
                    "oldStr": {
                        "type": "string",
                        "description": "Text to replace. Leave empty to create file."
                    },
                    "newStr": {
                        "type": "string",
                        "description": "New content or replacement text."
                    }
                },
                "required": ["path", "oldStr", "newStr"]
                }
            }
    }
]