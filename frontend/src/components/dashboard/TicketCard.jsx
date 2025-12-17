import React from 'react';

export default function TicketCard({ ticket }) {
    return (
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 relative mb-4 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-1">
                <span className="text-xs font-semibold text-gray-400">#{ticket.id}</span>
                <span className="bg-yellow-100 text-yellow-700 text-xs px-2 py-0.5 rounded-full font-medium">
                    {ticket.status}
                </span>
            </div>
            <h4 className="font-semibold text-gray-800 text-base mb-1 pr-6 leading-tight">
                {ticket.title}
            </h4>
            <p className="text-gray-500 text-sm mb-4">{ticket.user_role}</p>
            <div className="flex justify-between items-end">
                <span className="text-xs text-gray-400">{ticket.date}</span>
                <span className={`text-xs font-medium ${ticket.priority === 'Alta' ? 'text-red-500' :
                        ticket.priority === 'Media' ? 'text-orange-500' : 'text-green-500'
                    }`}>
                    {ticket.priority}
                </span>
            </div>
            {/* Arrow icon absolute */}
            <div className="absolute top-1/2 right-4 transform -translate-y-1/2">
                <svg className="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                </svg>
            </div>
        </div>
    );
}
