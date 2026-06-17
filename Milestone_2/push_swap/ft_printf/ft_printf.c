/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 17:10:44 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/07 12:34:58 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	check_format_specifier(const char *format, int *i, va_list args)
{
	int		countoutput;

	countoutput = 0;
	(*i)++;
	if (format[*i] == 'd' || format[*i] == 'i')
		countoutput = output_nb(va_arg(args, int));
	else if (format[*i] == 'u')
		countoutput = output_nb(va_arg(args, unsigned int));
	else if (format[*i] == 's')
		countoutput = output_str(va_arg(args, char *));
	else if (format[*i] == 'c')
		countoutput = (ft_putchar_fd((char)va_arg(args, int), 1), 1);
	else if (format[*i] == '%')
		countoutput = (ft_putchar_fd('%', 1), 1);
	else if (format[*i] == 'X')
		countoutput = convert_hex(va_arg(args, unsigned int), 'X');
	else if (format[*i] == 'x')
		countoutput = convert_hex(va_arg(args, unsigned int), 'x');
	else if (format[*i] == 'p')
		countoutput = convert_hex(va_arg(args, unsigned long), 'p');
	(*i)++;
	return (countoutput);
}

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int		i;
	int		countoutput;

	if (!format)
		return (-1);
	va_start(args, format);
	i = 0;
	countoutput = 0;
	while (format[i] != '\0')
	{
		if (format[i] == '%' && format[i + 1] != '\0')
			countoutput += check_format_specifier(format, &i, args);
		if (countoutput == -1)
			return (countoutput);
		else
		{
			ft_putchar_fd(format[i], 1);
			countoutput++;
			i++;
		}
	}
	va_end(args);
	return (countoutput);
}
