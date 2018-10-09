module.exports = {
    plugins: [
        "react",
        "react-native"
    ],
    extends: [
        "google",
        "plugin:react-native/all"
    ],
    parserOptions: {
        ecmaVersion: 7,
        sourceType: "module",
        ecmaFeatures: {
            jsx: true,
        }
    },
    rules: {
        "padded-blocks": 0,
        "quotes": 0,
        "require-jsdoc": 0,
        "valid-jsdoc": 0,
        "no-var": 0,
        "space-before-function-paren": 0,
        "no-trailing-spaces": 0,
        "comma-dangle": 1,
        "react-native/no-unused-styles": 2,
        "react-native/split-platform-components": 2,
        "react-native/no-inline-styles": 2,
        "react-native/no-color-literals": 0,
        "react/jsx-uses-vars": [2],
    }
};
