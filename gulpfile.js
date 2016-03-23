/**
 * Gulpfile used to build static CSS/JS/Images used by django templates
 */

var gulp = require('gulp');
var chug = require( 'gulp-chug' );
var awspublish = require('gulp-awspublish');
var cloudfront = require("gulp-cloudfront");
var del = require('del');
var rename = require('gulp-rename');

gulp.paths = {
    src: {
        base: './webapp'
    },
    statics: './staticfiles',
    dist: './staticfiles/dist',
    templates: 'server/templates/dist'
};

var aws = {
    params: {
        Bucket: "mybucket",
        Region: "us-east-1"
    },
    "distributionId": "XYZ123"
};

var publisher = awspublish.create(aws);
// One week = 604,800
var headers = {'Cache-Control': 'max-age=604800, no-transform, public'};
var index_header = {'Cache-Control': 'public, must-revalidate, proxy-revalidate, max-age=0'};

gulp.task('clean', function(cb) {
    return del([gulp.paths.dist + '/*'], cb)
});

gulp.task( 'base', [], function () {
    return gulp.src( gulp.paths.src.base +'/gulpfile.js', { read: false } )
        .pipe( chug({
            tasks:  [ 'templates' ]
        }) )
});

gulp.task('deploy', ['base'], function () {
    return gulp.src([gulp.paths.statics + '/**', '!'+ gulp.paths.dist + '/**/index.html'])
        .pipe(rename(function (path) {
            path.dirname = 'static/' + path.dirname;
        }))
        .pipe(awspublish.gzip())
        .pipe(publisher.publish(headers))
        .pipe(publisher.cache())
        .pipe(awspublish.reporter())
        .pipe(cloudfront(aws));
});

gulp.task('default', ['deploy']);

