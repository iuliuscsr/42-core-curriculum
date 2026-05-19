NAME = libft.a
CC = cc
RM = rm -f
CFLAGS = -Wall -Wextra -Werror

LIBC_FUNCTIONS = ft_isalnum.c ft_isalpha.c ft_isdigit.c ft_isascii.c \
ft_isprint.c ft_strlen.c ft_memset.c ft_bzero.c ft_memmove.c ft_memcpy.c \
ft_strlcpy.c ft_strlcat.c ft_toupper.c ft_tolower.c ft_strchr.c \
ft_strrchr.c ft_strncmp.c ft_memchr.c ft_memcmp.c ft_strnstr.c ft_atoi.c \
ft_calloc.c ft_strdup.c 

ADDITIONAL_FUNCTIONS = ft_substr.c ft_strjoin.c ft_strtrim.c ft_split.c ft_itoa_modified.c \
ft_strmapi.c ft_striteri.c ft_putchar_fd.c ft_putstr_fd.c ft_putendl_fd.c ft_itoa.c \
ft_putnbr_fd.c

LINKED_LIST = ft_lstnew.c ft_lstadd_front.c ft_lstsize.c ft_lstlast.c \
ft_lstadd_back.c ft_lstdelone.c ft_lstclear.c ft_lstiter.c ft_lstmap.c 

CFILES = $(LIBC_FUNCTIONS) $(ADDITIONAL_FUNCTIONS) $(LINKED_LIST)

OFILES = $(CFILES:.c=.o)

all: $(NAME)

%.o:%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(NAME): $(OFILES)
	ar rcs $(NAME) $(OFILES)

clean:
	$(RM) $(OFILES)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re