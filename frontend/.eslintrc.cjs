module.exports = {
    env: {
        browser: true,
        es2021: true,
    },
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:ecmascript-compat/recommended",
        "plugin:svelte/recommended",
    ],
    overrides: [
        {
            files: ["*.svelte"],
            parser: "svelte-eslint-parser",
            parserOptions: {
                parser: "@typescript-eslint/parser",
            },
        },
    ],
    parser: "@typescript-eslint/parser",
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        extraFileExtensions: [".svelte"],
    },
    plugins: [
        "@typescript-eslint",
    ],
    rules: {
        "@typescript-eslint/no-unused-vars": ["warn", {argsIgnorePattern: "^_"}],
        "svelte/indent": ["warn", {indent: 4}],
    }
}
