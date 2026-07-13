### Purpose Summary

The `sage.services.module_docs` module is responsible for generating per-file documentation in a batch process. It leverages asynchronous programming to handle multiple files concurrently while ensuring that only documentable files are processed. The module interacts with other services such as `doc_generator` and `git_ops` to fetch source files and generate documentation, respectively.

### Key Functions/Classes

| Function/Class | Description |
|----------------|-------------|
| `generate_module_docs(local_path: Path) -> list[dict]` | Asynchronously generates documentation for all documentable files in the specified local path. Returns a list of dictionaries containing the file paths and their corresponding documentation content. |

### Notable Dependencies or Side Effects

- **Dependencies**: This module depends on the following services:
  - `sage.services.doc_generator.generate_module_doc`: Used to generate documentation for individual files.
  - `sage.services.git_ops.list_source_files`: Used to list source files in the specified local path.

- **Side Effects**:
  - Logs information about the progress and results of the documentation generation process using `sage.core.logging.get_logger`.
  - Handles exceptions during documentation generation, logging warnings for failures.
  - Uses an asynchronous semaphore to limit concurrency, ensuring that only a specified number of files are processed at a time.

This module is integral to the larger system by providing a scalable and efficient way to generate documentation for multiple source files, enhancing maintainability and readability.