# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/22 16:06:24 by jawosylu          #+#    #+#              #
#    Updated: 2026/05/27 17:45:07 by jawosylu         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = push_swap.a
PRINTF = ./ft_printf/libftprintf.a
CC = cc
FLAGS = -Wall -Wextra -Werror -I.
RM = rm -f
BNAME = bonus_checker.a

CFILES = input_parsing/input_parsing.c input_parsing/input_parsing_utils.c \
		operations/stack_ops_push.c operations/stack_ops_swap.c operations/stack_ops_rotate.c operations/stack_ops_reverse_rotate.c \
		operations/double_linked_list_operations.c \
		dispatch_algorithm.c env_setup.c \
		algorithms/algorithm_utils.c \
		algorithms/bubble_sort.c \
		algorithms/chunk_sort.c \
		algorithms/radix_sort.c \
		algorithms/selection_sort.c \

BFILES = bonus/get_next_line_bonus.c \
		bonus/checker_bonus.c \
		bonus/checker_bonus_utils.c \

BOFILES = $(BFILES:.c=.o)

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

$(BNAME): $(PRINTF) $(BOFILES) $(NAME)
	@cp $(PRINTF) $(BNAME)
	@ar rcs $(BNAME) $(BOFILES)

$(PRINTF):
	@make --no-print-directory -C ./ft_printf

clean:
	@$(RM) $(OFILES)
	@$(RM) $(BOFILES)
	@make --no-print-directory clean -C ./ft_printf
	@echo .o files cleaned up.

fclean: clean
	@$(RM) $(NAME)
	@$(RM) $(BNAME)
	@make --no-print-directory fclean -C ./ft_printf
	@echo All cleaned up.

re: fclean all

bonus: $(BNAME)
	@$(CC) $(FLAGS) bonus/checker_bonus.c  $(NAME) $(BNAME) -o checker
	@echo "checker was created"
	@make --no-print-directory fclean

.PHONY: all clean fclean re
