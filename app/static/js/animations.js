$('.cardAnimation').animate({
    height: '250px',
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