*This project has been created as part of the 42 curriculum by jmalsam*

# libft

## Description 
The ft_libft is a library created within the 42 core curriculum, using a set of libc functions as its fundament, adhering strictly to their definitions in the man page. Furthermore there are plenty of additional functions to modify strings or memory which are not included in the libc as well as functions to manipulate linked lists.

## Overview

<details>
<summary>Libc_Functions</summary>

| Function | Description |
|---|---|
| `ft_isalnum.c` | checks if a character is alphabetical or numeric |
| `ft_isalpha.c` | checks if a given character is alphabetical |
| `ft_isdigit.c` | checks if a given character is numeric |
| `ft_isascii.c` | checks if a given character is within ASCII |
| `ft_isprint.c` | checks if a given character is printable |
| `ft_strlen.c` | checks the length of a given string |
| `ft_memset.c` | fills the first n bytes of a pointer with the byte c |
| `ft_bzero.c` | fills the first n bytes of a pointer with zeros |
| `ft_memmove.c` | copies n bytes from src to dest, overlap allowed |
| `ft_memcpy.c` | copies n bytes from src to dest, overlap forbidden |
| `ft_strlcpy.c` | copies n bytes from a string src to a string dest, nullterminating the string after |
| `ft_strlcat.c` | concatenates n bytes from a string src to a string dest, nullterminating the string after |
| `ft_toupper.c` | makes upper case letter if c is lowercase |
| `ft_tolower.c` | mkaes lower case letter if c is upper case |
| `ft_strchr.c` | returns a pointer to the index of the first occurance of c in a string |
| `ft_strrchr.c-` | returns a pointer to the index of the last occurance of c in a string |
| `ft_strncmp.c` | compares two strings until the n byte
| `ft_memchr.c` | returns a pointer to the index of the first occurance of c |
| `ft_memcmp.c` | compares two pointers until the n byte |
| `ft_strnstr.c` | returns a pointer to the index of the first occurance of a substring |
| `ft_atoi.c` | converts a given string to integer |
| `ft_calloc.c` | allocates memory, initializing it with zeros |
| `ft_strdup.c` | returns a pointer to a new string which is a duplicate of s |
</details>

<details>
<summary>Additional_Functions</summary>

| Function | Description
|---|---|
| `ft_substr.c` | returns a substring from string s |
| `ft_strjoin.c` | concatenates two strings and returns a new string as result |
| `ft_strtrim.c` | trims a given string removing letters of a given set |
| `ft_split.c` | creates an array of strings, which holds strings seperated by a given seperator |
| `ft_itoa.c` | returns a string representing the given integer |
| `ft_strmapi.c` | applies a given function f to each character of a string, returning a new string |
| `ft_striteri.c` | applies a given function f to each character of a string |
| `ft_putchar_fd.c` | writes a given character with a given descriptor |
| `ft_putstr_fd.c` | writes a given string with a given descriptor |
| `ft_putendl_fd.c` | writes a string followed by a new line with a given descriptor |
| `ft_putnbr_fd.c` | writes a given string, with a given descriptor |

</details>

<details>
<summary>Linked_List</summary>

| Function | Description
|---|---|
| `ft_lstnew.c` | allocates memory for a new node initializing it with given content |
| `ft_lstadd_front.c` | adds a node at the beginning of the list |
| `ft_lstsize.c` | gets the length of a list |
| `ft_lstlast.c` | returns the last node of the list |
| `ft_lstadd_back.c` | adds a node at the end of the list |
| `ft_lstdelone.c` | frees a node and its content |
| `ft_lstclear.c` | frees a node and all its successors |
| `ft_lstiter.c` | applies a function f to the content of each node |
| `ft_lstmap.c` | applies a function f to the content of each node and creates a new list of the successive applications |

</details>

## Instructions

### Compile
In order to create the library use

```bash
make
```

### Commands
You can apply the following commands in order to work with your library

`make clean`	removes .o files  
`make fclean`	removes .o files + created library  
`make re`		rebuilds the library  

### Include Header
In order to use the library, you have to include it first 

```c
#Include "libft.h
```

### Execute
To run the programm you need to create the library as shown above and compile your .c file with the included Header

```bash
cc -Wall -Wextra -Werror your_file.c -L. -lft
```

after that you execute the created file using

`./a.out`

## Resources

- linux man page
- learn-c.org
- makefiletutorial.com
- github.com
- geeksforgeeks.org
- stackoverflow.com

### AI usage

Gemini was used for code review as well as getting detailed explanation about abstract concepts like linked lists, memory allocation and pointers. In addition to that it provided specific edge cases which were not included in francinette. No code has been copied and it purely served as a reviewing tool.
