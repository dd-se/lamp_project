$('.cardAnimation').animate({
    height: '300px',
    width: '350px'
},
    {
        duration: 1500,
        step: function () {
            console.log($(this).width());
        },
        complete: function () {
            console.log("done");
        }
    }
);
$('.moviesAnimation').animate({
    height: '410px',
    width: '350px'
},
    {
        duration: 1500,
        step: function () {
            console.log($(this).width());
        },
        complete: function () {
            console.log("done");
        }
    }
);