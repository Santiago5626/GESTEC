import React from 'react';
import Header from './Header';
import BottomNav from './BottomNav';

export default function AppLayout({ children }) {
    return (
        <div className="min-h-screen bg-gray-50 font-sans pb-24">
            <Header />
            <main className="p-4 space-y-6">
                {children}
            </main>
            <BottomNav />
        </div>
    );
}
