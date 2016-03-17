/**
 * Gulpfile used to build static CSS/JS/Images used by django templates
 */

var gulp = require('gulp');
var chug = require( 'gulp-chug' );
var awspublish = require('gulp-awspublish');
var cloudfront = require("gulp-cloudfront");
var del = require('del');
var replace = require('gulp-replace');
var rename = require('gulp-rename');
var es = require('event-stream');

gulp.paths = {
    src: {
        base: './staticbase'
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

var genStream = function(app) {
    // Black Magic to convert all static references to use django's 'static' templatetags
    return gulp.src(gulp.paths.dist + '/' + app + '/index.html')
        .pipe(replace(/href="([^h/]\S*)"/g, 'href="{% templatetag openblock %} static \'dist/' + app + '/$1\' {% templatetag closeblock %}"'))
        .pipe(replace(/src="([^h/]\S*)"/g, 'src="{% templatetag openblock %} static \'dist/' + app + '/$1\' {% templatetag closeblock %}"'))
        .pipe(gulp.dest(gulp.paths.templates + '/' + app));
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
            tasks:  [ 'build' ]
        }) )
});

gulp.task( 'build_local_base', ['base'], function () {

    return genStream('base');
});

gulp.task('build_local_all', ['clean', 'base'], function(){

    return es.merge(
        genStream('base')
    );
});

gulp.task('deploy', ['build_local_all'], function () {
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

