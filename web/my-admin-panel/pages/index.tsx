import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Task {
  id: number;
  title: string;
  status: string;
  progress: number;
}

interface Project {
  id: number;
  title: string;
  description: string;
  tasks: Task[];
}

interface User {
  id: number;
  name: string;
  email: string;
  telegram_id: number | null;
  projects: Project[];
}

const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const AdminPanel: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

const fetchUsers = async () => {
  try {
    setLoading(true);
    setError(null);

    const response = await axios.get(`${apiUrl}/users/`);
    const usersData: User[] = response.data;

    const usersWithProjects = await Promise.all(
      usersData.map(async (u) => {
        try {
          const projectsRes = await axios.get(`${apiUrl}/projects/`, {
            params: { user_id: u.telegram_id },
          });
          const projects = projectsRes.data.map((p: Project) => ({
            ...p,
            tasks: p.tasks ?? [],
          }));

          return { ...u, projects };
        } catch (err) {
          console.error(`Ошибка при загрузке проектов пользователя ${u.id}`, err);
          return { ...u, projects: [] };
        }
      })
    );

    setUsers(usersWithProjects);
  } catch (err) {
    setError("Ошибка загрузки данных пользователей");
    console.error(err);
  } finally {
    setLoading(false);
  }
};



  useEffect(() => {
    fetchUsers();
  }, []);

  const markTaskAsDone = async (taskId: number) => {
    try {
      await axios.patch(`${apiUrl}/tasks/${taskId}`, { status: 'done' });
      fetchUsers();
    } catch (err) {
      setError('Ошибка обновления задачи');
      console.error(err);
    }
  };

  const getAIReview = async (projectId: number, telegramId: number | null) => {
    try {
      const response = await axios.get(`${apiUrl}/report/${projectId}?user_id=${telegramId}`);
      const { ai_advice } = response.data;
      alert(ai_advice);
    } catch (err) {
      setError('Ошибка AI-анализа');
      console.error(err);
    }
  };

  if (loading) return <div className="text-center p-4">Загрузка...</div>;
  if (error) return <div className="text-red-500 text-center p-4">{error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Панель администратора</h1>
      {users.length === 0 ? (
        <p>Пользователи не найдены</p>
      ) : (
        users.map((user) => (
          <div key={user.id} className="mb-6 border p-4 rounded">
            <h2 className="text-xl font-semibold">Пользователь: {user.name}</h2>
            <p>Email: {user.email}</p>
            <p>Telegram ID: {user.telegram_id ?? 'N/A'}</p>
            <h3 className="text-lg font-medium mt-4">Проекты:</h3>
            {user.projects.length === 0 ? (
              <p>Проекты не найдены</p>
            ) : (
              user.projects.map((project) => (
                <div key={project.id} className="ml-4 mb-4 border-l-4 pl-4">
                  <h4 className="text-md font-medium">Проект: {project.title}</h4>
                  <p>Описание: {project.description}</p>
                  <button
                    onClick={() => getAIReview(project.id, user.telegram_id)}
                    className="bg-blue-500 text-white px-2 py-1 rounded mt-2 mr-2"
                  >
                    AI Review
                  </button>
                  <h5 className="text-sm font-medium mt-2">Задачи:</h5>
                  {project.tasks.length === 0 ? (
                    <p>Задачи не найдены</p>
                  ) : (
                    <ul className="list-disc ml-6">
                      {project.tasks.map((task) => (
                        <li key={task.id}>
                          {task.title} (Status: {task.status}, Progress: {task.progress})
                          {task.status !== 'done' && (
                            <button
                              onClick={() => markTaskAsDone(task.id)}
                              className="bg-green-500 text-white px-2 py-1 rounded ml-2"
                            >
                              Отметить как выполненную
                            </button>
                          )}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default AdminPanel;