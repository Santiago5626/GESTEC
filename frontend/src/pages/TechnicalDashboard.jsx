import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AppLayout from '../components/layout/AppLayout';
import WelcomeBanner from '../components/dashboard/WelcomeBanner';
import StatCard from '../components/dashboard/StatCard';
import TicketCard from '../components/dashboard/TicketCard';
import StatusAnimation from '../components/common/StatusAnimation';

// Iconos para stats (Reutilizados)
const CheckCircleIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>;
const ClockIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>;
const ExclamationIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>;
const TrendingUpIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>;

export default function TechnicalDashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const userStr = localStorage.getItem('user');
        const user = userStr ? JSON.parse(userStr) : null;
        const techId = user?.technician_id;
        const CACHE_KEY = `dashboard_cache_${techId}`;
        const CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

        // 1. Check Cache
        const cached = sessionStorage.getItem(CACHE_KEY);
        if (cached) {
            const { timestamp, data: cachedData } = JSON.parse(cached);
            if (Date.now() - timestamp < CACHE_DURATION) {
                console.log("Using cached dashboard data");
                setData(cachedData);
                setLoading(false);
                return; // Skip fetch if cache is valid
            }
        }

        // 2. Fetch from backend if no cache or expired
        axios.get(`${import.meta.env.VITE_API_URL}/dashboard/stats`, {
            headers: {
                'X-Technician-ID': techId || '',
                'X-User-Name': user?.name || ''
            }
        })
            .then(res => {
                setData(res.data);
                setLoading(false);
                // 3. Update Cache
                sessionStorage.setItem(CACHE_KEY, JSON.stringify({
                    timestamp: Date.now(),
                    data: res.data
                }));
            })
            .catch(err => {
                console.error("Error fetching data", err);
                // Si falla y tenemos cache aunque sea vieja, la usamos como fallback? 
                // Mejor mostrar error o dejar lo que había si ya seteamos data
                setLoading(false);
            });
    }, []);

    if (loading) return (
        <AppLayout>
            <StatusAnimation status="loading" message="Cargando tus tickets..." />
        </AppLayout>
    );

    if (!data) return (
        <AppLayout>
            <StatusAnimation status="error" message="No pudimos cargar tu información." />
        </AppLayout>
    );

    return (
        <AppLayout>
            <WelcomeBanner
                userName={data.user_name && data.user_name !== 'Usuario' ? data.user_name : (JSON.parse(localStorage.getItem('user'))?.name || 'Usuario')}
                openTickets={data.open_tickets_count}
            />

            {/* KPI Grid - Reused structure */}
            <div className="grid grid-cols-2 gap-4">
                <StatCard
                    label="Completados"
                    value={data.stats.completed}
                    icon={<CheckCircleIcon />}
                    bgClass="bg-green-100"
                    colorClass="text-green-600"
                />
                <StatCard
                    label="En servicio"
                    value={data.stats.in_service}
                    icon={<ClockIcon />}
                    bgClass="bg-blue-100"
                    colorClass="text-blue-600"
                />
                <StatCard
                    label="Abiertos"
                    value={data.stats.open}
                    icon={<ExclamationIcon />}
                    bgClass="bg-yellow-100"
                    colorClass="text-yellow-600"
                />
                <StatCard
                    label="Tareas Mes"
                    value={data.stats.this_month}
                    icon={<TrendingUpIcon />}
                    bgClass="bg-purple-100"
                    colorClass="text-purple-600"
                />
            </div>

            {/* My Tickets Section */}
            <div>
                <div className="flex justify-between items-center mb-3">
                    <h3 className="text-lg font-semibold text-gray-800">Mis Tickets Asignados</h3>
                </div>

                {data.recent_tickets.length === 0 ? (
                    <p className="text-gray-500 text-sm text-center py-4 bg-white rounded-xl">No tienes tickets pendientes.</p>
                ) : (
                    <div className="space-y-3">
                        {data.recent_tickets.map((ticket) => (
                            <TicketCard key={ticket.id} ticket={ticket} />
                        ))}
                    </div>
                )}
            </div>
        </AppLayout>
    );
}
