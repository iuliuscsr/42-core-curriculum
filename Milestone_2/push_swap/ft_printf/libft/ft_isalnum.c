/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalnum.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/15 12:43:57 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/16 13:58:34 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include "libft.h"

int	ft_isalnum(int c)
{
	int	istrue;

	istrue = 0;
	if (ft_isalpha(c) == 1 || ft_isdigit(c) == 1)
		istrue = 1;
	return (istrue);
}
