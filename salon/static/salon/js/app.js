$(document).ready(function(){

    /* switch page elements - start */
    function pageLayout () {
        const windowWidth = $(window).width();
        const staff = $('.staff2');
        const staff_row = $('.staff-row').eq(1);
        if (windowWidth < 757) {
            if (staff.eq(0).hasClass('staff-data')) {
                staff_row.html("");
                staff_row.append(staff.eq(1));
                staff_row.append(staff.eq(0));
            }

        } else {
            if (staff.eq(0).hasClass('staff-img')) {
                staff_row.html("");
                staff_row.append(staff.eq(1));
                staff_row.append(staff.eq(0));
            }
        }
    }

    pageLayout();

    $(window).bind('resizeEnd', function() {
        pageLayout();
    });

    $(window).resize(function() {
        if(this.resizeTO) clearTimeout(this.resizeTO);
        this.resizeTO = setTimeout(function() {
            $(this).trigger('resizeEnd');
        }, 500);
    });

    /* switch page elements - start */

    /* haircut-list table - dispaly second row on click - start */
    $('#haircut-list').on('click', '.row-active', function() {
        console.log('klikam');
        $(this).next().toggle();
    });
    /* haircut-list table - dispaly second row on click - stop */

    /*smooth-scrolling - start*/

	$("a[href^='#']").click(function(){

		var href = $(this).attr("href");
		$("html, body").animate({scrollTop: $(href).offset().top - 49}, 500);

	});
    /*smooth-scrolling - stop*/

    /*scrollReveal - start*/
    window.sr = ScrollReveal({ reset: true }).reveal('.scroll', { duration: 500 });
    /*scrollReveal - stop*/

});