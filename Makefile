NAME = push_swap.a
PRINTF = ./ft_printf/libftprintf.a
CC = cc
FLAGS = -Wall -Wextra -Werror -I.
RM = rm -f

CFILES = input_parsing/input_parsing.c input_parsing/input_parsing_utils.c \
		operations/stack_ops_push.c operations/stack_ops_swap.c operations/stack_ops_rotate.c operations/stack_ops_reverse_rotate.c \
		operations/double_linked_list_operations.c \
		compute_disorder.c control_struct.c \
		algorithms/bubble_sort.c algorithms/selection_sort.c \

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


