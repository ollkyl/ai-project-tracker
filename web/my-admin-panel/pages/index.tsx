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
  completion_percentage?: number;
}

interface User {
  id: number;
  name: string;
  email: string;
  telegram_id: number | null;
  projects: Project[];
}

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://backend:8000";

const AdminPanel: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedUsers, setExpandedUsers] = useState<{ [key: number]: boolean }>({});
  const [expandedProjects, setExpandedProjects] = useState<{ [key: number]: boolean }>({});

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
            const projects = await Promise.all(
              projectsRes.data.map(async (p: Project) => {
                try {
                  const reportRes = await axios.get(
                    `${apiUrl}/report/${p.id}?user_id=${u.telegram_id}`
                  );
                  return {
                    ...p,
                    tasks: p.tasks ?? [],
                    completion_percentage: reportRes.data.completion_percentage,
                  };
                } catch (err) {
                  console.error(`Ошибка загрузки отчёта для проекта ${p.id}`, err);
                  return { ...p, tasks: p.tasks ?? [], completion_percentage: 0 };
                }
              })
            );
            return { ...u, projects };
          } catch (err) {
            console.error(`Ошибка при загрузке проектов пользователя ${u.id}`, err);
            return { ...u, projects: [] };
          }
        })
      );

      setUsers(usersWithProjects);
    } catch (err) {
      setError('Ошибка загрузки данных пользователей');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateTaskStatus = async (taskId: number, projectId: number, telegramId: number | null) => {
    try {
      setLoading(true);
      setError(null);

      await axios.patch(`${apiUrl}/tasks/${taskId}`, { status: 'done' });

      if (telegramId) {
        const reportRes = await axios.get(`${apiUrl}/report/${projectId}?user_id=${telegramId}`);
        const { completion_percentage, tasks } = reportRes.data;

        setUsers((prevUsers) =>
          prevUsers.map((user) =>
            user.telegram_id === telegramId
              ? {
                  ...user,
                  projects: user.projects.map((project) =>
                    project.id === projectId
                      ? { ...project, tasks, completion_percentage }
                      : project
                  ),
                }
              : user
          )
        );
      }
    } catch (err) {
      setError('Ошибка обновления задачи');
      console.error('Update task error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAIReview = async (projectId: number, telegramId: number | null) => {
    try {
      if (!telegramId) throw new Error('Telegram ID отсутствует');
      const response = await axios.get(`${apiUrl}/report/${projectId}?user_id=${telegramId}`);
      const { ai_advice } = response.data;
      alert(ai_advice);
    } catch (err) {
      setError('Ошибка AI-анализа');
      console.error('AI review error:', err);
    }
  };

  const toggleUser = (userId: number) => {
    setExpandedUsers((prev) => ({
      ...prev,
      [userId]: !prev[userId],
    }));
  };

  const toggleProject = (projectId: number) => {
    setExpandedProjects((prev) => ({
      ...prev,
      [projectId]: !prev[projectId],
    }));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  if (loading) return <div className="text-center p-4 text-gray-700">Загрузка...</div>;
  if (error) return <div className="text-red-600 text-center p-4">{error}</div>;

  return (
    <div className="container mx-auto p-4 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Панель администратора</h1>
      {users.length === 0 ? (
        <p className="text-gray-600">Пользователи не найдены</p>
      ) : (
        <ul className="space-y-4">
          {users.map((user) => (
            <li key={user.id} className="border-l-4 border-blue-500 p-4 rounded-lg shadow-sm bg-gray-50">
              <div
                className="flex items-center justify-between cursor-pointer"
                onClick={() => toggleUser(user.id)}
              >
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Пользователь: {user.name}</h2>
                  <p className="text-gray-700">Email: {user.email}</p>
                  <p className="text-gray-700">Telegram ID: {user.telegram_id ?? 'N/A'}</p>
                </div>
                <span className="text-lg text-gray-700">{expandedUsers[user.id] ? '▲' : '▼'}</span>
              </div>

              {expandedUsers[user.id] && (
                <div className="mt-4 space-y-4">
                  <h3 className="text-lg font-medium text-gray-800">Проекты:</h3>
                  {user.projects.length === 0 ? (
                    <p className="ml-4 text-gray-500">Проекты не найдены</p>
                  ) : (
                    <div className="ml-4 space-y-4">
                      {user.projects.map((project) => (
                        <div
                          key={project.id}
                          className="p-4 border rounded-lg shadow-md bg-white hover:bg-gray-50 transition"
                        >
                          <div
                            className="flex items-center justify-between cursor-pointer"
                            onClick={() => toggleProject(project.id)}
                          >
                            <h4 className="text-md font-medium text-gray-900">
                              {project.title} ({project.completion_percentage?.toFixed(1) ?? 0}% выполнено)
                            </h4>
                            <span className="text-lg text-gray-700">
                              {expandedProjects[project.id] ? '▲' : '▼'}
                            </span>
                          </div>

                          {expandedProjects[project.id] && (
                            <div className="mt-2 space-y-2">
                              <p className="text-gray-800">
                                <strong>Описание:</strong> {project.description}
                              </p>

                              <button
                                onClick={() => getAIReview(project.id, user.telegram_id)}
                                className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
                              >
                                AI Review
                              </button>

                              <h5 className="text-sm font-medium mt-2 text-gray-800">Задачи:</h5>
                              {project.tasks.length === 0 ? (
                                <p className="text-gray-500">Задачи не найдены</p>
                              ) : (
                                <ul className="list-disc ml-6 space-y-1">
                                  {project.tasks.map((task) => (
                                    <li
                                      key={task.id}
                                      className="flex items-center justify-between text-gray-900"
                                    >
                                      <span>{task.title}</span>
                                      {task.status !== 'done' ? (
                                        <button
                                          onClick={() =>
                                            updateTaskStatus(task.id, project.id, user.telegram_id)
                                          }
                                          className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600 transition ml-2"
                                        >
                                          В процессе
                                        </button>
                                      ) : (
                                        <span className="bg-green-500 text-white px-2 py-1 rounded ml-2">
                                          Выполнено
                                        </span>
                                      )}
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AdminPanel;
