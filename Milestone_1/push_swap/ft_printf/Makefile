NAME = libftprintf.a
LIBFT = ./libft/libft.a
CC = cc
FLAGS = -Wall -Wextra -Werror
RM = rm -f

CFILES = ft_printf.c hex_conversion.c output_functions.c

OFILES = $(CFILES:.c=.o)

all: $(NAME)
	@echo ft_printf created

%.o:%.c
	@$(CC) $(FLAGS) -c $< -o $@

$(NAME): $(LIBFT) $(OFILES)
	@cp $(LIBFT) $(NAME)
	@ar rcs $(NAME) $(OFILES)

$(LIBFT):
	@make --no-print-directory -C ./libft

clean:
	@$(RM) $(OFILES)
	@make clean --no-print-directory -C ./libft

fclean: clean
	@$(RM) $(NAME)
	@make fclean --no-print-directory -C ./libft

re: fclean all

.PHONY: all clean fclean re



