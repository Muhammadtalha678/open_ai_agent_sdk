import { apiCallGet, apiCallPost } from "@/api/api_call";
import TodoList from "@/components/TodoList";
import { AppRoutes } from "@/constant/AppRoutes";
import { TodoListSchema } from "@/TypingSchemas/TodoListSchema";

export default async function Home() {
  const data = await apiCallGet(AppRoutes.allTodos)


  const todos: TodoListSchema[] = data.todos || []
  // console.log(data);
  return (
    <div className="bg-gray-50 min-h-screen">
      <h1 className="text-center text-2xl font-bold text-blue-800 px-4 pt-6 pb-2">
        All Todos
      </h1>
      <TodoList todos={todos} />
    </div>
  );
}

