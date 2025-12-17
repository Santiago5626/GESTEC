import React, { useRef } from 'react';
import Lottie from 'lottie-react';

// URL de animaciones gratuitas de LottieFiles (direct JSON links)
// Nota: En producción, idealmente se descargarían estos assets a /public/animations
const ANIMATION_URLS = {
    loading: 'https://lottie.host/9f665552-328d-4229-87c2-95886616055d/0XvJtJgN8o.json', // Loader azul
    success: 'https://lottie.host/5a0c9664-002d-48d6-9969-90518be57494/2r8qY3M70e.json', // Check verde
    error: 'https://lottie.host/98064d7c-880c-4467-828e-595305141209/4C0X7g2qO0.json', // Error rojo
    empty: 'https://lottie.host/5b27163f-8c31-4e76-886f-a49d7967912d/5sK00aJt5n.json' // Empty state
};

export default function StatusAnimation({ status, message, className = "w-32 h-32" }) {
    const animationUrl = ANIMATION_URLS[status] || ANIMATION_URLS.loading;
    const [animationData, setAnimationData] = React.useState(null);

    React.useEffect(() => {
        let isMounted = true;
        fetch(animationUrl)
            .then(res => res.json())
            .then(data => {
                if (isMounted) setAnimationData(data);
            })
            .catch(err => console.error("Error loading lottie", err));

        return () => { isMounted = false; };
    }, [animationUrl]);

    if (!animationData) return <div className="animate-pulse bg-gray-100 rounded-full w-20 h-20 mx-auto opacity-50"></div>;

    return (
        <div className="flex flex-col items-center justify-center py-10 w-full h-full min-h-[200px]">
            <div className={className}>
                <Lottie animationData={animationData} loop={status === 'loading'} />
            </div>
            {message && <p className="text-gray-500 mt-4 text-sm font-medium animate-pulse">{message}</p>}
        </div>
    );
}
