/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./*.{js,ts,jsx,tsx}",
        "./components/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'memoweave-purple': '#7D5FB5',
                'memoweave-light': '#F6F3FA',
            },
        },
    },
    plugins: [],
}