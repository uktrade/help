// GULPFILE
// - - - - - - - - - - - - - - -
// This file processes all of the assets in the "assets" folder
// and outputs the finished files in the "static" folder.

// LIBRARIES
// - - - - - - - - - - - - - - -
import gulp from 'gulp';
import sourcemaps from 'gulp-sourcemaps';
import path from 'path';
import sass from 'gulp-sass';
import stylish from 'jshint-stylish';
import paths from './projectpath.babel';
import loadPlugins from 'gulp-load-plugins';

const plugins = loadPlugins(),
    protractor = plugins.protractor.protractor,
    webdriver_standalone = plugins.protractor.webdriver_standalone,
    webdriver_update = plugins.protractor.webdriver_update;

gulp.task('webdriver_update', webdriver_update);
gulp.task('webdriver_standalone', webdriver_standalone);

const SASS_FILES = `${paths.src}/stylesheets/**/*.scss`;
const OUTPUT_CSS = `${paths.dist}/stylesheets`;

// set debugMode to true to use non uglified and compressed js versions
let debugMode = false ? { mangle: false, compress: false, output: { beautify: true } } : null;

// TASKS
// - - - - - - - - - - - - - - -

gulp.task('javascripts', () => gulp
    .src([
        paths.src + 'javascripts/**/*.js'
    ])
    .pipe(plugins.babel({
        presets: ['es2015']
    }))
    .pipe(plugins.uglify(debugMode))
    .pipe(plugins.addSrc.prepend([
        paths.npm + 'jquery/dist/jquery.min.js',
        paths.npm + 'underscore/underscore-min.js',
    ]))
    .pipe(plugins.concat('all.js'))
    .pipe(gulp.dest(paths.dist + 'javascripts/'))
);

gulp.task('images', () =>
    gulp.src(paths.src+'images/**/*')
        .pipe(plugins.imagemin({
            progressive: true
        }))
        .pipe(gulp.dest(paths.dist + 'images/'))
);

gulp.task('stylesheets', () =>
    gulp.src(paths.src+'stylesheets/**/*')
        .pipe(gulp.dest(paths.dist + 'stylesheets/'))
);

gulp.task('sass', function () {
  return gulp.src(SASS_FILES)
    .pipe(sourcemaps.init())
    .pipe(sass({
      outputStyle: 'expanded'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./sourcemaps', {includeContent: false}))
    .pipe(gulp.dest(OUTPUT_CSS));
});

gulp.task('external-links', () =>
    gulp.src(paths.src+'external-links/**/*')
        .pipe(gulp.dest(paths.dist + 'external-links/'))
);

// Watch for changes and re-run tasks
gulp.task('watchForChanges', function() {
    gulp.watch(paths.src + 'javascripts/**/*', ['javascripts']);
    gulp.watch('gulpfile.babel.js', ['default']);
});


gulp.task('lint:js', () => gulp
    .src(paths.src + 'javascripts/**/*.js')
    .pipe(plugins.jshint({'esversion': 6, 'esnext': false}))
    .pipe(plugins.jshint.reporter(stylish))
    .pipe(plugins.jshint.reporter('fail'))
);


gulp.task('protractor:e2e', (callback) => gulp
    .src(['assets/test/e2e/specs/*-spec.js'])
    .pipe(protractor({
        'configFile': 'assets/test/e2e/conf.js',
    })).on('error', function(e) {
        console.log(e);
    }).on('end', function (callback) {
        callback;
    })
);

gulp.task('lint', ['lint:js']);


// Default: compile everything
gulp.task('default', ['javascripts', 'images', 'stylesheets', 'sass', 'external-links']);

// Optional: recompile on changes
gulp.task('watch', ['watchForChanges']);

gulp.task('test', ['lint', 'default']);
