"use strict";

const courseDetailTemplate = require("courses/course_detail.html");
const coursePostulationTemplate = require("courses/course_postulate_front.html");

module.exports = ["$stateProvider", ($stateProvider) => {

    $stateProvider
        .state("courses", {
            url: "/courses",
            abstract: true,
            template: `<div class="courses-screen" ui-view>`,
            controller: "CoursesCtl" 
        })

        .state("courses.detail", {
            url: "/detail/{id:int}",
            params: {
                id: {
                    squash: false
                }
            },
            resolve: {
                courseData: [
                    "$stateParams",
                    'CoursesCollections'
                    ,($stateParams, CoursesCollections) => {
                        return CoursesCollections.PublicCourses.getInstance().getItem($stateParams.id);
                    }
                ]
            },
            controller: "CourseDetailCtl",
            template: courseDetailTemplate
        })

        .state("courses.postulate", {
            url: "/postulate/{id:int}",
            params: {
                id: {
                    squash: false 
                }
            },
            resolve: {
                courseData: [
                    "$stateParams",
                    "CoursesCollections",
                    ($stateParams, CoursesCollections) => {
                        return CoursesCollections.PublicCourses
                            .getInstance()
                            .getItem($stateParams.id);
                    }
                ]
            },
            template: coursePostulationTemplate,
            controller: "coursePostulateCtl"
        })
    ;
}];
