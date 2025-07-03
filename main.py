
import os
from google.adk.tools.tool_context import ToolContext
from rag_agent.agent import root_agent
from rag_agent.tools.get_corpus_info import get_corpus_info
from rag_agent.tools.get_log_content_by_filename import get_log_content_by_filename
from rag_agent.tools.analyze_logs import analyze_logs

def main():
    corpus_name = "example_corpus"
    query = "Show me all ERROR logs from last week"
    invocation_context = {}
    tool_context = ToolContext(invocation_context)

    # Query the corpus
    result = root_agent.tools[0](corpus_name=corpus_name, query=query, tool_context=tool_context)

    if result.get("status") == "success":
        # Save results to a local file
        output_file = 'queried_logs.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in result["results"]:
                f.write(f"{entry['text']}\n")
        print(f"Query results saved to {output_file}")

        # --- Fetch log content and analyze logs ---
        info = get_corpus_info(corpus_name, tool_context)
        filename = info["files"][0]["display_name"]  # Use display_name, not file_id
        log_content = get_log_content_by_filename(filename, corpus_name, tool_context)
        analysis_result = analyze_logs(
            corpus_name=corpus_name,
            tool_context=tool_context,
            log_content=log_content
        )
        print("Log analysis result:", analysis_result)
    else:
        print("Query failed:", result.get("error", "Unknown error"))

if __name__ == "__main__":
    main()