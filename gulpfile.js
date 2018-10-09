"use strict";

const gulp = require('gulp');
const gutil = require('gulp-util');

// Rename
const rename = require('gulp-rename');

// Styles
const sass = require('gulp-sass');
// const cleanCSS = require('gulp-clean-css');
const importCss = require("gulp-cssimport");

// Jshint
const jshint = require('gulp-jshint');
const stylish = require('jshint-stylish');

// Browserify
const browserify = require('browserify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');
const globby = require('globby');
const through = require('through2');
// const uglify = require('gulp-uglify');
const sourcemaps = require('gulp-sourcemaps');
const babelify = require('babelify');
const htmlminifyify = require("htmlminifyify");

// Mocha 
//const mocha = require('gulp-mocha');
const argv = require('yargs').argv;

// Shell
const shell = require('gulp-shell');

const paths = {
    sass: ['styles/index.scss'],
    lib: ['front/index.js']
};

gulp.task('build-sass', function(done) {
  gulp.src(paths.sass)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .on('error', sass.logError)
    .pipe(importCss({
        matchPattern: "!*.{less,sass,scss}" 
    }))
    /*.pipe(cleanCSS({
        compatibility: 'ie8'
    }))*/
    .pipe(sourcemaps.write())
    .pipe(rename("app.css"))
    .pipe(gulp.dest('./dist/css/'))
    .on('end', done);
});

gulp.task('check', function() {

    if (argv.nocheck) {
        return;
    }

    return gulp.src(paths.lib)
       .pipe(jshint({
            lookup: true,
       }))
       .pipe(jshint.reporter(stylish))
       .pipe(jshint.reporter('fail'));
});

gulp.task('build-lib', function () {

    var options = {
        paths: [
            'node_modules',
            'front',
            'templates'
        ],
    };

    var bundledStream = through();

    var babelifyTransform = babelify.configure({
        only: /front\/.+\.js$/
    });

    bundledStream
        .pipe(source(paths.lib[0]))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        .on('error', gutil.log)
        // .pipe(uglify())
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./dist/js/'));

    globby(['./front/**/*.js']).then((entries) => {
        var b = browserify({
            paths: options.paths,
            entries: entries,
            debug: true,
            transform: [babelifyTransform, htmlminifyify]
        });

        b.bundle().pipe(bundledStream);
    }).catch((err) => {
        bundledStream.emit('error', err); 
    });

    return bundledStream;

});

gulp.task('build-docs', shell.task([
            'node_modules/jsdoc/jsdoc.js '+
            '-c node_modules/angular-jsdoc/common/conf.json '+
            '-t node_modules/angular-jsdoc/angular-template '+
            '-d docs '+
            './README.md ' +
            '-r front'
]));

gulp.task('build', [
    'check',
    'build-sass',
    'build-lib'
]);

gulp.task('watch', ['build'], function() {
  gulp.watch("styles/**/*.scss", ['build-sass']);
  gulp.watch([
      "front/**/*",
      "templates/**/*"
  ],['check', 'build-lib']);
});

gulp.task('pre-commit', ['check']);

gulp.task('default', ['watch']);
