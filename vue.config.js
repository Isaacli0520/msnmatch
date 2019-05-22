const BundleTracker = require("webpack-bundle-tracker");
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

module.exports = {
    publicPath: IS_PRODUCTION ? 'static' : 'http://127.0.0.1:8080/',
    outputDir: 'dist',
    // assetsDir: 'static',

    pages: {
        home: {
          // entry for the page
          entry: 'src/home/main.js',
          // the source template
          template: 'templates/home.html',
          // output as dist/home.html
          filename: 'home.html',
          // when using title option,
          // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        //   title: 'Index Page',
          // chunks to include on this page, by default includes
          // extracted common chunks and vendor chunks.
        //   chunks: ['chunk-vendors', 'chunk-common', 'index']
        },
        // when using the entry-only string format,
        // template is inferred to be `public/subpage.html`
        // and falls back to `public/index.html` if not found.
        // Output filename is inferred to be `subpage.html`.
        superadmin: {
            // entry for the page
            entry: 'src/superadmin/main.js',
            // the source template
            template: 'templates/superadmin.html',
            // output as dist/superadmin.html
            filename: 'superadmin.html',
        },
        tagspage: {
          entry: 'src/tags/main.js',
          template: 'templates/tags.html',
          filename: 'tags.html',
        },
        familypage: {
          entry: 'src/family/main.js',
          template: 'templates/family.html',
          filename: 'family.html',
        },
        groupsmanagepage: {
          entry: 'src/groupsmanage/main.js',
          template: 'templates/groups_manage.html',
          filename: 'groups_manage.html',
        },
        grouppage: {
          entry: 'src/group/main.js',
          template: 'templates/group.html',
          filename: 'group.html',
        },
        grouptagpage: {
          entry: 'src/grouptag/main.js',
          template: 'templates/group_tag.html',
          filename: 'group_tag.html',
        },
      },

    chainWebpack: config => {

        config.optimization
            .splitChunks(false)

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: 'webpack-stats.json'}])

        config.resolve.alias
            .set('__STATIC__', 'static')
        
        config.devServer
            .public('http://0.0.0.0:8080')
            .host('0.0.0.0')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
            .clientLogLevel('info')
            }
    };