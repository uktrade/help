// GULPFILE
// - - - - - - - - - - - - - - -
// This file processes all of the assets in the "assets" folder
// and outputs the finished files in the "contact/static" folder.

// LIBRARIES
// - - - - - - - - - - - - - - -
import gulp from 'gulp';
import stylish from 'jshint-stylish';
import paths from './projectpath.babel';
import loadPlugins from 'gulp-load-plugins';

const plugins = loadPlugins();


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

gulp.task('lint', ['lint:js']);


// Default: compile everything
gulp.task('default', ['javascripts']);

// Optional: recompile on changes
gulp.task('watch', ['watchForChanges']);

gulp.task('test', ['lint']);