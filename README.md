*This project has been created as part of the 42 curriculum by jmalsam*

# ft_printf

## Description

The **ft_printf** project is part of the 42 core curriculum and consists of recreating the well-known `printf()` function from the C standard library.

The goal of this project is to understand and implement **variadic functions** using `va_list`, while building a clean and modular output system based on low-level functions like `write()`.

This implementation supports a subset of the original `printf()` functionality and focuses on correct formatting, memory safety, and extensibility.

## Overview

<details>
<summary>Supported_Conversions</summary>

| Conversion | Description                                                         |
| ---------- | ------------------------------------------------------------------- |
| `%c`       | prints a single character                                           |
| `%s`       | prints a string (handles NULL as `(null)`)                          |
| `%p`       | prints a pointer address in hexadecimal format (`0x...` or `(nil)`) |
| `%d`       | prints a decimal (base 10) number                                   |
| `%i`       | prints an integer in base 10                                        |
| `%u`       | prints an unsigned decimal number                                   |
| `%x`       | prints a hexadecimal number (lowercase)                             |
| `%X`       | prints a hexadecimal number (uppercase)                             |
| `%%`       | prints a percent sign                                               |

</details>

<details>
<summary>Core_Functions</summary>

| Function                 | Description                                    |
| ------------------------ | ---------------------------------------------- |
| `ft_printf.c`            | main function handling parsing and output      |
| `check_format_specifier` | detects and dispatches format specifiers       |
| `output_nb`              | converts and prints numbers using `ft_itoa_modified`|
| `output_str`             | prints strings with NULL protection            |
| `convert_hex`            | converts numbers to hexadecimal representation |
| `output_hex`             | prints formatted hexadecimal output            |
| `ft_putchar_fd`          | writes a single character to stdout            |

</details>

<details>
<summary>Variadic_Handling</summary>

| Function/Macro | Description                   |
| -------------- | ----------------------------- |
| `va_start`     | initializes the argument list |
| `va_arg`       | retrieves the next argument   |
| `va_end`       | cleans up the argument list   |

</details>

## Algorithm & Design Choices

The implementation is based on a **linear parser** that iterates through the format string:

* Regular characters are printed directly using `ft_putchar_fd`
* When encountering `%`, the next character is interpreted as a format specifier
* A dispatcher function (`check_format_specifier`) routes the argument to the correct output function

### Key Design Decisions

**1. Modular Output Functions**
Each data type is handled in its own function (`output_nb`, `output_str`, `convert_hex`, etc.), making the code easier to maintain and extend.

**2. Number Handling via `ft_itoa_modified`**
All decimal numbers are converted using `ft_itoa_modified`, which was adapted to accept a `long int`.
This allows handling both:

* signed integers (`%d`, `%i`)
* unsigned integers (`%u`) by implicit casting

**3. Hexadecimal Conversion**
Hex values are constructed manually:

* Digits are stored in a buffer in reverse order
* Then printed in correct order via `output_hex`
* Supports lowercase (`x`), uppercase (`X`), and pointer (`p`) formats

**4. Pointer Handling**
Pointers are printed with:

* prefix `0x`
* special case `(nil)` when the pointer is `NULL`

**5. Return Value Tracking**
Each output function returns the number of printed characters, which is accumulated in `ft_printf` to match the behavior of the original `printf`.

## Instructions

### Compile

```bash
make
```

### Commands

`make clean`	removes object files
`make fclean`	removes object files + library
`make re`		rebuilds the project

### Include Header

```c
#include "ft_printf.h"
```

### Execute

Compile your program with:

```bash
cc -Wall -Wextra -Werror your_file.c -L. -lftprintf
```

Run it:

```bash
./a.out
```

## Example Usage

```c
#include "ft_printf.h"

int main(void)
{
    ft_printf("Char: %c\n", 'A');
    ft_printf("String: %s\n", "Hello");
    ft_printf("Number: %d\n", -42);
    ft_printf("Unsigned: %u\n", 42);
    ft_printf("Hex: %x\n", 255);
    ft_printf("Pointer: %p\n", NULL);
    return (0);
}
```

## Resources

* linux man pages (`man 3 printf`)
* cppreference.com
* learn-c.org
* geeksforgeeks.org
* stackoverflow.com

### AI usage

Gemini was used as a **supporting tool** for:

* reviewing code structure and modularization
* explaining variadic arguments (`va_list`)
* identifying edge cases (NULL strings, zero values)
* regarding any questions it was instructed to not write code as an answer 
