# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/22 16:06:24 by jawosylu          #+#    #+#              #
#    Updated: 2026/05/27 05:01:46 by jmalsam          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = push_swap.a
PRINTF = ./ft_printf/libftprintf.a
CC = cc
FLAGS = -g -Wall -Wextra -Werror -I.
RM = rm -f

CFILES = input_parsing/input_parsing.c input_parsing/input_parsing_utils.c \
		operations/stack_ops_push.c operations/stack_ops_swap.c operations/stack_ops_rotate.c operations/stack_ops_reverse_rotate.c \
		operations/double_linked_list_operations.c \
		dispatch_algorithm.c env_setup.c \
		algorithms/algorithm_utils.c \
		algorithms/bubble_sort.c \
		algorithms/chunk_sort.c \
		algorithms/radix_sort.c \
		algorithms/selection_sort.c \
		bonus/get_next_line.c \
		bonus/checker_bonus.c \
		bonus/checker_bonus_utils.c \


OFILES = $(CFILES:.c=.o)

all: $(NAME)
	@clear
	@printf "██████╗ ██╗   ██╗███████╗██╗  ██╗    ███████╗██╗    ██╗ █████╗ ██████╗ \n"
	@printf "██╔══██╗██║   ██║██╔════╝██║  ██║    ██╔════╝██║    ██║██╔══██╗██╔══██╗\n"
	@printf "██████╔╝██║   ██║███████╗███████║    ███████╗██║ █╗ ██║███████║██████╔╝\n"
	@printf "██╔═══╝ ██║   ██║╚════██║██╔══██║    ╚════██║██║███╗██║██╔══██║██╔═══╝ \n"
	@printf "██║     ╚██████╔╝███████║██║  ██║    ███████║╚███╔███╔╝██║  ██║██║     \n"
	@printf "╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     \n"
	@echo push_swap created
	@echo Run make fclean for removing .o files
	@$(CC) $(FLAGS) main.c $(NAME) -o push_swap

%.o:%.c
	@$(CC) $(FLAGS) -c $< -o $@

$(NAME): $(PRINTF) $(OFILES)
	@cp $(PRINTF) $(NAME)
	@ar rcs $(NAME) $(OFILES)

$(PRINTF):
	@make --no-print-directory -C ./ft_printf

clean:
	@$(RM) $(OFILES)
	@make --no-print-directory clean -C ./ft_printf
	@echo .o files cleaned up.

fclean: clean
	@$(RM) $(NAME)
	@make --no-print-directory fclean -C ./ft_printf
	@echo All cleaned up.

re: fclean all

bonus: $(NAME)
	@cc checker_bonus.c push_swap.a -o checker
	@echo "checker was created"
	@make --no-print-directory fclean

.PHONY: all clean fclean re
