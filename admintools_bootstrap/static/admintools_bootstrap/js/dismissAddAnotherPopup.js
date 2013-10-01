$(function () {

	var django_dismimssPopup = window.dismissAddAnotherPopup;

	window.dismissAddAnotherPopup = function (win, newId, newRepr) {
		var name = windowname_to_id(win.name);
		var elem = document.getElementById(name);
		django_dismimssPopup(win, newId, newRepr);
		$(elem).removeClass('chzn-done');
		$('#' + name + '_chzn').remove();
		$(elem).chosen();
	}

	// menu search

	var nav_menu = $('#navigation-menu');
	var menu_map = [];
	var menu_url_map = {};
	var search_results = $('#menu_search ul');
	var menu_search_visible = false;

	$('#navigation-menu a').not('.dropdown-toggle').each(function (i, a) {
		var line = [a.text.toLowerCase().replace(/^\s+|\s+$/g, ''), a.href];
		menu_map[i] = line;
		menu_url_map[a.href] = a.text.replace(/^\s+|\s+$/g, '');
	});

	$('#menu_search input').keyup(function (e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		if (code == 40) {
			// down arrow key
			$('#menu_search ul li a:first').focus();
			return;
		}
		var inp = $(this).val().toLowerCase();
		if (inp == '') {
			search_results.html('');
			return;
		}
		var results = "";
		var highlight_re = new RegExp('(' + inp + ')', 'ig');
		var cnt = 0;
		var unique_map = {};
		$(menu_map).each(function (i, e) {
			if ((-1 != e[0].indexOf(inp)) && (cnt < 10)) {
				if (unique_map[e[1]]) {
					return;
				}
				var txt = menu_url_map[e[1]].replace(highlight_re, '<span class="highlight">$1</span>');
				results = results + '<li><a href="' + e[1] + '">' + txt + '</a></li>';
				unique_map[e[1]] = true;
				cnt++;
			}
		});
		search_results.html(results);
	});

	$('#menu_search ul li a').on('keydown', function (e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		if (code == 40) {
			e.preventDefault();
			$(this).parent().next().children('a').focus();
		}
		if (code == 38) {
			e.preventDefault();
			$(this).parent().prev().children('a').focus();
		}
	});

	$('#menu_search ul li a').on('mouseover', function (e) {
		$(this).focus();
	});

	$('#menu-search-toggle').click(function (e) {
		e.preventDefault();
		menu_search_visible = !menu_search_visible;
		$('#menu_search').toggle(menu_search_visible);
		if (menu_search_visible) {
			$(this).twipsy('hide');
			$('#menu_search input').focus();
		}
	});

});