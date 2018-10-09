"use strict";

require("slick-carousel");

const $ = require('jquery');

$('.responsive').slick({
    pauseOnHover: false,
    dots: false,
    infinite: false,
    focusOnSelect: false,
    speed: 300,
    slidesToShow: 6,
    slidesToScroll: 4,
    responsive: [
    {
        breakpoint: 1024,
        settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            infinite: false,
            dots: false
        }
    },
    {
        breakpoint: 600,
        dots: false,
        settings: {
            slidesToShow: 3,
            slidesToScroll: 2
        }
    },
    {
        dots: false,
        breakpoint: 480,
        settings: {
            slidesToShow: 3,
            slidesToScroll: 1
        }
    }
    ]
});
