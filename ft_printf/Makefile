NAME = libftprintf.a
LIBFT = ./libft/libft.a 
CC = cc
FLAGS = -Wall -Wextra -Werror
RM = rm -f 

CFILES = ft_printf.c hex_conversion.c output_functions.c

OFILES = $(CFILES:.c=.o)

all: $(NAME)

%.o:%.c
	$(CC) $(FLAGS) -c $< -o $@

$(NAME): $(LIBFT) $(OFILES)
	cp $(LIBFT) $(NAME)
	ar rcs $(NAME) $(OFILES)

$(LIBFT):
	make -C ./libft

clean:
	$(RM) $(OFILES)
	make clean -C ./libft

fclean: clean
	$(RM) $(NAME)
	make fclean -C ./libft

re: fclean all

.PHONY: all clean fclean re



