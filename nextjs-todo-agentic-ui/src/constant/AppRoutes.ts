const dev_url = "http://localhost:8000"
const prod_url = process.env.NEXT_PUBLIC_PROD_URL
const base_url = process.env.NODE_ENV === "production" ? prod_url : dev_url

export const AppRoutes = {
    allTodos: `${base_url}/api/todos`,
    chat: `${base_url}/api/query`,
}