import colors from 'vuetify/es5/util/colors'


const routerBase = process.env.DEPLOY_ENV === 'GH_PAGES' ? {
    router: {
        base: '/desarquivo/'
    }
} : {}

export default {
    mode: 'spa',
    ...routerBase,
    /*
     ** Headers of the page
     */
    head: {
        // titleTemplate: '%s - ' + process.env.npm_package_name,
        // title: process.env.npm_package_name || '',
        title: "Desarquivo",
        meta: [{
                charset: 'utf-8'
            },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1'
            },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || ''
            }, {
                property: 'og:image',
                content: "https://msramalho.github.io/desarquivo/favicon.ico"
            }, {
                property: 'og:title',
                content: "Desarquivo"
            }, {
                property: 'og:description',
                content: process.env.npm_package_description || ''
            }, {
                property: 'og:url',
                content: "https://msramalho.github.io/desarquivo"
            }, {
                property: 'og:locale',
                content: "pt"
            }
        ],
        link: [{
            rel: 'icon',
            type: 'image/x-icon',
            href: process.env.DEPLOY_ENV === 'GH_PAGES' ? '/desarquivo/favicon.ico' : '/favicon.ico'
        }]
    },
    /*
     ** Customize the progress-bar color
     */
    loading: {
        color: '#fff'
    },
    /*
     ** Global CSS
     */
    css: [],
    /*
     ** Plugins to load before mounting the App
     */
    plugins: [
        '@plugins/vuetify-toast',
        'plugins/i18n.js'
    ],
    /*
     ** Nuxt.js dev-modules
     */
    buildModules: [
        '@nuxtjs/vuetify',
    ],
    /*
     ** Nuxt.js modules
     */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios',
        ['cookie-universal-nuxt', {
            alias: 'cookies'
        }],
    ],
    /*
     ** Axios module configuration
     ** See https://axios.nuxtjs.org/options
     */
    axios: {
        // baseURL: "http://localhost:5000/"
        // baseURL: "https://cors-anywhere.herokuapp.com/http://35.234.109.95/"
        // baseURL: "https://rocky-spire-69467.herokuapp.com/http://35.234.109.95/"
        // baseURL: "https://peaceful-forest-55095.herokuapp.com//http://35.234.109.95/"
        baseURL: process.env.DEPLOY_ENV === 'GH_PAGES' ? "https://desarquivo-api.msramalho.xyz" : "http://localhost:5000/"
        // baseURL: "http://35.234.109.95/"
    },
    /*
     ** vuetify module configuration
     ** https://github.com/nuxt-community/vuetify-module
     */
    vuetify: {
        customVariables: ['~/assets/variables.scss'],
        theme: {
            themes: {
                light: {
                    primary: colors.teal.base,
                    accent: colors.teal.accent1,
                    secondary: colors.deepPurple.base
                }
            }
        }
    },
    /*
     ** Build configuration
     */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {}
    }
}