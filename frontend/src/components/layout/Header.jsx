import React from 'react';

const BellIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
    </svg>
);

export default function Header() {
    return (
        <header className="bg-white p-4 flex justify-between items-center shadow-sm sticky top-0 z-10">
            <h1 className="text-2xl font-bold tracking-tight">
                <span className="text-blue-900">GEST</span>
                <span className="text-purple-500">TEC</span>
            </h1>
            <div className="flex items-center space-x-4">
                <div className="relative">
                    <span className="absolute -top-1 -right-1 bg-cyan-400 text-white text-xs font-bold rounded-full h-4 w-4 flex items-center justify-center">3</span>
                    <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                </div>
                <button
                    onClick={() => {
                        localStorage.removeItem('token');
                        localStorage.removeItem('user');
                        window.location.href = '/';
                    }}
                    className="text-sm font-medium text-red-500 hover:text-red-700 border border-red-200 px-3 py-1 rounded-lg transition-colors"
                >
                    Salir
                </button>
            </div>
        </header>
    );
}
