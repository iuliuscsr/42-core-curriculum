/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 22:25:46 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/22 00:48:19 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "ft_printf/ft_printf.h"

typedef struct s_stack
{
	int				content;
	struct s_stack	*next;
	struct s_stack	*prev;
}	t_stack;

typedef struct s_strg
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	int		size_stack_a;
	int		size_stack_b;
}	t_strg;

// converting input
t_stack	*get_input(int argc, char **argv);
t_stack	*create_stack(char **split_input, int wordindex, t_stack *stack_a);
t_strg	*init_control(t_stack *stack_a, t_stack *stack_b);
int		check_input(char **argv, int wordindex, int letterindex);
int		check_numbers(t_stack *stack_a);
int		ft_atoi_modified(const char *nptr);
void	free_and_exit(void);
void	free_split(char **split_input);
void	del_int(int content);
char	*concenate_input(int argc, char **argv);

//compute disorder
double	compute_disorder(t_stack *stack_a);

// linked list operations
void	ft_stackadd_back(t_stack **lst, t_stack *new);
void	ft_stackadd_front(t_stack **lst, t_stack *new);
void	ft_stackclear(t_stack **lst, void (*del)(int));
void	ft_stackdelone(t_stack *lst, void (*del)(int));
t_stack	*ft_stacknew(int content);

// stack operations -- swap
void	sa(t_stack **stack_a);
void	sb(t_stack **stack_b);
void	ss(t_stack **stack_a, t_stack **stack_b);

// stack operations -- push
void	pa(t_stack **stack_a, t_stack **stack_b);
void	pb(t_stack **stack_a, t_stack **stack_b);

// stack operations -- rotate
void	ra(t_stack **stack_a);
void	rb(t_stack **stack_b);
void	rr(t_stack **stack_a, t_stack **stack_b);

// stack operations -- reverse_rotate
void	rra(t_stack **stack_a);
void	rrb(t_stack **stack_b);
void	rrr(t_stack **stack_a, t_stack **stack_b);

// simple algorithm
void	bubble_sort(t_stack **stack_a);
void	selection_sort(t_strg *config);
int		find_min(t_stack *temp);

#endif
