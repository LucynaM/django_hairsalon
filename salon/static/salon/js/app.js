$(document).ready(function(){


    /* change order of image and staff presentation box depending on screen width */
    function changeOrderOfLaoutElements() {

        const imagesToChangePosition = $('.staff-img');
        const staffRow = $('.staff-row');
        const windowWidthCondition = window.innerWidth < 768;

        if (windowWidthCondition) {
            staffRow.each(function(index) {
                if (index % 2 !== 0) {
                    $(this).find(".staff-img").remove();
                    $(this).prepend(imagesToChangePosition[index]);
                }
            })

        } else  {
            staffRow.each(function(index) {
                if (index % 2 !== 0 && $(this).children().eq(0).hasClass('staff-img')) {
                    $(this).children().eq(0).remove();
                    $(this).append(imagesToChangePosition[index]);
                }
            })
        }
    };

    changeOrderOfLaoutElements();

    $(window).resize(changeOrderOfLaoutElements);


    /* haircut-list table - dispaly second row on click */
    $('#haircut-list').on('click', '.row-active', function() {
        $(this).next().toggle();
    });


    /* smooth-scrolling */

	$("a[href^='#']").click(function(){

		var href = $(this).attr("href");
		$("html, body").animate({scrollTop: $(href).offset().top - 49}, 500);

	});


    /* scrollReveal */
    window.sr = ScrollReveal({ reset: true }).reveal('.scroll', { duration: 500 });

});