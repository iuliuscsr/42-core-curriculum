NAME = push_swap.a
PRINTF = ./ft_printf/libftprintf.a
CC = cc
FLAGS = -Wall -Wextra -Werror
RM = rm -f

CFILES = double_linked_list_operations.c input_parsing.c input_parsing_utils.c \
		stack_ops_push.c stack_ops_swap.c stack_ops_rotate.c stack_ops_reverse_rotate.c \
		compute_disorder.c control_struct.c \

OFILES = $(CFILES:.c=.o)

all: $(NAME)

%.o:%.c
	$(CC) $(FLAGS) -c $< -o $@

$(NAME): $(PRINTF) $(OFILES)
	cp $(PRINTF) $(NAME)
	ar rcs $(NAME) $(OFILES)

$(PRINTF):
	make -C ./ft_printf

clean:
	$(RM) $(OFILES)
	make clean -C ./ft_printf

fclean: clean
	$(RM) $(NAME)
	make fclean -C ./ft_printf

re: fclean all

.PHONY: all clean fclean re


