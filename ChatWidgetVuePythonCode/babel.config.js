// module.exports = {
//     presets: ["@vue/cli-plugin-babel/preset"],
//     presets: [
//         ['@vue/app', {
//             useBuiltIns: 'entry'
//         }]
//     ],
//     plugins: ["@babel/plugin-transform-arrow-functions"]
// }

module.exports = {
        "presets": [
            ["@babel/preset-env", {
                "modules": false,
                "corejs": "^3.6.5",
                "useBuiltIns": "entry",
                "targets": {
                    "browsers": [" >0.25% ", "last 5 versions", "not ie<=10"]
                }
            }]
        ],
        "plugins": [
            ["@babel/plugin-proposal-decorators",
                {
                    "legacy": true
                }
            ],
            "@babel/plugin-transform-arrow-functions",
            "@babel/plugin-proposal-class-properties",
            "@babel/plugin-transform-runtime",
            "@babel/plugin-transform-classes",
            "@babel/plugin-syntax-dynamic-import",
            "@babel/plugin-proposal-json-strings",
            "@babel/plugin-proposal-export-namespace-from",
            "@babel/plugin-proposal-throw-expressions",
            "@babel/plugin-proposal-export-default-from"
        ]
    }
    // env: {
    //     production: {
    //         "preset": [
    //             '@babel/preset-env',
    //         ],
    //         "plugin": [
    //             '@babel/plugin-proposal-class-properties',
    //             'transform-es2015-modules-commonjs',
    //             'babel-plugin-dynamic-import-node',
    //         ]
    //     }
    // }