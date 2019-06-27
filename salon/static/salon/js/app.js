$(document).ready(function(){


    /* change order of image and staff presentation depending on screen width */
    class LayoutImgChanges {
        constructor() {
            this.changeOrder();
            window.addEventListener('resize', this.changeOrder);

        }
        changeOrder() {
            const imagesToChangePosition = [...document.querySelectorAll('.staff-img')];
            const staffRow = [...document.querySelectorAll('.staff-row')];
            const windowWidthCondition = window.innerWidth < 768;

            if (windowWidthCondition) {
                staffRow.forEach((row, index) => {
                    if (index % 2 !== 0) {
                        const elemToRemove = row.querySelector(".staff-img");
                        row.removeChild(elemToRemove);
                        row.prepend(imagesToChangePosition[index]);
                    }
                })
            } else  {
                staffRow.forEach((row, index) => {
                    if (index % 2 !== 0 && row.children[0].classList.contains('staff-img')) {
                        const elemToRemove = row.children[0];
                        row.removeChild(elemToRemove);
                        row.append(imagesToChangePosition[index]);
                    }
                })
            }

        }
    };

    const imageSwitch = new LayoutImgChanges();


    /* haircut-list table - display second row on click */
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