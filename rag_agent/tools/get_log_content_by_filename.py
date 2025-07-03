from google.adk.tools.tool_context import ToolContext
from vertexai import rag
from rag_agent.tools.utils import check_corpus_exists, get_corpus_resource_name


def get_log_content_by_filename(
    filename: str,
    corpus_name: str,
    tool_context: ToolContext,
) -> dict:
    """
    Retrieve the content of a file from a RAG corpus by file name.
    """
    print("Retrieving log content for file:", filename)
    print("Corpus name is :", corpus_name)
    print("Tool context is:", tool_context)

    try:
        # Check if corpus exists
        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist",
                "corpus_name": corpus_name,
            }

        corpus_resource_name = get_corpus_resource_name(corpus_name)
        files = rag.list_files(corpus_resource_name)

        # Print the list of files to inspect their attributes
        print("Files in corpus:", files)

        filename = filename.strip()
        file_obj = next(
            (f for f in files if getattr(f, "name", None) == filename or getattr(f, "display_name", None) == filename),
            None
        )
        if not file_obj:
            return {
                "status": "error",
                "message": f"File '{filename}' not found in corpus."
            }
        # Inspect the file_obj to see its attributes
        print("File object:", file_obj)
        # Use the appropriate attribute from file_obj
        file_resource_name = f"{corpus_resource_name}/ragFiles/{file_obj.name}"  # Replace file_obj.name with the correct attribute if needed
        for f in files:
            print(f"name: {getattr(f, 'name', None)}, display_name: {getattr(f, 'display_name', None)}")
        file_content = rag.get_file(file_resource_name).read()
        if isinstance(file_content, bytes):
            file_content = file_content.decode("utf-8")
        return {
            "status": "success",
            "content": file_content
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }