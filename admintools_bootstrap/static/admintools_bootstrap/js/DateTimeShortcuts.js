// Inserts shortcut buttons after all of the following:
//     <input type="text" class="vDateField">
//     <input type="text" class="vTimeField">

var DateTimeShortcuts = {
    calendars: [],
    calendarInputs: [],
    clockInputs: [],
    calendarDivName1: 'calendarbox', // name of calendar <div> that gets toggled
    calendarDivName2: 'calendarin',  // name of <div> that contains calendar
    calendarLinkName: 'calendarlink',// name of the link that is used to toggle
    clockDivName: 'clockbox',        // name of clock <div> that gets toggled
    clockLinkName: 'clocklink',      // name of the link that is used to toggle
    shortCutsClass: 'datetimeshortcuts', // class of the clock and cal shortcuts
    admin_media_prefix: '',
    init: function() {
        // Get admin_media_prefix by grabbing it off the window object. It's
        // set in the admin/base.html template, so if it's not there, someone's
        // overridden the template. In that case, we'll set a clearly-invalid
        // value in the hopes that someone will examine HTTP requests and see it.
        if (window.__admin_media_prefix__ != undefined) {
            DateTimeShortcuts.admin_media_prefix = window.__admin_media_prefix__;
        } else {
            DateTimeShortcuts.admin_media_prefix = '/missing-admin-media-prefix/';
        }

        var inputs = document.getElementsByTagName('input');
        for (i=0; i<inputs.length; i++) {
            var inp = inputs[i];
            if (inp.getAttribute('type') == 'text' && inp.className.match(/vTimeField/)) {
                DateTimeShortcuts.addClock(inp);
            }
            else if (inp.getAttribute('type') == 'text' && inp.className.match(/vDateField/)) {
                DateTimeShortcuts.addCalendar(inp);
            }
        }
    },
    handleClockQuicklink: function(num, val) {
       DateTimeShortcuts.clockInputs[num].value = val;
       DateTimeShortcuts.clockInputs[num].focus();
       DateTimeShortcuts.dismissClock(num);
    },

    handleCalendarQuickLink: function(num, offset) {
       var d = new Date();
       d.setDate(d.getDate() + offset)
       DateTimeShortcuts.calendarInputs[num].value = d.strftime(get_format('DATE_INPUT_FORMATS')[0]);
       DateTimeShortcuts.calendarInputs[num].focus();
       DateTimeShortcuts.dismissCalendar(num);
    },
    cancelEventPropagation: function(e) {
        if (!e) e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    }
}

addEvent(window, 'load', DateTimeShortcuts.init);
