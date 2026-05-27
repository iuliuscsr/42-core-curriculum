/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 22:25:46 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/27 15:31:06 by jawosylu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "ft_printf/ft_printf.h"

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 3
# endif

typedef struct s_env
{
	int		adaptive;
	int		simple;
	int		medium;
	int		complex;
	int		bench;
	int		print_operations;
	int		total_ops;
	int		total_sa;
	int		total_sb;
	int		total_ss;
	int		total_pa;
	int		total_pb;
	int		total_ra;
	int		total_rb;
	int		total_rr;
	int		total_rra;
	int		total_rrb;
	int		total_rrr;
	double	disorder;
	char	*strategy1;
	char	*strategy2;
	int		checker;
}	t_env;

typedef struct s_stack
{
	int				content;
	int				index;
	struct s_stack	*next;
	struct s_stack	*prev;
}	t_stack;

// converting input
t_stack	*get_input(int argc, char **argv, t_env *env);
t_stack	*create_stack(char **split_input, int wordindex, t_stack *stack_a);
int		check_input(char **argv, int wordindex, int letterindex);
int		check_numbers(t_stack *stack_a);
long	ft_atoi_modified(const char *nptr);
void	free_and_exit(void);
void	free_split(char **split_input);
void	del_int(int content);
char	*concenate_input(int argc, char **argv, int wordindex);

// linked list operations
void	ft_stackadd_back(t_stack **lst, t_stack *new);
void	ft_stackadd_front(t_stack **lst, t_stack *new);
void	ft_stackclear(t_stack **lst, void (*del)(int));
void	ft_stackdelone(t_stack *lst, void (*del)(int));
t_stack	*ft_stacknew(int content);

// stack operations -- swap
void	sa(t_stack **stack_a, t_env *env);
void	sb(t_stack **stack_b, t_env *env);
void	ss(t_stack **stack_a, t_stack **stack_b, t_env *env);

// stack operations -- push
void	pa(t_stack **stack_a, t_stack **stack_b, t_env *env);
void	pb(t_stack **stack_a, t_stack **stack_b, t_env *env);

// stack operations -- rotate
void	ra(t_stack **stack_a, t_env *env);
void	rb(t_stack **stack_b, t_env *env);
void	rr(t_stack **stack_a, t_stack **stack_b, t_env *env);

// stack operations -- reverse_rotate
void	rra(t_stack **stack_a, t_env *env);
void	rrb(t_stack **stack_b, t_env *env);
void	rrr(t_stack **stack_a, t_stack **stack_b, t_env *env);

// simple algorithm
void	bubble_sort(t_stack **stack_a, t_stack **stack_b, t_env *env);
void	selection_sort(t_stack **stack_a, t_stack **stack_b, t_env *env);

// medium algorithm
void	chunk_sort(t_stack **stack_a, t_stack **stack_b, t_env *env);

//complex algorithm
void	radix_sort(t_stack **stack_a, t_stack **stack_b, t_env *env);

// exec program
void	ft_normalize(t_stack *stack, int size);
double	compute_disorder(t_stack *stack_a);
void	init_env(t_env *stack);
void	print_bench(t_env *env);
int		stack_size(t_stack **stack);
int		is_sorted(t_stack **stack);

//dispatch algorithm
void	dispatch_agorithm(t_stack **stack_a, t_stack **stack_b, t_env *env);
void	adaptive(t_stack **stack_a, t_stack **stack_b,
			t_env *env, double disorder);
void	set_simple(t_env *env);
void	set_medium(t_env *env);
void	set_complex(t_env *env);
int		check_flags(int argc, char **argv, t_env *env);

#endif
