$(document).ready(function() {

	$('.dropdown-toggle').click(function(e) {
	  e.preventDefault();
	  e.stopPropagation();
	  $(this).closest('.search-dropdown').toggleClass('open');
	});

	$('.dropdown-menu > li > a').click(function(e) {
	  e.preventDefault();
	  var clicked = $(this);
	  clicked.closest('.dropdown-menu').find('.menu-active').removeClass('menu-active');
	  clicked.parent('li').addClass('menu-active');
	  clicked.closest('.search-dropdown').find('.toggle-active').html(clicked.html());
	});

	$(document).click(function() {
	  $('.search-dropdown.open').removeClass('open');
	});

});

