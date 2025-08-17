import { TodoListSchema } from '@/TypingSchemas/TodoListSchema'
import React from 'react'

const TodoList = ({ todos }: { todos: TodoListSchema[] }) => {
  return (
    <div className="p-4">

      <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
        {
          todos.length > 0 ?
            (
              <table className="w-full text-sm text-left text-gray-700 bg-white">
                <thead className="text-xl uppercase bg-gray-200 text-gray-800">
                  <tr className="border-b border-gray-300">
                    <th className="px-6 py-3 text-center whitespace-nowrap">S.No</th>
                    <th className="px-6 py-3 text-center whitespace-nowrap">Title</th>
                    <th className="px-6 py-3 text-center whitespace-nowrap">Description</th>
                    <th className="px-6 py-3 text-center whitespace-nowrap">Status</th>
                    {/* <th className="px-6 py-3 text-center whitespace-nowrap">Actions</th> */}
                  </tr>
                </thead>
                <tbody>
                  {
                    todos.map((todo, index) => (
                      <tr key={index} className="bg-white border-b hover:bg-gray-50">
                        <td className="px-6 py-4 text-center">{index + 1}</td>
                        <td className="px-6 py-4 text-center">{todo.title}</td>
                        <td className="px-6 py-4 text-center">
                          {todo.description}</td>
                        <td className="px-6 py-4 text-center">{todo.status === false ? "Pending" : "Completed"}</td>

                      </tr>

                    ))

                  }
                </tbody>
              </table>

            ) : (

              <div className="text-center py-8 text-red-600 font-semibold text-lg">
                No Todos Found
              </div>

            )
        }


      </div>
    </div>
  )
}

export default TodoList
