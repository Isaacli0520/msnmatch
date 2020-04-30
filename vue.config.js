const BundleTracker = require("webpack-bundle-tracker");
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

module.exports = {
	lintOnSave: false,
	// publicPath: IS_PRODUCTION ? 'static' : 'http://127.0.0.1:8080/',
	publicPath: IS_PRODUCTION ? 'https://d1ixiphwkdejqh.cloudfront.net/static/' : 'http://127.0.0.1:8080/',
	outputDir: 'dist',
	// assetsDir: 'static',
	transpileDependencies: ['vuetify'],
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
		skillpage: {
			entry: 'src/skill/main.js',
			template: 'templates/skill.html',
			filename: 'skill.html',
		},
		skillspage: {
			entry: 'src/skills/main.js',
			template: 'templates/skills.html',
			filename: 'skills.html',
		},
		coursespage: {
			entry: 'src/courses/main.js',
			template: 'templates/courses.html',
			filename: 'courses.html',
		},
		coursepage: {
			entry: 'src/course/main.js',
			template: 'templates/course.html',
			filename: 'course.html',
		},
		departmentpage: {
			entry: 'src/department/main.js',
			template: 'templates/department.html',
			filename: 'department.html',
		},
		departmentspage: {
			entry: 'src/departments/main.js',
			template: 'templates/departments.html',
			filename: 'departments.html',
		},
		mycoursespage: {
			entry: 'src/mycourses/main.js',
			template: 'templates/mycourses.html',
			filename: 'mycourses.html',
		},
		reviewspage: {
			entry: 'src/reviews/main.js',
			template: 'templates/reviews.html',
			filename: 'reviews.html',
		},
		courseinstructorpage: {
			entry: 'src/courseinstructor/main.js',
			template: 'templates/course_instructor.html',
			filename: 'course_instructor.html',
		},
		instructorpage: {
			entry: 'src/instructor/main.js',
			template: 'templates/instructor.html',
			filename: 'instructor.html',
		},
		commentspage: {
			entry: 'src/comments/main.js',
			template: 'templates/comments.html',
			filename: 'comments.html',
		},
		commentsendpage: {
			entry: 'src/commentsend/main.js',
			template: 'templates/commentsend.html',
			filename: 'commentsend.html',
		},
		commentfilterpage: {
			entry: 'src/commentfilter/main.js',
			template: 'templates/commentfilter.html',
			filename: 'commentfilter.html',
		},
		commentcreatepage: {
			entry: 'src/commentcreate/main.js',
			template: 'templates/commentcreate.html',
			filename: 'commentcreate.html',
		},
		market_page: {
			entry: 'src/market/main.js',
			template: 'templates/market.html',
			filename: 'market.html',
		},
		market_item_page: {
			entry: 'src/market_item/main.js',
			template: 'templates/market_item.html',
			filename: 'market_item.html',
		},
		market_my_items_page: {
			entry: 'src/market_my_items/main.js',
			template: 'templates/market_my_items.html',
			filename: 'market_my_items.html',
		},
		profile_page: {
			entry: 'src/profile/main.js',
			template: 'templates/profile.html',
			filename: 'profile.html',
		},
		profile_edit_page: {
			entry: 'src/profile_edit/main.js',
			template: 'templates/profile_edit.html',
			filename: 'profile_edit.html',
		},
		match: {
			entry: 'src/match/main.js',
			template: 'templates/match.html',
			filename: 'match.html',
		},
	},

	css: {
		loaderOptions: {
			sass: {
				data: `@import "~@/sass/main.scss"`,
			},
		},
	},

	// configureWebpack: {
	// 	plugins: [
	// 		new BundleAnalyzerPlugin({
	// 			generateStatsFile:true,
	// 		})
	// 	]
	// },

	chainWebpack: config => {
		["vue-modules", "vue", "normal-modules", "normal"].forEach((match) => {
			config.module.rule('sass').oneOf(match).use('sass-loader')
			.tap(opt => Object.assign(opt, { data: `@import 'src/sass/main.scss'` }))
		})
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