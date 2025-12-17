import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Public VAPID Key (debería venir del backend, pero para iniciar la suscripción la necesitamos)
// La obtendremos del endpoint.

export default function NotificationButton() {
    const [permission, setPermission] = useState(Notification.permission);
    const [loading, setLoading] = useState(false);
    const [subscribed, setSubscribed] = useState(false);

    const urlBase64ToUint8Array = (base64String) => {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    };

    const subscribeUser = async () => {
        setLoading(true);
        try {
            // Robust URL construction
            let baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

            // Ensure no trailing slash
            if (baseUrl.endsWith('/')) baseUrl = baseUrl.slice(0, -1);

            // Build proper API endpoint URL handling /api suffix
            let endpointUrl = baseUrl;
            // If baseUrl doesn't end in /api, append it (assuming backend lives at /api)
            if (!baseUrl.endsWith('/api')) {
                endpointUrl = `${baseUrl}/api`;
            }

            console.log(`[Push] Base API URL: ${baseUrl}`);
            console.log(`[Push] Using Endpoint: ${endpointUrl}`);

            // 1. Get Public Key
            const keyRes = await axios.get(`${endpointUrl}/notifications/vapid-public-key`);
            const publicKey = keyRes.data.publicKey;
            console.log("[Push] Public Key received");

            // 2. Request Permission
            const perm = await Notification.requestPermission();
            setPermission(perm);

            if (perm === 'granted') {
                // 3. Register SW
                const registration = await navigator.serviceWorker.ready;

                // 4. Subscribe (prevent error if already subscribed)
                let subscription = await registration.pushManager.getSubscription();
                if (!subscription) {
                    subscription = await registration.pushManager.subscribe({
                        userVisibleOnly: true,
                        applicationServerKey: urlBase64ToUint8Array(publicKey)
                    });
                }

                // 5. Send to Backend
                const user = JSON.parse(localStorage.getItem('user'));
                const email = user?.email || localStorage.getItem('userEmail') || 'tecnico@gesttec.com';

                await axios.post(`${endpointUrl}/notifications/subscribe?x_user_email=${email}`, {
                    endpoint: subscription.endpoint,
                    keys: subscription.toJSON().keys
                });

                setSubscribed(true);
                alert("¡Notificaciones activadas correctamente!");
            }
        } catch (error) {
            console.error("Error subscribing:", error);
            const status = error.response ? error.response.status : 'Network Error';
            alert(`Error al activar notificaciones (${status}): ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    if (permission === 'denied') {
        return <p className="text-xs text-red-500">Notificaciones bloqueadas.</p>;
    }

    if (subscribed || permission === 'granted') {
        // Podríamos chequear si realmente hay suscripción activa en SW, pero asumimos sí.
        return (
            <button className="flex items-center space-x-2 text-green-600 bg-green-50 px-3 py-1 rounded-full text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                <span>Activas</span>
            </button>
        );
    }

    return (
        <button
            onClick={subscribeUser}
            disabled={loading}
            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-700 transition"
        >
            {loading ? (
                <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            )}
            <span>Activar Notificaciones</span>
        </button>
    );
}
