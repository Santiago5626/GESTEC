import React from 'react';

// Componentes SVG animados con TailwindCSS
// Eliminamos dependencia de URLs externas (Lottie) para evitar errores 403/CORS

const LoadingSpinner = () => (
    <div className="flex flex-col items-center">
        <div className="relative w-16 h-16">
            <div className="absolute top-0 left-0 w-full h-full border-4 border-blue-200 rounded-full animate-ping opacity-75"></div>
            <div className="absolute top-0 left-0 w-full h-full border-4 border-t-blue-600 border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
        </div>
    </div>
);

const SuccessIcon = () => (
    <div className="rounded-full bg-green-100 p-4 animate-bounce-short">
        <svg className="w-16 h-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
        </svg>
    </div>
);

const ErrorIcon = () => (
    <div className="rounded-full bg-red-100 p-4 animate-pulse">
        <svg className="w-16 h-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
    </div>
);

const EmptyIcon = () => (
    <div className="rounded-full bg-gray-100 p-4">
        <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
        </svg>
    </div>
);

export default function StatusAnimation({ status, message, className = "w-32 h-32" }) {
    let Component = LoadingSpinner;

    if (status === 'success') Component = SuccessIcon;
    else if (status === 'error') Component = ErrorIcon;
    else if (status === 'empty') Component = EmptyIcon;

    return (
        <div className="flex flex-col items-center justify-center py-10 w-full h-full min-h-[200px]">
            <div className="mb-4">
                <Component />
            </div>
            {message && <p className="text-gray-500 mt-2 text-sm font-medium animate-pulse">{message}</p>}
        </div>
    );
}
