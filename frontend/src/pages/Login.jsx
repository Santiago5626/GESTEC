import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await axios.post('http://localhost:8000/api/auth/login', {
                email,
                password
            });

            const { token, user } = response.data;
            // Guardar en localStorage (simple mock auth)
            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(user));

            if (user.role === 'admin') {
                navigate('/admin');
            } else if (user.role === 'technical') {
                navigate('/technical');
            } else {
                setError('Rol desconocido');
            }

        } catch (err) {
            setError('Credenciales inválidas');
            console.error(err);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
            {/* Background Gradient Top Half (aprox) */}
            <div className="absolute top-0 left-0 w-full h-[50vh] bg-gradient-to-r from-blue-900 via-purple-700 to-pink-600 z-0 rounded-b-[40px]"></div>

            <div className="relative z-10 flex flex-col items-center justify-center flex-grow p-4">

                {/* Logo Box */}
                <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 w-64 flex justify-center items-center">
                    <h1 className="text-3xl font-bold tracking-tight">
                        <span className="text-blue-900">GEST</span>
                        <span className="text-purple-500">TEC</span>
                    </h1>
                </div>

                <div className="text-white text-center mb-8">
                    <p className="text-sm font-medium tracking-wide">Sistema de Gestión Técnica</p>
                </div>

                {/* Login Card */}
                <div className="bg-white rounded-3xl shadow-xl p-8 w-full max-w-sm">
                    {/* Icon Circle */}
                    <div className="flex justify-center mb-4">
                        <div className="bg-purple-50 p-3 rounded-full">
                            <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                        </div>
                    </div>

                    <h2 className="text-2xl font-bold text-gray-800 text-center mb-1">Iniciar Sesión</h2>
                    <p className="text-gray-400 text-center text-sm mb-6">Ingresa tus credenciales para continuar</p>

                    <form onSubmit={handleLogin} className="space-y-4">
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1">Correo Electrónico</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                                </div>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-50"
                                    placeholder="tu@email.com"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1">Contraseña</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                                </div>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-50"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        {error && <p className="text-red-500 text-sm text-center">{error}</p>}

                        <button
                            type="submit"
                            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-bold text-white bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-all mt-6"
                        >
                            <span className="mr-2">➜</span> Iniciar Sesión
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
