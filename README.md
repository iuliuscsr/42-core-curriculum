*This project has been created as part of the 42 curriculum by jmalsam*

# get_next_line

## Description

The **get_next_line** project is part of the 42 core curriculum and focuses on implementing a function that reads from a file descriptor **one line at a time**.

The objective of this project is to understand:

* static variables
* file descriptor handling
* dynamic memory allocation
* buffer management
* efficient string manipulation

The function returns exactly one line per call, including the newline character (`\n`) if present, while preserving unread content for future calls.

## Overview

<details>
<summary>Core_Functions</summary>

| Function              | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| `get_next_line.c`     | main logic for reading and extracting lines                |
| `get_next_line`       | reads from file descriptor and returns the next line       |
| `edit_strings`        | splits stored data into current line and remaining content |
| `extract_line`        | extracts a line ending with `\n`                           |
| `extract_last`        | extracts the remaining content at EOF                      |
| `ft_strchr_modified`  | searches for newline characters                            |
| `ft_strjoin_modified` | appends newly read data to the stored buffer               |
| `ft_substr`           | creates substrings                                         |
| `ft_strlcpy`          | safely copies strings                                      |
| `ft_strlen`           | calculates string length                                   |
| `ft_free_str1`        | safely frees and nullifies pointers                        |

</details>

<details>
<summary>Key_Concepts</summary>

| Concept            | Description                                      |
| ------------------ | ------------------------------------------------ |
| Static variable    | preserves unread data between function calls     |
| Dynamic allocation | allocates memory for buffers and extracted lines |
| Buffered reading   | reads data in chunks of `BUFFER_SIZE`            |
| Memory management  | prevents leaks and invalid memory access         |
| Line extraction    | isolates exactly one line per function call      |

</details>

## Algorithm & Design Choices

The implementation is based on a **persistent static storage system**.

A static string (`src`) stores all unread content between function calls.
Each call to `get_next_line` reads additional data until:

* a newline (`\n`) is found
* or EOF is reached

### Step-by-step Process

1. **Initialize buffer**

   * Allocate a temporary buffer of size `BUFFER_SIZE + 1`

2. **Read from file descriptor**

   * `read()` appends content into `buffer`
   * `buffer` is concatenated to `src` using `ft_strjoin_modified`

3. **Search for newline**

   * `ft_strchr_modified` returns:

     * index of `\n`
     * `-1` if none exists## Resources

4. **Extract the line**

   * `edit_strings` separates:

     * the line to return
     * the remaining unread content

5. **Store leftovers**

   * Remaining data after the newline stays inside `src`
   * This allows the next call to continue exactly where the previous one stopped

6. **Handle EOF**

   * If no newline exists and EOF is reached:

     * remaining content is returned once
     * afterwards `NULL` is returned

## Important Design Decisions

### Static Variable Usage

The static variable `src` is the core of the project:

* it persists between function calls
* stores partially read data
* prevents data loss between reads

Without static storage, line-by-line reading would not work correctly.

### Modular Extraction Logic

The extraction process was separated into:

* `extract_line`
* `extract_last`
* `edit_strings`

This improves:

* readability
* debugging
* memory safety
* extensibility

### Safe Memory Management

Memory is carefully managed throughout the project:

* old strings are freed after concatenation
* helper function `ft_free_str1` safely frees and nullifies pointers
* failed allocations clean up previously allocated memory
* edge cases avoid leaks and dangling pointers

### Custom String Functions

Custom utility functions were implemented instead of libc equivalents:

* `ft_strlen`
* `ft_strlcpy`
* `ft_substr`
* `ft_strjoin_modified`

This improves understanding of:

* string manipulation
* pointer arithmetic
* dynamic allocation

## Instructions

### Compile

```bash id="80r9r5"
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
get_next_line.c get_next_line_utils.c
```

### Include Header

```c id="nqzntj"
#include "get_next_line.h"
```

### Execute

Example program:

```c id="j9cgo8"
#include "get_next_line.h"
#include <fcntl.h>

int	main(void)
{
	int		fd;
	char	*line;

	fd = open("test.txt", O_RDONLY);
	while ((line = get_next_line(fd)) != NULL)
	{
		printf("%s", line);
		free(line);
	}
	close(fd);
	return (0);
}
```

Run executable:

```bash id="3l1spw"
./a.out
```

## Example Behavior

Input file:

```id="31cn0h"
Hello
World
42
```

Returned values per function call:

```id="v5i7m0"
"Hello\n"
"World\n"
"42"
NULL
```

## Edge Cases Handled

* invalid file descriptors
* `BUFFER_SIZE <= 0`
* empty files
* files without trailing newline
* `read()` errors
* allocation failures
* NULL pointer protection

## Limitations

* Mandatory version supports only a single file descriptor
* No multi-fd bonus handling
* Performance depends on chosen `BUFFER_SIZE`

## Resources

* linux man pages (`man 2 read`)
* geeksforgeeks.org
* stackoverflow.com
* valgrind.org
* codequoi.com
* github.com

### AI usage

AI was used as a **supporting tool** for:

* understanding static variables and buffer behavior
* reviewing memory management and edge cases
* debugging segfaults and NULL-check failures
* validating algorithm structure

No code was copied. AI was only used to **support learning and debugging**, especially regarding string handling, dynamic memory allocation, and pointer safety.

