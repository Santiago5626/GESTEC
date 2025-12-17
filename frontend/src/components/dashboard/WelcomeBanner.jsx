import React from 'react';

export default function WelcomeBanner({ userName, openTickets }) {
    // Si tiene coma (Apellido, Nombre) toma el nombre, si no usa el string completo
    const firstName = userName && userName.includes(',') ? userName.split(',')[1] : userName;

    return (
        <div className="bg-gradient-to-r from-blue-900 to-pink-600 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
            <h2 className="text-lg font-semibold mb-1">Bienvenido de vuelta, {firstName}</h2>
            <p className="text-sm opacity-90">Tienes {openTickets} tickets abiertos</p>

            {/* Elemento decorativo opcional */}
            <div className="absolute -right-4 -top-4 bg-white opacity-10 rounded-full h-24 w-24 blur-xl"></div>
        </div>
    );
}
