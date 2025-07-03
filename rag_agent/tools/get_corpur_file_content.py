import json

from vertexai import rag

from rag_agent.tools import get_corpus_info


def download_corpus_logs_as_json(corpus_name, tool_context, output_json_path):
    # Get corpus info (including file list)
    """
        Downloads all file contents from a specified corpus and saves them as a JSON file.

        Args:
            corpus_name (str): The name of the corpus to fetch files from.
            tool_context: Context or configuration required to access the corpus.
            output_json_path (str): Path to the output JSON file where logs will be saved.

        Returns:
            None. Prints status messages and writes file contents to the specified JSON file.
        """
    corpus_info = get_corpus_info(corpus_name, tool_context)
    if corpus_info.get("status") != "success":
        print(f"Error: {corpus_info.get('message')}")
        return

    corpus_resource_name = corpus_name  # Adjust if needed
    files = corpus_info.get("files", [])
    logs = []

    for file_info in files:
        file_id = file_info["file_id"]
        file_resource_name = f"{corpus_resource_name}/ragFiles/{file_id}"
        try:
            file_content = rag.get_file(file_resource_name).read()
            if isinstance(file_content, bytes):
                file_content = file_content.decode("utf-8")
            logs.append({
                "file_id": file_id,
                "display_name": file_info.get("display_name", ""),
                "content": file_content
            })
        except Exception as e:
            print(f"Failed to fetch file {file_id}: {e}")

    # Save all logs to a local JSON file
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(logs)} log files to {output_json_path}")
