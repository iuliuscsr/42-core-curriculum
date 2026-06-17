/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 15:47:34 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/28 13:01:49 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	void	*array;

	if (nmemb != 0 && size > (size_t)-1 / nmemb)
		return (NULL);
	array = malloc(size * nmemb);
	if (!array)
		return (NULL);
	ft_bzero(array, nmemb * size);
	return (array);
}
