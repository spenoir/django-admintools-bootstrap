/* vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4: */

/**
 * Dashboard plugin.
 * This plugin is not yet released, but should be when it will be finished.
 *
 * copyright (c) 2010 David Jean Louis <izimobil@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

(function($) {

    $.fn.extend({
        //pass the options variable to the function
        dashboard: function(options) {
            //Set the default values, use comma to separate the settings, example:
            var defaults = {
                panel_id: 'dashboard-panel',
                dashboard_id: this.attr('id'),
                dashboard_module_class: 'dashboard-module',
                columns: 2,
                load_preferences_function: false,
                save_preferences_function: false
            }
            var options = $.extend(defaults, options);

            return this.each(function() {
                // set ids for dashboard modules
                _initialize($(this), options);
                // restore positions, must be done *before* columnize
                _restore_positions($(this), options);
                _restore_flags($(this), options);
                // columnize the dashboard modules
                _columnize($(this), options);
                // add draggable behaviour
                _set_draggable($(this), options);
                // add collapsible behaviour
                _set_collapsible($(this), options);
                // add deletable behaviour
                _set_deletable($(this), options);
                // add addable behaviour to dashboard panel items
                _set_addable($(this), options);
                // restore user preferences
                _restore_preferences($(this), options);
            });
        },
        _calc_dashboard_pref: function() {
            var pref = {
                columns: [],
                disabled: {},
                collapsed: {},
                positions: []
            }

            $(this).find('.dashboard-module').each(function() {
                pref.disabled[this.id] = true;
                pref.collapsed[this.id] = $(this).find('.collapsed').length > 0;
            });

            // count of columns to show in each row
            $(this).children('.dashboard-column').each(function() {
                var colmodules = $(this).children();
                pref.columns.push(colmodules.length);
                colmodules.each(function(){
                    pref.positions.push(this.id);
                    pref.disabled[this.id] = false;
                });
            });

            return pref;
        }
    });

    var preferences = false;

    var _initialize = function(elt, options) {
        // load preferences
        if (preferences === false) {
            if (options.load_preferences_function) {
                preferences = options.load_preferences_function(options);
            } else {
                var json_str = $.cookie('admin-tools.' + options.dashboard_id);
                preferences = json_str ? JSON.parse(json_str) : {};
            }
        }
        // set ids if not set
        elt.children('div[id!=' + options.panel_id +']').each(function(index) {
            if (!$(this).attr('id')) {
                $(this).attr('id', 'module_' + index);
            }
        });
    };

    var _restore_positions = function(elt, options) {
        // restore positions
        try {
            var saved_positions = _get_preference(options, 'positions');
        } catch (e) {
            return;
        }
        var current_positions = _get_positions(elt, options);
        var new_positions = [];

        for(var v = 0; v < current_positions.length; v++) {
            new_positions[current_positions[v]] = current_positions[v];
        }

        for(var i = 0; i < saved_positions.length; i++) {
            // item id from saved order
            var id = saved_positions[i];
            if (id in new_positions) {
                var item = new_positions[id];
                var child = elt.children('#'+item);
                // select the item according to the saved order
                var saved = elt.children('#'+item);
                child.remove();
                elt.append(saved);
            }
        }
    };

    var _restore_flags = function(elt, options) {
        try {
            var saved_disabled = _get_preference(options, 'disabled');
        } catch (e) {
            return;
        }
        var elts = elt.children('div[id!=' + options.panel_id +']');
        elts.each(function() {
            var module = $(this);
            var is_disabled = saved_disabled[module.attr('id')];
            
            if (typeof is_disabled === 'undefined') {
                // No state saved for this module, use default
            } else {
                if (is_disabled) {
                    module.addClass('disabled');
                } else {
                    module.removeClass('disabled');
                }
            }
        });
    };

    var _columnize = function(elt, options) {
        var elts = elt.children('div[id!=' + options.panel_id +']:not(.disabled)');
        var size = Math.ceil(elts.length / options.columns);
        var sizes = _get_preference(options, 'columns');
        var percent = Math.floor(100 / options.columns);
        if ($.browser.msie && $.browser.version < 8.0) {
            percent -= 0.1;
        }
        var start = 0;
        var stop = 0;

        var columns = [];

        for (var i = 0; i < options.columns; i++) {
            if (typeof(sizes[i]) == 'undefined') {
                start = i * size;
                stop  = start + size;
            } else if (sizes[i] == 0) {
                columns.push($('<div class="dashboard-column" style="float:left;width:'+percent+'%;"/>'));
                continue;
            } else {
                start = (i == 0) ? 0 : start + sizes[i-1];
                stop  = start + sizes[i];
            }
            var col = ($('<div class="dashboard-column" style="float:left;width:'+percent+'%;"/>'));
            elts.slice(start, stop).appendTo(col);
            columns.push(col);
        }

        $.each(columns, function(i, v) {
            elt.append(v);
        });

        if ($.browser.msie && $.browser.version < 8.0) {
            $('.dashboard-column:last').css('float', 'right');
        }
    };

    var _restore_preferences = function(elt, options) {
        elt.find('.dashboard-module.disabled').each(function() {
            _delete_element($(this), options);
        });
        var disabled = _get_preference(options, 'disabled')
        ;
        if (disabled) {
            $.each(disabled, function(k, v) {
                var m = $('#' + k);
                if (m.length > 0) {
                    v ? _delete_element(m, options) : _add_element(m, options);
                } else {
                    delete disabled[k];
                }
            });
        }
        if (_get_preference(options, 'collapsed')) {
            $.each(_get_preference(options, 'collapsed'), function(k, v) {
                if (v) {
                    _toggle_element($('#'+k), options);
                }
            });
        }
        // if there's no element in the panel, hide it
        if (!$('#' + options.panel_id).find('li').length) {
            $('#' + options.panel_id).hide();
        }
    };

    var _set_draggable = function(elt, options) {
        // the dashboard column
        elt.children('.dashboard-column').sortable({
            handle: 'h2',
            items: '.draggable',
            connectWith: '.dashboard-column',
            placeholder: 'dashboard-placeholder',
            forcePlaceholderSize: true,
            cursor: 'crosshair',
            opacity: 0.7,
            update: function() {
                _save_preferences(elt, options);
            }
        });
    };

    var _set_collapsible = function(elt, options) {
        elt.find('.collapsible > h2').each(function() {
            $(this).append('<a href="#" class="toggle-icon">Toggle</a>').find('a.toggle-icon').click(function() {
                var prnt = $(this).parent().parent();
                _toggle_element(prnt, options, true);
            });
        });
    };

    var _toggle_element = function(elt, options, save_preference) {
        elt.find('h2 a.toggle-icon').toggleClass('collapsed');
        elt.children('div').slideToggle(500, function() {
            if (save_preference) {
                _save_preferences(elt, options);
            }
        });
    };

    var _set_deletable = function(elt, options) {
        elt.find('.deletable > h2').each(function() {
            $(this).append('<a href="#" class="close-icon">Close</a>').find('a.close-icon').click(function() {
                var prnt = $(this).parent().parent();
                _delete_element(prnt, options, true);
            });
        });
    };

    var _delete_element = function(elt, options, save_preference) {
        var existing = $('#'+options.panel_id).find('li a[rel='+elt.attr('id')+']');
        if (!existing.length) {
            var panel_ul = $('#' + options.panel_id).find('ul');
            if (!panel_ul.length) {
                $('#' + options.panel_id).append('<ul/>');
                panel_ul = $('#' + options.panel_id).find('ul');
            }
            panel_ul.append(
                '<li><a href="#" rel="'
                + elt.attr('id')
                + '" class="addlink dashboard-module-add">'
                + elt.find('h2').contents().first().text()
                + '</a></li>'
            );
            _set_addable(elt, options, $('#'+options.panel_id).find('li a[rel='+elt.attr('id')+']'));
        } else {
            existing.parent().show();
        }
        elt.fadeOut('fast', function() {
            var container = elt.closest('.dashboard-container');
            elt.detach().appendTo(container);
            $('#' + options.panel_id).show();
            if (save_preference) {
                _save_preferences(elt, options);
            }
        });
    };

    var _set_addable = function(elt, options, elts) {
        if (!elts) {
            elts = $('#'+options.panel_id).find('li a');
        }
        elts.click(function() {
            _add_element($('#'+$(this).attr('rel')), options, true);
        });
    };

    var _add_element = function(elt, options, save_preference) {
        var panel_elt = $('#'+options.panel_id).find('li a[rel='+elt.attr('id')+']');
        panel_elt.parent().remove();
        elt.removeClass('disabled');
        if (elt.closest('.dashboard-column').length === 0) {
            elt
                .closest('.dashboard-container')
                .find('.dashboard-column:last')
                .prepend(elt);
            elt.show();
        }
        elt.fadeIn('fast');
        if (save_preference) {
            _save_preferences(elt, options);
        }
        // if there's no element in the panel, hide it
        if (!$('#' + options.panel_id).find('li').length) {
            $('#' + options.panel_id).hide();
        }
    };

    var load_preferences = function(options) {
        if (options.load_preferences_function) {
            return options.load_preferences_function(options);
        }
        if (preferences === false) {
            var json_str = $.cookie('admin-tools.' + options.dashboard_id);
            preferences = json_str ? JSON.parse(json_str) : {};
        }
        return preferences;
    }

    var _get_preference = function(options, cat, id, defaultval) {
        try {
            if (preferences[cat] == undefined) {
                preferences[cat] = {};
            }
            if (id) {
                return preferences[cat][id];
            }
            return preferences[cat];
        } catch (e) {
            return defaultval ? defaultval : null;
        }
    };

    // quick hack to ensure that we do not save preferences if they are
    // not modified...
    var last_saved_preferences = null;

    function _save_preferences(elt, options) {
        var preferences = elt.closest('.dashboard-container')._calc_dashboard_pref();

        // save preferences
        if (JSON.stringify(preferences) != last_saved_preferences) {
            if (options.save_preferences_function) {
                options.save_preferences_function(options, preferences);
            } else {
                $.cookie(cookie_name, JSON.stringify(preferences), {expires: 1825});
            }
            last_saved_preferences = JSON.stringify(preferences);
        }
    };

    var _get_positions = function(elt, options) {
        var modules = [];
        if (!elt.children('.dashboard-column').length) {
            elt.children('div[id!=' + options.panel_id +']').each(function() {
                modules.push($(this).attr('id'));
            });
        } else {
            elt.children('.dashboard-column').each(function() {
                $.each($(this).sortable('toArray'), function(index, item) {
                    modules.push(item);
                });
            });
        }
        return modules;
    }

})(jQuery);
