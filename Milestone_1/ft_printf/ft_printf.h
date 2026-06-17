/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 17:11:47 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/06 01:06:16 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H
# include <unistd.h>
# include <string.h>
# include <stdlib.h>
# include <stdarg.h>
# include "libft/libft.h"

int	ft_printf(const char *format, ...);
int	convert_hex(unsigned long nb, char specifier);
int	output_hex(char *hex, int i, char specifier, unsigned long nb);
int	output_str(char *str);
int	output_nb(long int nb);

#endif