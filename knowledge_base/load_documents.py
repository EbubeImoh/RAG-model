import os

def load_documents_from_folder(folder_path: str):
    """
    Load all documents from a folder and return a list of document contents.
    """
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Adjust for your document types
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                documents.append(file.read())
    return documents

def load_documents_from_file(file_path: str):
    """
    Load a document from a specific file and return its contents.
    """
    with open(file_path, "r") as file:
        return file.read()