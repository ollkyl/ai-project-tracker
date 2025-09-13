import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface User {
  id: number;
  name: string;
  email: string;
  telegram_id: number | null;
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
      setUsers(response.data);
    } catch (err) {
      setError('Ошибка загрузки данных пользователей');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  if (loading) return <div className="text-center p-4">Загрузка...</div>;
  if (error) return <div className="text-red-500 text-center p-4">{error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Панель администратора</h1>
      {users.length === 0 ? (
        <p>Пользователи не найдены</p>
      ) : (
        <ul className="space-y-4">
          {users.map((user) => (
            <li key={user.id} className="border p-4 rounded hover:bg-gray-100">
              <Link href={`/users/${user.id}`}>
                <div className="cursor-pointer">
                  <h2 className="text-xl font-semibold">Пользователь: {user.name}</h2>
                  <p>Email: {user.email}</p>
                  <p>Telegram ID: {user.telegram_id ?? 'N/A'}</p>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AdminPanel;