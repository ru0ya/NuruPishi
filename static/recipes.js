#!/usr/bin/node

window.onLoad = function() {
	const searchContainer = document.querySelector('.search-container');
	const recipeContainer = document.querySelector('.recipe-container');

	window.addEventListener('scroll', () => {
		const offsetY = window.scrollY;
		searchContainer.style.transform = `translateY(${offsetY * 0.1}px)`;
		recipeContainer.style.transform = `translateY(${offsetY * 0.4}px)`;
	}


