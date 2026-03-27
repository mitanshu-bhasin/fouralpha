/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./**/*.{html,js}"],
    theme: {
        extend: {
            colors: {
                cosmic: {
                    dark: "#0A0F24",
                    light: "#2B1B4D",
                    accent: "#171A3D"
                },
                gold: "#FFB800",
                slate: "#475569"
            },
            fontFamily: {
                sans: ["Montserrat", "Inter", "sans-serif"],
                serif: ["Merriweather", "serif"]
            }
        }
    },
    plugins: [],
}
