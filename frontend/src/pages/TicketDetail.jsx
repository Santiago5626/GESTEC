import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import AppLayout from '../components/layout/AppLayout';

import StatusAnimation from '../components/common/StatusAnimation';

export default function TicketDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [ticket, setTicket] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        // Fetch specific ticket details
        axios.get(`http://localhost:8000/api/tickets/${id}`)
            .then(res => {
                setTicket(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching ticket details", err);
                setError(true);
                setLoading(false);
            });
    }, [id]);

    if (loading) return <StatusAnimation status="loading" message="Cargando detalles del ticket..." />;
    if (error || !ticket) return (
        <div className="flex flex-col items-center">
            <StatusAnimation status="error" message="No se pudo cargar el ticket. Intenta nuevamente." />
            <button onClick={() => navigate(-1)} className="mt-4 text-blue-600 hover:underline">Volver atrás</button>
        </div>
    );

    const priorityColors = {
        'Alta': 'bg-red-100 text-red-700',
        'Media': 'bg-yellow-100 text-yellow-700',
        'Baja': 'bg-green-100 text-green-700'
    };

    const priorityColor = priorityColors[ticket.priority] || 'bg-gray-100 text-gray-700';

    return (
        <AppLayout>
            {/* Header / Back Button */}
            <div className="flex items-center space-x-3 mb-6">
                <button onClick={() => navigate(-1)} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                    <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                </button>
                <div>
                    <h2 className="text-xl font-bold text-gray-900">Detalle del Ticket</h2>
                    <p className="text-sm text-gray-500">#{ticket.id}</p>
                </div>
            </div>

            {/* Actions */}
            <div className="flex space-x-3 mb-6">
                <button className="flex-1 bg-green-500 hover:bg-green-600 text-white font-medium py-2.5 rounded-xl shadow-sm flex justify-center items-center space-x-2 transition-colors">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
                    <span>Llenar Visita Técnica</span>
                </button>
                <button className="flex-1 bg-white border border-gray-200 text-gray-700 font-medium py-2.5 rounded-xl hover:bg-gray-50 flex justify-center items-center space-x-2 transition-colors">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
                    <span>Compartir</span>
                </button>
            </div>

            {/* Main Info Card */}
            <div className="bg-white rounded-2xl p-6 shadow-sm mb-4 border border-gray-100">
                <div className="mb-4">
                    <h3 className="text-base font-bold text-blue-900 mb-3 uppercase leading-snug">{ticket.subject}</h3>
                    <div className="flex space-x-2">
                        <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-xs font-bold rounded-full">
                            {ticket.status}
                        </span>
                        <span className={`px-3 py-1 text-xs font-bold rounded-full ${priorityColor}`}>
                            Prioridad {ticket.priority}
                        </span>
                    </div>
                </div>

                <div className="space-y-3 text-sm border-t border-gray-100 pt-4">
                    <div className="flex justify-between">
                        <span className="text-gray-500">Solicitante:</span>
                        <span className="font-medium text-gray-900">{ticket.requester}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-500">Técnico asignado:</span>
                        <span className="font-medium text-gray-900">{ticket.technician}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-500">Grupo:</span>
                        <span className="font-medium text-gray-900">{ticket.group}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-500">Fecha de creación:</span>
                        <span className="font-medium text-gray-900">{ticket.created_time}</span>
                    </div>
                </div>
            </div>

            {/* Description Card */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-20">
                <h4 className="text-sm font-bold text-gray-900 mb-3">Descripción</h4>
                <div className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                    {ticket.description && ticket.description.replace(/<[^>]*>?/gm, '')} {/* Basic Strip HTML if needed */}
                </div>
            </div>

        </AppLayout>
    );
}
